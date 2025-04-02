import os
import json
from opencc import OpenCC

def convert_to_markdown(poem):
    try:
        lines = [] 
        lines.append(f"# {poem['title']}\n")
        lines.append(f"**作者**\n")
        lines.append(f"{poem['author']}\n")
        lines.append(f"**朝代**\n")
        lines.append(f"{poem['dynasty']}\n")
        lines.append(f"**内容**\n")
        for paragraph in poem['paragraphs']:
            lines.append(f"{paragraph}\n")
        lines.append(f"**声韵**\n")
        if isinstance(poem['strains'], list):
            for i, strain in enumerate(poem['strains']):
                if isinstance(strain, dict):
                    lines.append(f"{strain.get('line', '')}: {strain.get('strains', '')}\n")
                else:
                    lines.append(f"{strain}\n")
        # lines.append(f"\n**字数**：\n")
        # lines.append(f"{sum(len(p) for p in poem['paragraphs'])}\n")
        # lines.append(f"\n**句数**：\n")
        # lines.append(f"{len(poem['paragraphs'])}\n")

        return "".join(lines)
    except KeyError as e:
        print(f"警告：诗歌数据格式错误 - 缺少字段 {e}")
        return None

def process_poetry_files(poetry_dir, strains_dir, output_dir):
    cc = OpenCC('t2s')
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取所有平仄数据
    print("正在加载平仄数据...")
    strains_data = {}
    strain_files = [f for f in os.listdir(strains_dir) if f.endswith('.json')]
    for file in strain_files:
        try:
            with open(os.path.join(strains_dir, file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    strains_data[item['id']] = item['strains']
        except json.JSONDecodeError:
            print(f"警告：平仄文件解析失败 - {file}")
            continue
    
    # 处理诗歌文件
    print("正在处理诗歌文件...")
    poetry_files = [f for f in os.listdir(poetry_dir) if f.endswith('.json')]
    for file in poetry_files:
        output_file = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.md")
        
        try:
            with open(os.path.join(poetry_dir, file), 'r', encoding='utf-8') as f:
                poetry_data = json.load(f)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                processed_count = 0
                for poem in poetry_data:
                    if poem['id'] in strains_data:
                        try:
                            # 转换繁体到简体
                            poem['title'] = cc.convert(poem['title'])
                            poem['author'] = cc.convert(poem['author'])
                            poem['paragraphs'] = [cc.convert(p) for p in poem['paragraphs']]
                            poem['strains'] = strains_data[poem['id']]
                            poem['dynasty'] = ''
                            if 'tang' in file.lower():
                                poem['dynasty'] = '唐朝'
                            elif 'song' in file.lower():
                                poem['dynasty'] = '宋朝'
                            
                            
                            markdown_content = convert_to_markdown(poem)
                            if markdown_content:
                                f.write(markdown_content)
                                f.write("\n\n")
                                processed_count += 1
                        except Exception as e:
                            print(f"警告：处理诗歌失败 - ID: {poem.get('id', 'unknown')}, 错误: {str(e)}")
                
                print(f"已完成文件 {file} 的处理，成功转换 {processed_count} 首诗")
                break

        except Exception as e:
            print(f"错误：处理文件 {file} 失败 - {str(e)}")
            continue

def main():
    poetry_dir = '/home/wqh/projects/ChinesePoetry/全唐诗'
    strains_dir = '/home/wqh/projects/ChinesePoetry/strains/json'
    output_dir = '/home/wqh/projects/ChinesePoetry/output'
    
    process_poetry_files(poetry_dir, strains_dir, output_dir)

if __name__ == '__main__':
    main()