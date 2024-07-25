import os
import aslib.base_func as base_func
import aslib.country_groups as country_groups
import aslib.base_country_codes as base_country_codes

base_dir = os.path.dirname(os.path.abspath(__file__))
aslib_dir = os.path.join(base_dir, "aslib")



base_func.download_file('https://abc', os.path.join(base_dir, "tmp", "download", "config.dler.yaml"), 3600)
base_func.download_file('https://abc', os.path.join(base_dir, "tmp", "download", "config.dler.aa.yaml"), 3600)
base_func.download_file('https://abc', os.path.join(base_dir, "tmp", "download", "config.zhs.yaml"), 3600)
base_func.download_file('https://abc', os.path.join(base_dir, "tmp", "download", "config.aiboboxx.yaml"), 3600)
base_func.download_file('https://git.io/GeoLite2-Country.mmdb', os.path.join(base_dir, "tmp", "download", "Country.mmdb"), 3600)
base_func.download_file('https://git.io/GeoLite2-ASN.mmdb', os.path.join(base_dir, "tmp", "download", "ASN.mmdb"), 3600)
base_func.download_file('https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/direct.txt', os.path.join(base_dir, "tmp", "download", "dns.fakeip.filter.payload.yaml"), 3600)








# init
base_func.copy_content(os.path.join(aslib_dir, "base_config_router1.init.yaml"), os.path.join(base_dir, "tmp", "process", "config_router.yaml"))
# rules
base_func.append_file_content(os.path.join(base_dir, "tmp", "process", "config_router.yaml"), os.path.join(aslib_dir, "base_config_router4.rules.yaml"))
# providers
base_func.append_file_content(os.path.join(base_dir, "tmp", "process", "config_router.yaml"),os.path.join(aslib_dir, "base_config_router3.providers.yaml"))
# proxies
base_func.merge_yaml_sections([os.path.join(base_dir, "tmp", "download", "config.dler.aa.yaml")], 'proxies', os.path.join(base_dir, "tmp", "process", "config_router.proxies.yaml"))
sort_rules = ('新加坡', '泰国')
base_func.sort_yaml_section(os.path.join(base_dir, "tmp", "process", "config_router.proxies.yaml"), os.path.join(base_dir, "tmp", "process", "config_router.proxies.sort.yaml"), 'proxies', 'name', sort_rules)
base_func.single_line_yaml_format(os.path.join(base_dir, "tmp", "process", "config_router.proxies.sort.yaml"), os.path.join(base_dir, "tmp", "process", "config_router.proxies.sort.single.yaml"), "proxies")
base_func.append_file_content(os.path.join(base_dir, "tmp", "process", "config_router.yaml"), os.path.join(base_dir, "tmp", "process", "config_router.proxies.sort.single.yaml"))








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
names = country_groups.extract_field(os.path.join(base_dir, "tmp", "process", "config_router.yaml"), 'proxies', 'name')
classified = country_groups.classify_proxies_name(names,base_country_codes.country_codes,slice_rule=rules_for_extracting_country_names_from_node_names['dlercloud.com'])
country_groups.create_file_with_initial_content(os.path.join(base_dir, "tmp", "process", "config_router.country.json") + ".country.json", classified)
country_groups.write_classify_proxies_to_output(os.path.join(base_dir, "tmp", "process", "config_router.proxy_groups.yaml"), classified, sorting_rules_for_nodes_in_the_same_country['dlercloud.com'])








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
names = country_groups.extract_field(os.path.join(base_dir, "tmp", "process", "config_router.proxy_groups.yaml"), 'proxy-groups', 'name')
print(f"\n搜索到了国家: {names}")
country_groups.append_proxies_to_file(os.path.join(base_dir, "tmp", "process", "config_router.proxy_groups.yaml"), names, sort_keywords['common'], proxies_params_auto_url_test,'Auto_Url_Test')
country_groups.append_proxies_to_file(os.path.join(base_dir, "tmp", "process", "config_router.proxy_groups.yaml"), names, sort_keywords['proxy'], proxies_params_select,'PROXY')
country_groups.append_proxies_to_file(os.path.join(base_dir, "tmp", "process", "config_router.proxy_groups.yaml"), names, sort_keywords['proxy2'], proxies_params_select,'PROXY1')
country_groups.append_proxies_to_file(os.path.join(base_dir, "tmp", "process", "config_router.proxy_groups.yaml"), names, sort_keywords['common'], proxies_params_select,'PROXY2')
country_groups.append_proxies_to_file(os.path.join(base_dir, "tmp", "process", "config_router.proxy_groups.yaml"), names, sort_keywords['ChatGPT'], proxies_params_select_app,'ChatGPT')
country_groups.append_proxies_to_file(os.path.join(base_dir, "tmp", "process", "config_router.proxy_groups.yaml"), names, sort_keywords['AdBlock'], proxies_params_select_ad,'AdBlock')
country_groups.append_proxies_to_file(os.path.join(base_dir, "tmp", "process", "config_router.proxy_groups.yaml"), names, sort_keywords['dev'], proxies_params_select_app,'dev')
country_groups.append_proxies_to_file(os.path.join(base_dir, "tmp", "process", "config_router.proxy_groups.yaml"), names, sort_keywords['IPtest'], proxies_params_select_app,'IPtest')








# proxy_groups 排序 合并
sort_rules = (r'PROXY', r'PROXY2', r'^([a-zA-Z])')
base_func.sort_yaml_section(os.path.join(base_dir, "tmp", "process", "config_router.proxy_groups.yaml"), os.path.join(base_dir, "tmp", "process", "config_router.proxy_groups.sort.yaml"), 'proxy-groups', 'name', sort_rules)
base_func.single_line_yaml_format(os.path.join(base_dir, "tmp", "process", "config_router.proxy_groups.sort.yaml"), os.path.join(base_dir, "tmp", "process", "config_router.proxy_groups.sort.single.yaml"), "proxy-groups")
base_func.append_file_content(os.path.join(base_dir, "tmp", "process", "config_router.yaml"), os.path.join(base_dir, "tmp", "process", "config_router.proxy_groups.sort.single.yaml"))








# dns
# base_func.replace_lines_in_file(os.path.join(base_dir, "tmp", "download", "dns.fakeip.filter.payload.yaml"), r"payload:","dns:\n  fake-ip-filter:\n")
# base_func.merge_yaml_sections([os.path.join(aslib_dir, "base_config_router2.dns.yaml"), os.path.join(base_dir, "tmp", "download", "dns.fakeip.filter.payload.yaml")], 'dns', os.path.join(base_dir, "tmp", "process", "config_router.dns.yaml"))
# base_func.single_line_yaml_format(os.path.join(base_dir, "tmp", "process", "config_router.dns.yaml"), os.path.join(base_dir, "tmp", "process", "config_router.dns.single.yaml"), "dns", True)
base_func.append_file_content(os.path.join(base_dir, "tmp", "process", "config_router.yaml"), os.path.join(aslib_dir, "base_config_router2.dns.yaml"))








# download providers
base_func.download_providers_from_yaml_file(os.path.join(base_dir, "tmp", "process", "config_router.yaml"), os.path.join(base_dir, "tmp", "download"), 3600)








# 发布
base_func.copy_content(os.path.join(base_dir, "tmp", "process", "config_router.yaml"), os.path.join(base_dir, "tmp.output.router", "config.yaml"))
base_func.copy_content(os.path.join(base_dir, "tmp", "download", "Country.mmdb"), os.path.join(base_dir, "tmp.output.router", "Country.mmdb"))
base_func.copy_content(os.path.join(base_dir, "tmp", "download", "ASN.mmdb"), os.path.join(base_dir, "tmp.output.router", "ASN.mmdb"))
base_func.copy_content(os.path.join(base_dir, "tmp", "download", "ruleset"), os.path.join(base_dir, "tmp.output.router", "ruleset"))
# base_func.replace_lines_in_file(os.path.join(base_dir, "tmp.output.router", "ruleset","openai.yaml"), r'\s+-\s+IP-ASN.*',"")
