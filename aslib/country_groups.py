import os
import yaml
import re
import json
from copy import deepcopy
from ruamel.yaml import YAML
#pip install ruamel.yaml




#提取proxies组的 "name" 字段
def extract_field(file_path, rootkey, field):
    yaml = YAML(typ="safe")
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.load(file)
    names = [proxy[field] for proxy in data.get(rootkey, [])]
    return names





#根据国家代码对 "name" 字段的值进行分类, 按规则返回截取后的name字段的子串（目标是国家名称或代码）
def slice_proxies_name(name, slice_rule):
    if all(isinstance(item, int) for item in slice_rule):
        start, length = slice_rule
        return name[start:start+length]
    if isinstance(slice_rule[0], str) and isinstance(slice_rule[1], int):
        start_str, length = slice_rule
        start = name.find(start_str) + len(start_str) if name.find(start_str) != -1 else 0
        return name[start:start+length]
    if all(isinstance(item, str) for item in slice_rule):
        start_str, end_str = slice_rule
        start_index = name.find(start_str)
        end_index = name.find(end_str, start_index + len(start_str))
        if start_index == -1 or end_index == -1:
            return ""
        return name[start_index + len(start_str):end_index]
    if isinstance(slice_rule[0], int) and isinstance(slice_rule[1], str):
        start, end_str = slice_rule
        end_index = name.find(end_str, start)
        return name[start:] if end_index == -1 else name[start:end_index]
    return name
# 根据国家代码对 "name" 字段的值进行分类,
def classify_proxies_name(names, country_codes, slice_rule=None):
    classified = {country_values[0]: [] for country_values in country_codes.values()}
    # print("slice_rules规则截取后的节点名称:")
    for name in names:
        sliced_name = slice_proxies_name(name, slice_rule) if slice_rule else name
        # print(sliced_name)
        for code, country_values in country_codes.items():
            if code.lower() in sliced_name.lower() or any(country.lower() in sliced_name.lower() for country in country_values):
                classified[country_values[0]].append(name)
                break
        else:
            classified.setdefault('其它', []).append(name)
    return classified





def create_file_with_initial_content(output_file, initial_content):
    os.makedirs(os.path.dirname(output_file), exist_ok=True) if os.path.dirname(output_file) else None
    with open(output_file, 'w', encoding="utf-8") as f:
        if isinstance(initial_content, dict):
            f.write(json.dumps(initial_content, ensure_ascii=False, indent=4))
        else:
            f.write(initial_content)





def write_classify_proxies_to_output(output_file, classified, sort_keywords):
    yaml = YAML()
    data = {'proxy-groups': []}
    for country, names in classified.items():
        if names:
            group = {
                'name': 'Fallback',
                'type': 'fallback',
                'url': 'http://cp.cloudflare.com/generate_204',
                'interval': 7200,
                'proxies': [],
            }
            group['name'] = country
            group['proxies'] = group['proxies'] + names  # 创建新的代理列表并添加代理
            # 应用排序规则
            group['proxies'].sort(key=lambda proxy: [re.search(keyword, proxy) is not None for keyword in sort_keywords], reverse=True)
            data['proxy-groups'].append(group)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)  # 使用 ruamel.yaml 的 dump 方法直接写入文件


















def append_proxies_to_file(file_path, classified, sort_keywords, proxies_params, proxies_name='Auto_Url_Test'):
    # Since 'classified' is a list of proxy names, we'll use it directly as 'countries'
    countries = classified
    group = deepcopy(proxies_params)  # Use a deep copy of the passed dictionary to create a new proxy group
    group['name'] = proxies_name
    group['proxies'].extend(countries)  # Add proxy list to proxy group
    group['proxies'].sort(key=lambda proxy: [re.search(keyword, proxy) is not None for keyword in sort_keywords], reverse=True)
    
    # Convert the group to a YAML string with specific settings
    group_yaml = yaml.dump(group, default_flow_style=True, allow_unicode=True, width=float("inf")).strip()
    
    # Append the generated YAML string to the file
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write("- " + group_yaml + "\n")



