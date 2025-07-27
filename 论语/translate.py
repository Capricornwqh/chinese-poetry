import os
import json
from opencc import OpenCC

def convert_to_markdown(poem):
    try:
        lines = [] 
        lines.append(f"# {poem['chapter']}\n")
        lines.append(f"**朝代**\n")
        lines.append(f"{poem['dynasty']}\n")
        lines.append(f"**内容**\n")
        for paragraph in poem['paragraphs']:
            lines.append(f"{paragraph}\n")
        return "".join(lines)
    except KeyError as e:
        print(f"警告：诗歌数据格式错误 - 缺少字段 {e}")
        return None
    
def process_poetry_files(poetry_dir, output_dir):
    cc = OpenCC('t2s')
    os.makedirs(output_dir, exist_ok=True)
    
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
                    try:
                        # 转换繁体到简体
                        poem['chapter'] = cc.convert(poem['chapter'])
                        poem['paragraphs'] = [cc.convert(p) for p in poem['paragraphs']]
                        poem['dynasty'] = '春秋'
                        
                        markdown_content = convert_to_markdown(poem)
                        if markdown_content:
                            f.write(markdown_content)
                            f.write("\n\n")
                            processed_count += 1
                    except Exception as e:
                        print(f"警告：处理诗歌失败，错误: {str(e)}")
                
                print(f"已完成文件 {file} 的处理，成功转换 {processed_count} 首诗")

        except Exception as e:
            print(f"错误：处理文件 {file} 失败 - {str(e)}")
            continue

def main():
    poetry_dir = '/home/wqh/projects/ChinesePoetry/论语'
    output_dir = '/home/wqh/projects/ChinesePoetry/output'
    
    process_poetry_files(poetry_dir, output_dir)

if __name__ == '__main__':
    main()