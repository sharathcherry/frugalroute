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
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.style.use('dark_background')
    
    # Force a solid background color so transparency doesn't hide text in markdown
    fig.patch.set_facecolor('#111111')
    ax.set_facecolor('#111111')
    
    cmap = plt.get_cmap('tab20')
    
    for i, row in enumerate(data):
        is_star = '⭐' in row.get('pick', '')
        is_control = 'control' in row.get('pick', '') or '32B' in row['model']
        
        marker = '*' if is_star else ('X' if is_control else 'o')
        size = 350 if is_star else (200 if is_control else 120)
        
        color = cmap(i % 20)
        if is_star:
            color = 'gold'
        elif is_control:
            color = '#ff4444'
            
        ax.scatter(
            row['remote_tokens'], 
            row['accuracy'], 
            color=color, 
            marker=marker, 
            s=size, 
            edgecolors='white', 
            linewidths=1.5,
            label=row['model'],
            zorder=5
        )
    
    # Explicitly label the axes with bright text
    ax.set_xlabel('Remote Tokens (Cost) ↓', fontsize=13, color='white', labelpad=10)
    ax.set_ylabel('Accuracy ↑', fontsize=13, color='white', labelpad=10)
    ax.set_title('Cost vs Accuracy Pareto Frontier (MI300X Routing)', fontsize=15, color='white', pad=15)
    
    # Format tick marks so numbers are clearly visible
    ax.tick_params(axis='both', colors='white', labelsize=11)
    
    # Add a prominent grid
    ax.grid(True, color='gray', alpha=0.4, linestyle='--')
    
    # Invert x-axis so better (fewer tokens) is to the right
    ax.invert_xaxis()
    
    # Adjust limits to add some padding around the points
    x_vals = [r['remote_tokens'] for r in data]
    y_vals = [r['accuracy'] for r in data]
    if x_vals and y_vals:
        x_range = max(x_vals) - min(x_vals) if len(x_vals) > 1 else 100
        y_range = max(y_vals) - min(y_vals) if len(y_vals) > 1 else 0.1
        ax.set_xlim(max(x_vals) + x_range*0.1, min(x_vals) - x_range*0.1) # inverted
        ax.set_ylim(min(y_vals) - y_range*0.1, max(y_vals) + y_range*0.1)
    
    # Put a legend to the right
    legend = ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left", borderaxespad=0, title="Models", fontsize=11)
    legend.get_title().set_color('white')
    for text in legend.get_texts():
        text.set_color('white')
    legend.get_frame().set_facecolor('#222222')
    legend.get_frame().set_edgecolor('gray')
    
    pareto_path = os.path.join(os.path.dirname(__file__), "pareto.png")
    plt.savefig(pareto_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f"Generated {pareto_path}")

if __name__ == "__main__":
    main()
