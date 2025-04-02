# pip install python-dotenv lxml requests bs4 PyGitHub

import datetime
import os
import subprocess
import sys

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from github import Github

GIT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = 'www.kundabc.com'
SITEMAP_URL = 'http://www.kundabc.com/sitemap.xml'

TOP_BANNER = f'''<p align="center">\n![关注公众号](https://zhangpingguo.com/spider/fetchImage?url=https%3A%2F%2Fmmbiz.qpic.cn%2Fsz_mmbiz_png%2FkswPKia3kOHcYbKh1Z8riaT9xNbzUOdoYYbYzG81KoPmEYnQwd6ZTicND1RCZiaza2BOnWHGWHc50pC5jhjPQYQnbg%2F640%3Fwx_fmt%3Dpng%26from%3Dappmsg)\n</p>\n'''
TOP_CONTENT = f'''上海源瑞科细胞生物技术（以下简称“源瑞科”）是“产、学、研、医、服”一体化综合服务平台，聚焦干细胞科技存储、制备与应用，由长江学者、复旦大学教授带领，依托19项专利，与上海市东方医院构建稳定的战略合作关系，“持续用科技激活生命力”。\n<p align="center">\n![科研工作团队](https://zhangpingguo.com/spider/fetchImage?url=https%3A%2F%2Fmmbiz.qpic.cn%2Fsz_mmbiz_png%2FicBFYZ6XyUaY4DwDkK59DbzyBNApqBdqocTWI4DHcLGPs8QzrmcwD42lew0nkkSL07iaaIrZFfhu7OsJmWSzu0GA%2F640%3Fwx_fmt%3Dpng%26from%3Dappmsg)\n</p>\n源瑞科拥有一支由行业专家和学者组成的精英团队，与上海市东方医院（南院）、中源协和等平台建立战略合作，致力于推动人体干细胞技术和细胞技术的研发与应用。凭借在细胞生物技术领域的深厚积累，以及对医疗健康产业的敏锐洞察，源瑞科用干细胞研究前沿成果，为患者提供了全新的“标本兼治”的治疗策略：不仅缓解疼痛，还能从根本上修复受损细胞，恢复组织器官功能，改善患者生理感受，助力众多临床患者有效控制病程、延缓病情、修复治愈。\n<p align="center">\n![实验室走廊](https://zhangpingguo.com/spider/fetchImage?url=https%3A%2F%2Fmmbiz.qpic.cn%2Fsz_mmbiz_jpg%2FicBFYZ6XyUaY4DwDkK59DbzyBNApqBdqopDhGaYOwicFxX4t85A7z3l7ndhGanibPa1Y92ZUqCv1MmTq1eV7IiahyQ%2F640%3Fwx_fmt%3Djpeg%26from%3Dappmsg)\n</p>\n<hr/>\n'''
BOTTOM_CONTENT = f'''\n<p align="center">\n![关注公众号](https://zhangpingguo.com/spider/fetchImage?url=https%3A%2F%2Fmmbiz.qpic.cn%2Fsz_mmbiz_png%2FkswPKia3kOHcYbKh1Z8riaT9xNbzUOdoYYbYzG81KoPmEYnQwd6ZTicND1RCZiaza2BOnWHGWHc50pC5jhjPQYQnbg%2F640%3Fwx_fmt%3Dpng%26from%3Dappmsg)\n</p>\n'''
BOTTOM__BANNER = f'''\n<p align="center">\n![关注公众号](https://zhangpingguo.com/spider/fetchImage?url=https%3A%2F%2Fmmbiz.qpic.cn%2Fsz_mmbiz_png%2FkswPKia3kOHcYbKh1Z8riaT9xNbzUOdoYYbYzG81KoPmEYnQwd6ZTicND1RCZiaza2BOnWHGWHc50pC5jhjPQYQnbg%2F640%3Fwx_fmt%3Dpng%26from%3Dappmsg)\n</p>\n'''


def main():
    
    try:
        # 获取并解析sitemap（强制utf-8编码）
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(SITEMAP_URL, headers=headers, allow_redirects=True)
        # response.raise_for_status()  # 检查请求是否成功
        s = response.content.decode('utf-8')
        soup = BeautifulSoup(s, 'xml')
        urls = soup.find_all('url')
        
        today = datetime.date.today().isoformat()
        articles = []
        for url in urls:
            loc = url.find('loc').text
            lastmod = url.find('lastmod').text[:10] if url.find('lastmod') else ''
            if lastmod.startswith(today):
                image_tag = url.find('image:image')
                title = image_tag.find('image:title').text.strip() if image_tag else '无标题'
                articles.append({'title': title, 'loc': loc, 'date': lastmod})
        
        if not articles:
            print("今日无新文章。")
            return
        
        # 保存当天文章（按年/月/日分类）
        year, month, day = today.split('-')
        dir_path = f"{year}/{month}"
        os.makedirs(dir_path, exist_ok=True)
        with open(f"{dir_path}/{today}.md", "w", encoding="utf-8") as f:
            f.write(f"# {today} 文章\n\n")
            for a in articles:
                f.write(f"- [{a['title']}]({a['loc']})\n")
        
        # 更新README（强制utf-8读写）
        all_articles = []
        for root, _, files in os.walk("."):
            for file in files:
                if file.endswith(".md") and file != "README.md":
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        lines = f.read().splitlines()
                        for line in lines:
                            if line.startswith("- ["):
                                parts = line.split("](")
                                title = parts[0][3:]
                                link = parts[1].split(")")[0]
                                date = file.split(".")[0]
                                all_articles.append({'title': title, 'loc': link, 'date': date})
        all_articles.sort(key=lambda x: x['date'], reverse=True)
        
        # 生成README内容（按年-月-日分组）
        readme = "\n## 最新10篇\n\n"
        for a in all_articles[:10]:
            readme += f"- [{a['title']}]({a['loc']}) | {a['date']}\n"
        readme += "\n## 按日期分类\n\n"
        
        # 按年-月分组，再按日显示
        date_dict = {}
        for a in all_articles:
            key = a['date']  # 完整日期作为键
            year_month = a['date'][:7]
            if year_month not in date_dict:
                date_dict[year_month] = {}
            if key not in date_dict[year_month]:
                date_dict[year_month][key] = []
            date_dict[year_month][key].append(a)
        
        # 生成树形结构（年-月 -> 日 -> 文章）
        for year_month in sorted(date_dict.keys(), reverse=True):
            readme += f"### {year_month}\n"
            for date_key in sorted(date_dict[year_month].keys(), reverse=True):
                readme += f"#### {date_key}\n"
                for a in date_dict[year_month][date_key]:
                    readme += f"- [{a['title']}]({a['loc']})\n"
                readme += "\n"
            readme += "\n"
        
        # 写入README（强制utf-8编码）
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(f'{TOP_BANNER}{TOP_CONTENT}{readme}{BOTTOM_CONTENT}{BOTTOM__BANNER}')
        
        # 提交到GitHub（使用 `git -C` 参数）
        subprocess.run(["git", "-C", GIT_DIR, "add", "-A"])
        subprocess.run(["git", "-C", GIT_DIR, "commit", "-m", "Auto update"])
        subprocess.run(["git", "-C", GIT_DIR, "push", "origin", "main"])
        print(f"更新成功：{today}.md 和 README.md")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()