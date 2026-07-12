import json
import os
import matplotlib.pyplot as plt

def main():
    bench_file = os.path.join(os.path.dirname(__file__), "benchmark.json")
    with open(bench_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Generate markdown table
    table_lines = [
        "| Model | Params | VRAM | Local hit-rate | Remote tokens ↓ | Accuracy | Latency | Pick |",
        "|-------|-------:|-----:|---------------:|----------------:|---------:|--------:|:----:|"
    ]
    for row in data:
        pick = row.get("pick", "")
        # Highlight the best row
        model_str = f"**{row['model']}**" if "⭐" in pick else row['model']
        table_lines.append(
            f"| {model_str} | {row['params']} | {row['vram_gb']}GB | {row['local_hit_rate']}% | {row['remote_tokens']} | {row['accuracy']} | {row['latency_s']}s | {pick} |"
        )
    
    table_md = "\n".join(table_lines)
    
    # Inject into README.md
    readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
    
    import re
    new_content = re.sub(
        r"<!-- BENCH_START -->.*?<!-- BENCH_END -->",
        f"<!-- BENCH_START -->\n{table_md}\n<!-- BENCH_END -->",
        readme_content,
        flags=re.DOTALL
    )
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated README.md table")
    
    # Inject into BENCHMARK.md
    bench_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "BENCHMARK.md")
    with open(bench_path, "r", encoding="utf-8") as f:
        bench_content = f.read()
    new_bench_content = re.sub(
        r"<!-- BENCH_START -->.*?<!-- BENCH_END -->",
        f"<!-- BENCH_START -->\n{table_md}\n<!-- BENCH_END -->",
        bench_content,
        flags=re.DOTALL
    )
    with open(bench_path, "w", encoding="utf-8") as f:
        f.write(new_bench_content)
    print(f"Updated BENCHMARK.md table")

    # Generate Pareto Chart
    plt.figure(figsize=(10, 6))
    plt.style.use('dark_background')
    
    texts = []
    for row in data:
        color = 'gold' if '⭐' in row.get('pick', '') else 'lightblue'
        marker = '*' if '⭐' in row.get('pick', '') else 'o'
        size = 200 if '⭐' in row.get('pick', '') else 100
        if 'control' in row.get('pick', '') or '32B' in row['model']:
            color = 'red'
            marker = 'X'
            size = 150
            
        plt.scatter(row['remote_tokens'], row['accuracy'], color=color, marker=marker, s=size, edgecolors='white')
        texts.append(plt.text(row['remote_tokens'], row['accuracy'], row['model'], fontsize=9, alpha=0.9))
    
    try:
        from adjustText import adjust_text
        adjust_text(texts, arrowprops=dict(arrowstyle="-", color='gray', lw=0.5))
    except ImportError:
        print("adjustText not found. Falling back to simple offsets. Run 'pip install adjustText' for better label placement.")
        for i, t in enumerate(texts):
            # Simple alternating offset to help reduce overlap
            x, y = t.get_position()
            t.set_position((x + 10, y + (0.005 if i % 2 == 0 else -0.005)))
            
    plt.xlabel('Remote Tokens (Cost) ↓', fontsize=12)
    plt.ylabel('Accuracy ↑', fontsize=12)
    plt.title('Cost vs Accuracy Pareto Frontier (MI300X Small Model Routing)', fontsize=14)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Invert x-axis so better (fewer tokens) is to the right
    plt.gca().invert_xaxis()
    
    pareto_path = os.path.join(os.path.dirname(__file__), "pareto.png")
    plt.savefig(pareto_path, dpi=300, bbox_inches='tight')
    print(f"Generated {pareto_path}")

if __name__ == "__main__":
    main()
