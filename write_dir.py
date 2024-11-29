import os


pwd = os.getcwd()
md_path = os.path.join(pwd, 'README.md')
md = open(md_path, 'w', encoding='utf-8')
md.write('# README\n')
md.write('> 学习网络安全的过程中做的笔记和一些零零散散的东西。来源于网络、B站视频以及自己的总结。\n\n')
f_list = list(os.walk(f'{pwd}\\笔记\\'))

def sort_key(x):
    parts = x[0]
    parts = parts.split('\\')[-1].split('.')
    temp = int(parts[0]) if parts[-2].isdigit() else x[0]
    return temp

f_list = sorted(f_list[1:], key=sort_key)



for index, (root, dirs, files) in enumerate(f_list):
    title2 = root.split('\\')[-1]

    md.write('\n## {}\n'.format(title2))
    # 对文件夹下的文件进行排序
    files = sorted(files, key=lambda x: int(x.split('.')[0]))
    for file in files:
        file_name = file.split('.md')[0]
        file_relitive_path = f'./笔记/{title2}/' + file.replace(' ', '%20')
        md.write(f'- [{file_name}]({file_relitive_path})\n')

md.close()