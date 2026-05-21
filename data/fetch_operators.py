import requests
from bs4 import BeautifulSoup
import json
import re

def fetch_all_operators():
    """
    从 PRTS Wiki 获取所有干员名称（按星级分类）
    """
    url = "https://prts.wiki/w/CHAR"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"正在请求: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        return {}
    
    # 使用正则表达式提取所有 data-zh 属性的值
    html_content = response.text
    pattern = r'data-zh="([^"]*)"'
    matches = re.findall(pattern, html_content)
    
    # 去重并保持顺序
    seen = set()
    operators = []
    for name in matches:
        if name and name not in seen:
            seen.add(name)
            operators.append(name)
    
    print(f"找到 {len(operators)} 个干员")
    
    # 保存为 JSON 文件
    output_path = "/Users/altria/Documents/code/arkproject/base-calculator/data/operators.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(operators, f, ensure_ascii=False, indent=2)
    
    print(f"干员列表已保存到: {output_path}")
    
    # 同时保存为文本文件，每行一个干员
    txt_path = "/Users/altria/Documents/code/arkproject/base-calculator/data/operators.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        for op in operators:
            f.write(op + '\n')
    
    print(f"干员列表已保存到: {txt_path}")
    
    # 打印前 30 个干员
    print("\n前 30 个干员:")
    for op in operators[:30]:
        print(f"  - {op}")
    
    return operators

if __name__ == "__main__":
    operators = fetch_all_operators()
    print(f"\n总共获取到 {len(operators)} 个干员")
