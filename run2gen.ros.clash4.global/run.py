import os
import sys
import subprocess
import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from aslib import base_func
from aslib import country_groups
from aslib import base_country_codes
import env_local


base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir_output = os.path.join(base_dir, "output")
base_dir_output_bak = os.path.join(base_dir, "output", "bak." + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
base_dir_output_archive = os.path.join(base_dir, "output", "archive")
base_dir_output_download = os.path.join(base_dir, "output", "download")
base_dir_output_download_configyaml = os.path.join(base_dir, "output", "download", "config.yaml")
base_dir_output_download_countrydb = os.path.join(base_dir, "output", "download", "Country.mmdb")
base_dir_output_download_asndb = os.path.join(base_dir, "output", "download", "ASN.mmdb")
base_dir_output_download_ui_assetszip = os.path.join(base_dir, "output", "download", "ui.zip")
base_dir_output_process = os.path.join(base_dir, "output", "process")
base_dir_output_process_configyaml = os.path.join(base_dir, "output", "config.yaml")

yaml1_init = os.path.join(base_dir, "config1.init.yaml")
yaml2_dns = os.path.join(base_dir, "config2.dns.yaml")
yaml3_providers = os.path.join(base_dir, "config3.providers.yaml")
yaml4_rules = os.path.join(base_dir, "config4.rules.yaml")












try:
    base_func.download_file(env_local.config_yaml, base_dir_output_download_configyaml, 3600)
    # base_func.download_file(env_local.config_dler_aa, os.path.join(base_dir_output_download, "config.dler.aa.yaml"), 3600)
    # base_func.download_file(env_local.config_zhs, os.path.join(base_dir_output_download, "config.zhs.yaml"), 3600)
    # base_func.download_file(env_local.config_aiboboxx, os.path.join(base_dir_output_download, "config.aiboboxx.yaml"), 3600)
    base_func.download_file(env_local.config_countrydb, base_dir_output_download_countrydb, 3600)
    base_func.download_file(env_local.config_asndb, base_dir_output_download_asndb, 3600)
    # base_func.download_file('https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/direct.txt', os.path.join(base_dir_output_download, "dns.fakeip.filter.payload.yaml"), 3600)
    base_func.download_file(env_local.config_ui_assets, base_dir_output_download_ui_assetszip, 3600)







    # init
    base_func.copy_content(yaml1_init, base_dir_output_process_configyaml)
    # rules
    base_func.append_file_content(base_dir_output_process_configyaml, yaml4_rules)
    # providers
    base_func.append_file_content(base_dir_output_process_configyaml, yaml3_providers)
    # proxies
    base_func.merge_yaml_sections([base_dir_output_download_configyaml], 'proxies', os.path.join(base_dir_output_process, "config.proxies.yaml"))
    sort_rules = ('新加坡', '泰国')
    base_func.sort_yaml_section(os.path.join(base_dir_output_process, "config.proxies.yaml"), os.path.join(base_dir_output_process, "config.proxies.sort.yaml"), 'proxies', 'name', sort_rules)
    base_func.single_line_yaml_format(os.path.join(base_dir_output_process, "config.proxies.sort.yaml"), os.path.join(base_dir_output_process, "config.proxies.sort.single.yaml"), "proxies")
    base_func.append_file_content(base_dir_output_process_configyaml, os.path.join(base_dir_output_process, "config.proxies.sort.single.yaml"))








    # proxy_groups 国家组
    #用于分割节点名称的规则,提取国家代码，例如提取： name: '🇵🇭 菲律宾 IEPL [03] [Air]',  中的 菲律宾
    rules_for_extracting_country_names_from_node_names = {
        'zhs.ooo': ('.', 2),
        'zhs.ooo.2': (3, 5),
        'zhs.ooo.3': ('.', 2),
        'zhs.ooo.4': (3, '/'),
        'dlercloud.com': (' ', ' '),
        'dlercloud.com.2': (3, ' '),
        'github.aiboboxx': (0, 2),
        # Add more rules as needed...
    }
    #定义节点排序的关键字
    sorting_rules_for_nodes_in_the_same_country = {
        'zhs.ooo': (r'❿.*x1', r'❾.*x1', r'❽.*x1', r'❼.*x1', r'❻.*x1', r'❺.*x1',r'❹.*x1',r'❸.*x1',r'❸.*x1',r'❶.*x1',r'❸.*x1.5',r'❸.*x1.5',r'❶.*x1.5',r'❸.*x2',r'❸.*x2',r'❶.*x2',),
        'zhs.ooo.2': ('ghi', 'jkl',),
        'dlercloud.com': (r'(AC)', r'IEPL\s+\[\d+\]\s+\[Ultra\]', r'IEPL\s+\[\d+\]\s+\[Premium\]', r'IEPL\s+\[\d+\]\s+\[Std\]', r'IEPL\s+\[\d+\]\s+\[Lite\]', r'(DMIT|Aliyun|BBTEC|GIA)', r'(EDGE)',),
        'dlercloud.com.2': (r'IEPL\s+\[\d+\]\s+\[Premium\]', r'(AC)', r'IEPL\s+\[\d+\]\s+\[Std\]', r'IEPL\s+\[\d+\]\s+\[Lite\]', r'(DMIT|Aliyun|BBTEC|GIA)', r'(EDGE)',),
        'github.aiboboxx': (' ',),
        'url_est': (r'([一-龥]+)',),  #表示匹配汉字：[一-龥]
        # Add more rules as needed...
    }
    names = country_groups.extract_field(base_dir_output_process_configyaml, 'proxies', 'name')
    classified = country_groups.classify_proxies_name(names,base_country_codes.country_codes,slice_rule=rules_for_extracting_country_names_from_node_names['dlercloud.com'])
    country_groups.create_file_with_initial_content(os.path.join(base_dir_output_process, "config.country.json") + ".country.json", classified)
    country_groups.write_classify_proxies_to_output(os.path.join(base_dir_output_process, "config.proxy_groups.yaml"), classified, sorting_rules_for_nodes_in_the_same_country['dlercloud.com'])








    # proxy_groups 自定义组
    #定义节点排序的关键字
    sort_keywords = {
        'url_est': (r'([一-龥]+)',),  #表示匹配汉字：[一-龥]
        'common': (r'(Auto_Url_Test)',r'([a-zA-Z])',r'(香港)',r'(新加坡)',r'(美国)',r'(韩国)',r'(台湾)',r'(日本)',),
        'aggregation1': (r'(Auto_Url_Test)',r'([a-zA-Z])',r'(新加坡.*dlercloud)',r'(香港.*dlercloud)',r'(台湾.*dlercloud)',r'(日本.*dlercloud)',r'(美国.*dlercloud)',r'(韩国.*dlercloud)',),
        'proxy': (r'(新加坡)',),
        'proxy1': (r'(韩国)',),
        'proxy2': (r'(美国)',),
        'proxy3': (r'(日本)',),
        'ChatGPT': (r'(新加坡)',r'(韩国)',r'(日本)',r'(美国)'),
        'AdBlock': (r'(REJECT)',),
        'dev': (r'(DIRECT)',),
        'IPtest': (r'(DIRECT)',),
        # Add more rules as needed...
    }
    #添加url-test类型代理组
    proxies_params_auto_url_test = {
        'name': 'Auto_Url_Test',
        'type': 'url-test',
        'url': 'http://cp.cloudflare.com/generate_204',
        'interval': 3600,
        'proxies': [],
    }
    #添加select类型代理组
    proxies_params_select = {
        'name': 'Proxy',
        'type': 'select',
        'proxies': ["Auto_Url_Test", "DIRECT"],   #请自行注意 Auto_Url_Test 代理是否添加且名字匹配
    }
    #添加select类型代理组-选择应用
    proxies_params_select_app = {
        'name': 'app',
        'type': 'select',
        'proxies': ["PROXY", "PROXY1", "PROXY2", "Auto_Url_Test", "DIRECT"],   #请自行注意 PROXY PROXY1 PROXY2…… 代理是否添加且名字匹配
    }
    #添加select类型代理组-选择应用
    proxies_params_select_ad = {
        'name': 'AdBlock',
        'type': 'select',
        'proxies': ["Auto_Url_Test", "REJECT", "DIRECT", "PROXY1", "PROXY2"],   #请自行注意 PROXY PROXY1 PROXY2…… 代理是否添加且名字匹配
    }
    #添加 中继（套娃）类型代理组-选择应用
    proxies_params_relay_ai = {
    # relay chains the proxies. proxies shall not contain a relay. No UDP support.
    # Traffic: clash <-> http <-> vmess <-> ss1 <-> ss2 <-> Internet
        'name': 'relay',
        'type': 'relay',
        'proxies':["REJECT", "DIRECT", "Auto_Url_Test", "PROXY1", "PROXY2"],
    }
    names = country_groups.extract_field(os.path.join(base_dir_output_process, "config.proxy_groups.yaml"), 'proxy-groups', 'name')
    print(f"\n搜索到了国家: {names}")
    country_groups.append_proxies_to_file(os.path.join(base_dir_output_process, "config.proxy_groups.yaml"), names, sort_keywords['common'], proxies_params_auto_url_test,'Auto_Url_Test')
    country_groups.append_proxies_to_file(os.path.join(base_dir_output_process, "config.proxy_groups.yaml"), names, sort_keywords['proxy'], proxies_params_select,'PROXY')
    country_groups.append_proxies_to_file(os.path.join(base_dir_output_process, "config.proxy_groups.yaml"), names, sort_keywords['proxy2'], proxies_params_select,'PROXY1')
    country_groups.append_proxies_to_file(os.path.join(base_dir_output_process, "config.proxy_groups.yaml"), names, sort_keywords['common'], proxies_params_select,'PROXY2')
    country_groups.append_proxies_to_file(os.path.join(base_dir_output_process, "config.proxy_groups.yaml"), names, sort_keywords['ChatGPT'], proxies_params_select_app,'ChatGPT')
    country_groups.append_proxies_to_file(os.path.join(base_dir_output_process, "config.proxy_groups.yaml"), names, sort_keywords['AdBlock'], proxies_params_select_ad,'AdBlock')
    country_groups.append_proxies_to_file(os.path.join(base_dir_output_process, "config.proxy_groups.yaml"), names, sort_keywords['dev'], proxies_params_select_app,'dev')
    country_groups.append_proxies_to_file(os.path.join(base_dir_output_process, "config.proxy_groups.yaml"), names, sort_keywords['IPtest'], proxies_params_select_app,'IPtest')








    # proxy_groups 排序 合并
    sort_rules = (r'PROXY', r'PROXY2', r'^([a-zA-Z])')
    base_func.sort_yaml_section(os.path.join(base_dir_output_process, "config.proxy_groups.yaml"), os.path.join(base_dir_output_process, "config.proxy_groups.sort.yaml"), 'proxy-groups', 'name', sort_rules)
    base_func.single_line_yaml_format(os.path.join(base_dir_output_process, "config.proxy_groups.sort.yaml"), os.path.join(base_dir_output_process, "config.proxy_groups.sort.single.yaml"), "proxy-groups")
    base_func.append_file_content(base_dir_output_process_configyaml, os.path.join(base_dir_output_process, "config.proxy_groups.sort.single.yaml"))








    # dns
    # base_func.replace_lines_in_file(os.path.join(base_dir_output_download, "dns.fakeip.filter.payload.yaml"), r"payload:","dns:\n  fake-ip-filter:\n")
    # base_func.merge_yaml_sections([yaml2_dns, os.path.join(base_dir_output_download, "dns.fakeip.filter.payload.yaml")], 'dns', os.path.join(base_dir_output_process, "config.dns.yaml"))
    # base_func.single_line_yaml_format(os.path.join(base_dir_output_process, "config.dns.yaml"), os.path.join(base_dir_output_process, "config.dns.single.yaml"), "dns", True)
    base_func.append_file_content(base_dir_output_process_configyaml, yaml2_dns)








    # download providers
    base_func.download_providers_from_yaml_file(base_dir_output_process_configyaml, os.path.join(base_dir_output_download), 3600)







    # 单独处理配置文件行
    # base_func.replace_lines_in_file(os.path.join(base_dir_output_archive, "ruleset","openai.yaml"), r'\s+-\s+IP-ASN.*',"")








    # 归档
    base_func.copy_content(base_dir_output_process_configyaml, os.path.join(base_dir_output_archive, "config.yaml"))
    base_func.copy_content(base_dir_output_download_countrydb, os.path.join(base_dir_output_archive, "Country.mmdb"))
    base_func.copy_content(base_dir_output_download_asndb, os.path.join(base_dir_output_archive, "ASN.mmdb"))
    base_func.unzip_and_rename(base_dir_output_download_ui_assetszip, base_dir_output_archive)
    base_func.copy_content(os.path.join(base_dir_output_download, "ruleset"), os.path.join(base_dir_output_archive, "ruleset"))






    # 发布
    subprocess.run(f"scp -oStrictHostKeyChecking=no -r -P {env_local.cmd_port} {env_local.cmd_rls_dir}                       {base_dir_output_bak}",   check=True, shell=True)
    # subprocess.run(f"ssh -oStrictHostKeyChecking=no -n -p {env_local.cmd_port} {env_local.cmd_ssh_dst} mkdir -p              {env_local.cmd_rls_dir}",   check=True, shell=True)
    subprocess.run(f"scp -oStrictHostKeyChecking=no -r -P {env_local.cmd_port} {os.path.join(base_dir_output_archive, "*")}  {env_local.cmd_rls_dir}", check=True, shell=True)







except Exception as e:
    print(f"Error during script execution: {e}")
    # 处理错误，如退出脚本或尝试重新执行