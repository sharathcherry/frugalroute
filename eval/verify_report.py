import os
import re
import sys

def verify_report():
    eval_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(eval_dir, 'report.md')
    if not os.path.exists(report_path):
        print(f"Error: report.md not found at {report_path}")
        return False

    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.strip():
        print("Error: report.md is empty")
        return False

    # 1. Parse table
    lines = content.split('\n')
    table_lines = []
    in_table = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|'):
            table_lines.append(stripped)
            
    if len(table_lines) < 3:
        print("Error: Master comparison table not found or too short")
        return False
        
    # The first line of the table is header, second is separator, the rest are data rows
    header = [p.strip() for p in table_lines[0].split('|')][1:-1]
    
    expected_headers = [
        "Model Name", "Parameter Size", "Developer", "Release Date", 
        "Knowledge Cutoff Date", "MMLU Score", "HumanEval Score", 
        "GSM8K Score", "Context Window Size"
    ]
    
    header_clean = [h.strip() for h in header]
    print(f"Found headers: {header_clean}")
    
    for eh in expected_headers:
        if eh not in header_clean:
            print(f"Error: Expected header '{eh}' not found in table headers")
            return False

    data_rows = []
    for line in table_lines[2:]:
        if '---' in line:
            continue
        parts = [p.strip() for p in line.split('|')][1:-1]
        if len(parts) >= 9:
            data_rows.append(parts)
            
    print(f"Parsed {len(data_rows)} data rows from the model catalog table.")
    
    # Verify: The file is not empty and has a table with >= 30 distinct model variants.
    if len(data_rows) < 30:
        print(f"Error: Found only {len(data_rows)} model variants, expected >= 30.")
        return False
        
    # Check distinct model names
    model_names = set(row[0] for row in data_rows)
    if len(model_names) < 30:
        print(f"Error: Only {len(model_names)} distinct model names found, expected >= 30.")
        return False

    # 2. At least 8 distinct model families are covered.
    families = set()
    for name in model_names:
        family = get_family(name)
        if family != 'Unknown':
            families.add(family)
            
    print(f"Covered families ({len(families)}): {sorted(list(families))}")
    if len(families) < 8:
        print(f"Error: Only {len(families)} model families covered, expected >= 8.")
        return False

    # 3. At least 80% of model cutoffs are documented (i.e. not empty or "N/A" in cutoff column).
    cutoff_col_idx = header_clean.index("Knowledge Cutoff Date")
    documented_cutoffs = 0
    for row in data_rows:
        cutoff = row[cutoff_col_idx].strip()
        if cutoff and cutoff != "N/A" and cutoff != "-":
            documented_cutoffs += 1
            
    cutoff_percentage = (documented_cutoffs / len(data_rows)) * 100
    print(f"Documented cutoffs: {documented_cutoffs}/{len(data_rows)} ({cutoff_percentage:.1f}%)")
    if cutoff_percentage < 80.0:
        print(f"Error: Only {cutoff_percentage:.1f}% of model cutoffs are documented, expected >= 80%.")
        return False

    # 4. Exactly 3 recommendations are present and each recommended model fits VRAM (<=70B parameters).
    # Let's search for "### Recommendations for AMD MI300X Routing"
    recommendations_section_match = re.search(
        r'### Recommendations for AMD MI300X Routing\s*\n(.*?)(?=\n##|\Z)', 
        content, 
        re.DOTALL
    )
    if not recommendations_section_match:
        print("Error: Section '### Recommendations for AMD MI300X Routing' not found.")
        return False
        
    recommendations_text = recommendations_section_match.group(1)
    
    # Find list items
    raw_list_items = re.findall(r'^\s*-\s+.*$', recommendations_text, re.MULTILINE)
    print(f"Raw recommendation list items count: {len(raw_list_items)}")
    if len(raw_list_items) != 3:
        print(f"Error: Expected exactly 3 recommendations, found {len(raw_list_items)}.")
        return False

    recommendations = {}
    for item in raw_list_items:
        match = re.search(r'\*\*(.*?)\*\*:\s*(.*?)\s*\((.*?)\)', item)
        if match:
            tier, name, size_str = match.groups()
            size_match = re.search(r'([\d\.]+)\s*B', size_str)
            if size_match:
                param_size = float(size_match.group(1))
            else:
                param_size = 0.0
            recommendations[tier.strip()] = {"name": name.strip(), "size": param_size}
        else:
            print(f"Warning: Could not parse recommendation item: {item}")
            
    print(f"Extracted recommendations: {recommendations}")
    if len(recommendations) != 3:
        print("Error: Failed to extract exactly 3 recommendation profiles with sizes.")
        return False

    for tier, info in recommendations.items():
        size = info["size"]
        vram_footprint = size * 2
        print(f"Recommended {tier} ({info['name']}): {size}B parameters -> {vram_footprint:.1f} GB VRAM")
        # Ensure it fits <= 70.6B parameters (which covers Llama-3.1-70B-Instruct at 70.6B)
        if size > 71.0:
            print(f"Error: Model {info['name']} has {size}B parameters, exceeding the 70B limit.")
            return False
        if vram_footprint > 192.0:
            print(f"Error: Model {info['name']} VRAM footprint of {vram_footprint} GB exceeds 192 GB.")
            return False

    # 5. Citations/sources are linked.
    sources_section_match = re.search(r'## Sources\s*\n(.*)', content, re.DOTALL)
    if not sources_section_match:
        print("Error: '## Sources' section not found.")
        return False
        
    sources_text = sources_section_match.group(1).strip()
    sources_count = len(re.findall(r'^\d+\.\s+.*$', sources_text, re.MULTILINE))
    print(f"Found {sources_count} sources in the Sources section.")
    if sources_count < 10:
        print(f"Error: Only {sources_count} sources found, expected >= 10.")
        return False

    mmlu_idx = header_clean.index("MMLU Score")
    he_idx = header_clean.index("HumanEval Score")
    gsm_idx = header_clean.index("GSM8K Score")
    
    missing_citations = []
    for row in data_rows:
        model = row[0]
        mmlu = row[mmlu_idx]
        he = row[he_idx]
        gsm = row[gsm_idx]
        
        for val, col_name in [(mmlu, "MMLU"), (he, "HumanEval"), (gsm, "GSM8K")]:
            val_clean = val.strip()
            if val_clean != "N/A" and not re.search(r'\[\d+\]', val_clean):
                missing_citations.append(f"{model} ({col_name}: {val_clean})")
                
    if missing_citations:
        print(f"Error: Found {len(missing_citations)} scores missing citations:")
        for mc in missing_citations[:10]:
            print(f"  - {mc}")
        return False
        
    print("\nAll checks PASSED successfully!")
    return True

def get_family(model_name):
    name = model_name.lower()
    if 'llama' in name:
        return 'Llama'
    elif 'gemma' in name:
        return 'Gemma'
    elif 'phi' in name:
        return 'Phi'
    elif 'qwen' in name:
        return 'Qwen'
    elif 'deepseek' in name:
        return 'DeepSeek'
    elif 'yi' in name:
        return 'Yi'
    elif 'mixtral' in name or 'mistral' in name:
        return 'Mistral/Mixtral'
    elif 'command' in name:
        return 'Command'
    elif 'internlm' in name:
        return 'InternLM'
    elif 'glm' in name or 'chatglm' in name:
        return 'GLM/ChatGLM'
    elif 'dbrx' in name:
        return 'DBRX'
    elif 'falcon' in name:
        return 'Falcon'
    elif 'starcoder' in name:
        return 'StarCoder'
    else:
        return 'Unknown'

if __name__ == '__main__':
    success = verify_report()
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
