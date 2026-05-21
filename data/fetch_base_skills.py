import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import quote

def fetch_operator_base_skills(operator_name):
    """从 PRTS Wiki 获取单个干员的后勤技能"""
    base_url = "https://prts.wiki/w/"
    url = f"{base_url}{quote(operator_name)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找"后勤技能"标题
        logistics_header = soup.find('span', {'id': '后勤技能'})
        if not logistics_header:
            logistics_header = soup.find('span', {'id': '.E5.90.8E.E5.8B.A4.E6.8A.80.E8.83.BD'})
        
        if not logistics_header:
            return []
        
        # 获取后勤技能标题后的所有表格
        skills = []
        current = logistics_header.find_parent('h2')
        if not current:
            return []
        
        # 遍历 h2 之后的兄弟元素，直到下一个 h2
        for sibling in current.find_next_siblings():
            if sibling.name == 'h2':
                break
            if sibling.name == 'table' and 'wikitable' in sibling.get('class', []):
                rows = sibling.find_all('tr')
                if len(rows) < 2:
                    continue
                
                # 解析数据行
                for row in rows[1:]:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) < 4:
                        continue
                    
                    cell_texts = [cell.get_text(strip=True) for cell in cells]
                    
                    if len(cell_texts) >= 5:
                        skill = {
                            'condition': cell_texts[0],
                            'skill_name': cell_texts[2],
                            'room': cell_texts[3],
                            'description': cell_texts[4]
                        }
                        skills.append(skill)
                    elif len(cell_texts) >= 4:
                        skill = {
                            'condition': cell_texts[0],
                            'skill_name': cell_texts[1],
                            'room': cell_texts[2],
                            'description': cell_texts[3]
                        }
                        skills.append(skill)
        
        return skills
        
    except Exception as e:
        print(f"  [{operator_name}] 错误: {str(e)}")
        return None


def main():
    # 读取干员列表
    with open('/Users/altria/Documents/code/arkproject/base-calculator/data/operators.txt', 'r', encoding='utf-8') as f:
        operators = [line.strip() for line in f if line.strip()]
    
    # 进度文件路径
    progress_file = '/Users/altria/Documents/code/arkproject/base-calculator/data/base_skills_progress.json'
    output_file = '/Users/altria/Documents/code/arkproject/base-calculator/data/base_skills.json'
    
    # 加载已有进度
    all_skills = {}
    processed = set()
    if os.path.exists(progress_file):
        with open(progress_file, 'r', encoding='utf-8') as f:
            all_skills = json.load(f)
        processed = set(all_skills.keys())
        print(f"已加载进度: {len(processed)} 个干员已处理")
    
    failed = []
    no_skills = []
    
    # 只处理未处理的干员
    remaining = [op for op in operators if op not in processed]
    print(f"共 {len(operators)} 个干员，剩余 {len(remaining)} 个待处理")
    print(f"预计需要 {len(remaining) * 0.8 / 60:.1f} 分钟")
    print("=" * 50)
    
    for i, operator in enumerate(remaining):
        print(f"[{len(processed)+i+1}/{len(operators)}] {operator}", end=" ")
        
        skills = fetch_operator_base_skills(operator)
        
        if skills is None:
            failed.append(operator)
            print("- 失败")
        elif len(skills) > 0:
            all_skills[operator] = skills
            print(f"- {len(skills)} 个技能")
        else:
            no_skills.append(operator)
            print("- 无技能")
        
        # 每处理 10 个保存一次进度
        if (i + 1) % 10 == 0:
            with open(progress_file, 'w', encoding='utf-8') as f:
                json.dump(all_skills, f, ensure_ascii=False, indent=2)
            print(f"  [已保存进度]")
        
        time.sleep(0.8)
    
    # 最终保存
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_skills, f, ensure_ascii=False, indent=2)
    
    # 清理进度文件
    if os.path.exists(progress_file):
        os.remove(progress_file)
    
    print(f"\n{'=' * 50}")
    print(f"结果已保存到: {output_file}")
    print(f"成功获取: {len(all_skills)} 个干员的后勤技能")
    print(f"无后勤技能: {len(no_skills)} 个")
    print(f"请求失败: {len(failed)} 个")
    
    if failed:
        print(f"失败的干员: {', '.join(failed[:10])}{'...' if len(failed) > 10 else ''}")


if __name__ == "__main__":
    main()
