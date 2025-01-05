import os
import re

# 将 Markdown 文件中的图片链接中的反斜杠替换为正斜杠
def replace_backslashes_in_md(md_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 正则匹配图片链接（支持 Markdown 格式的 ![]() 和 HTML <img> 标签）
    markdown_image_pattern = r'!\[.*?\]\((.*?)\)'
    html_image_pattern = r'<img\s+[^>]*src=["\'](.*?)["\'][^>]*>'

    # 替换 Markdown 图片链接中的反斜杠
    content = re.sub(markdown_image_pattern, lambda match: replace_backslashes(match.group(0)), content)
    # 替换 HTML 图片标签中的反斜杠
    content = re.sub(html_image_pattern, lambda match: replace_backslashes(match.group(0)), content)

    # 将修改后的内容写回文件
    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated: {md_file_path}")

# 替换链接中的反斜杠为正斜杠
def replace_backslashes(link):
    # 只替换链接中的反斜杠为正斜杠
    return link.replace('\\', '/')

# 处理指定文件夹中的所有 Markdown 文件
def process_md_files_in_folder(root_folder):
    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            # 只处理 .md 文件
            if file.endswith('.md'):
                md_file_path = os.path.join(root, file)
                replace_backslashes_in_md(md_file_path)

if __name__ == "__main__":
    # 设置目标文件夹路径
    target_folder = './'  # 替换为你的目标文件夹路径

    # 处理目标文件夹中的所有 Markdown 文件
    process_md_files_in_folder(target_folder)
