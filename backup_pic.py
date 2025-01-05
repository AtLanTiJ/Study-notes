import os
import re
import requests
import uuid
from urllib.parse import urlparse
from pathlib import Path

# 下载图片并返回保存的本地路径
def download_image(image_url, save_folder):
    # 随机生成图片文件名，并保留原始扩展名
    parsed_url = urlparse(image_url)
    original_extension = os.path.splitext(parsed_url.path)[-1]  # 获取文件扩展名
    if not original_extension:  # 如果没有扩展名，默认用 .jpg
        original_extension = ".jpg"
    random_name = f"{uuid.uuid4().hex}{original_extension}"  # 生成随机文件名

    # 构建保存图片的完整路径
    save_path = os.path.join(save_folder, random_name)

    # 下载图片
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {image_url} -> {save_path}")
        return save_path
    except Exception as e:
        print(f"Failed to download {image_url}: {e}")
        return None

# 更新指定MD文件中的图片链接为本地相对路径
def update_md_file(md_file_path, save_folder):
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配 Markdown 的 `![]()` 格式图片链接
    markdown_image_pattern = r'!\[.*?\]\((.*?)[\s"\']*\)'
    # 匹配 HTML 的 `<img src="..." ...>` 格式图片链接
    html_image_pattern = r'<img\s+[^>]*src=["\'](.*?)["\'][^>]*>'

    # 提取两种格式的图片链接
    image_urls = re.findall(markdown_image_pattern, content) + re.findall(html_image_pattern, content)

    for image_url in image_urls:
        # 下载图片并获取本地路径
        local_image_path = download_image(image_url, save_folder)
        if local_image_path:
            # 构建相对路径（相对于md文件所在目录）
            relative_path = os.path.relpath(local_image_path, start=os.path.dirname(md_file_path))
            # 替换图片链接为相对路径
            content = content.replace(image_url, relative_path)

    # 保存修改后的Markdown文件
    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated MD file: {md_file_path}")






# # 遍历文件夹及子文件夹，处理所有.md文件
# def process_folder(root_folder):
#     # 创建一个图片保存的文件夹
#     picture_folder = os.path.join(root_folder, 'picture')
#     Path(picture_folder).mkdir(exist_ok=True)

#     # 遍历文件夹中的所有文件
#     for root, dirs, files in os.walk(root_folder):
#         for file in files:
#             if file.endswith('.md'):
#                 md_file_path = os.path.join(root, file)
#                 update_md_file(md_file_path, picture_folder)


# 只处理指定的 Markdown 文件列表
def process_folder(root_folder, md_files_to_process):
    # 创建一个图片保存的文件夹
    picture_folder = os.path.join(root_folder, 'picture')
    Path(picture_folder).mkdir(exist_ok=True)

    # 遍历指定的 Markdown 文件列表
    for md_file in md_files_to_process:
        # 构建完整路径
        md_file_path = os.path.join(root_folder, md_file)
        if os.path.isfile(md_file_path):  # 确保文件存在
            update_md_file(md_file_path, picture_folder)
        else:
            print(f"File not found: {md_file_path}")



if __name__ == "__main__":
    # 设置目标文件夹路径
    target_folder = './your_target_folder'  # 替换为你的目标文件夹路径

    # 指定需要处理的 Markdown 文件列表（相对于目标文件夹的路径）
    md_files = [
        "subfolder1/file1.md",
        "subfolder2/file3.md",
        "file4.md"
    ]

    process_folder(target_folder, md_files)
