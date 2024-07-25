import os
import yaml
import re
import requests
import time
import shutil
#pip install requests

base_dir = os.path.dirname(os.path.abspath(__file__))








# 下载文件    (如果文件存在，且大小不为0，且最后修改时间距离现在的秒数小于给定的参数，则跳过下载
def download_file(url, output_file, skip_if_modified_within_seconds=600):
    # 检查文件是否存在且在指定的时间内未被修改过
    if (os.path.exists(output_file) and
        os.path.getsize(output_file) > 0 and
        (time.time() - os.path.getmtime(output_file)) <= skip_if_modified_within_seconds):
        print(f"Skipping download for {output_file}, file is up-to-date.")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功
        os.makedirs(os.path.dirname(output_file), exist_ok=True)  # 创建必要的目录
        with open(output_file, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded and saved {url} to {output_file}")
    except requests.RequestException as e:
        print(f"Failed to download {url}: {str(e)}")








# 下载 rule_providers
def download_providers_from_yaml_file(yaml_file_path, base_path, skip_if_modified_within_seconds=600):
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)  # 直接从文件加载 YAML 数据
    
    if 'rule-providers' in data:
        for item in data['rule-providers'].values():
            if 'url' in item and 'path' in item:
                url = item['url']
                relative_path = item['path']
                full_path = os.path.join(base_path, relative_path)  # 构建完整的文件路径
                # 调用 download_file 函数以简化下载和保存文件的过程
                download_file(url, full_path, skip_if_modified_within_seconds)







def copy_content(source, destination):
    # 确保输出目标的目录存在，如果不存在则创建
    if not os.path.exists(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    try:
        # 检查 source 是否是目录
        if os.path.isdir(source):
            # 使用 copytree 来复制目录
            shutil.copytree(source, destination, dirs_exist_ok=True)  # 允许目录存在
        else:
            # 使用 copyfile 复制单个文件
            shutil.copyfile(source, destination)
    except Exception as e:
        # 如果复制失败，抛出异常
        raise RuntimeError(f"Failed to copy from '{source}' to '{destination}'. Reason: {str(e)}")








def append_file_content(file_a, file_b):
    # 读取文件 B 的内容
    with open(file_b, 'r', encoding='utf-8') as file:
        content_b = file.read()
    
    # 打开文件 A 并追加一个换行符和文件 B 的内容
    with open(file_a, 'a', encoding='utf-8') as file:
        file.write('\n')  # 总是先追加一个换行符
        file.write(content_b)  # 然后追加内容








def replace_lines_in_file(file_path, pattern, replacement, output_file=None):
    # 如果没有提供输出文件，则替换在原文件上进行
    if output_file is None:
        output_file = file_path
    
    # 读取原文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 对每行进行检查和替换
    new_lines = [re.sub(pattern, replacement, line) for line in lines]
    
    # 将修改后的内容写回到输出文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)








# 在指定文件后面添加内容
def copy_and_append(input_file, output_file, content_to_append):
    # 检查 input_file 是否存在
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"'{input_file}' does not exist.")
    # 创建 output_file 所在的目录
    os.makedirs(os.path.dirname(output_file), exist_ok=True) if os.path.dirname(output_file) else None
    # 尝试复制 input_file 到 output_file
    try:
        shutil.copyfile(input_file, output_file)
    except Exception as e:
        raise RuntimeError(f"Failed to copy from '{input_file}' to '{output_file}'. Reason: {str(e)}")
    # 在 output_file 末尾追加内容
    with open(output_file, 'a', encoding="utf-8") as f:
        f.write(content_to_append)








# 读取 yaml 中的 指定字段，输出单行格式
def single_line_yaml_format(input_file, output_file, key_path, force_single_line_for_lists=False):
    # 确保输出文件所在目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True) if os.path.dirname(output_file) else None
    # 读取源 YAML 文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    # 通过 '/' 分隔的多层键路径解析
    keys = key_path.split('/')
    content = data
    path_list = []
    for key in keys:
        if isinstance(content, dict) and key in content:
            path_list.append(key)
            content = content[key]
        else:
            content = None
            break
    # 确保找到数据后再进行处理
    if content is not None:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            # 写入嵌套键的每一级
            indent = 0
            for key in path_list:
                out_f.write('  ' * indent + f"{key}:\n")
                indent += 1
            if isinstance(content, dict):
                for key, value in content.items():
                    single_line = yaml.dump({key: value}, default_flow_style=True, width=float('inf'))
                    single_line = single_line.replace('\n', '').strip()[1:-1]
                    out_f.write('  ' * indent + f"{single_line}\n")
            elif isinstance(content, list):
                if force_single_line_for_lists:
                    single_line = yaml.dump(content, default_flow_style=True, width=float('inf'))
                    single_line = single_line.replace('\n', '').strip()
                    out_f.write('  ' * indent + f"{single_line}\n")
                else:
                    for item in content:
                        out_f.write('  ' * indent + f"- {item}\n")
    else:
        print(f"No content found for the path: {key_path}")









# 合并多个文件中的指定字段 input_files = [ "D:/agent/make.clash.config/aslib2/test/source.dler.yaml", "D:/agent/make.clash.config/aslib2/test/source.yaml" ]
# 辅助函数：深度合并两个字典
def deep_merge_dict(orig_dict, new_dict):
    for key, new_val in new_dict.items():
        if key in orig_dict and isinstance(orig_dict[key], dict) and isinstance(new_val, dict):
            deep_merge_dict(orig_dict[key], new_val)
        else:
            orig_dict[key] = new_val
def merge_yaml_sections(input_files, root_field, output_file, merge_dicts=True):
    # 初始化为字典或列表，取决于我们期待的合并类型
    merged_data = {}

    # 遍历所有输入文件
    for input_file in input_files:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = yaml.safe_load(file)  # 加载文件内容
            if root_field in content:
                field_data = content[root_field]
                if isinstance(field_data, dict):
                    # 合并字典类型的数据
                    for key, value in field_data.items():
                        if key in merged_data:
                            if isinstance(value, list) and isinstance(merged_data[key], list):
                                merged_data[key].extend(value)
                            elif merge_dicts and isinstance(merged_data[key], dict) and isinstance(value, dict):
                                deep_merge_dict(merged_data[key], value)
                            else:
                                merged_data[key] = value  # 默认覆盖
                        else:
                            merged_data[key] = value
                elif isinstance(field_data, list):
                    # 如果是列表，扩展或创建新列表
                    if isinstance(merged_data, list):
                        merged_data.extend(field_data)
                    else:
                        merged_data = field_data

    # 确保输出数据不是嵌套的 root_field
    if isinstance(merged_data, dict) and root_field in merged_data:
        output_data = {root_field: merged_data[root_field]}
    else:
        output_data = {root_field: merged_data}

    # 写入合并后的数据到输出文件
    with open(output_file, 'w', encoding='utf-8') as file:
        yaml.dump(output_data, file, allow_unicode=True)











# 对指定字段排序
def sort_section(data, field, rule_patterns):
    def get_sort_key(item):
        name = item.get(field, '')
        for i, pattern in enumerate(rule_patterns):
            if re.search(pattern, name):
                return i
        return len(rule_patterns)  # 没有匹配的放在最后
    return sorted(data, key=get_sort_key)
def sort_yaml_section(input_file, output_file, section, field, rule):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = yaml.safe_load(file)

    if section in content:
        rule_patterns = rule
        sorted_section = sort_section(content[section], field, rule_patterns)
        with open(output_file, 'w', encoding='utf-8') as file:
            yaml.dump({section: sorted_section}, file, allow_unicode=True)

