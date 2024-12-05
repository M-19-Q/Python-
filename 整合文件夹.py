import os
import shutil

def copy_pdfs_to_target_dir(source_dir, target_dir):
    # 确保目标文件夹存在，如果不存在则创建它
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

        # 遍历源文件夹及其所有子文件夹
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith('.lrc'):
                # 构建源文件的完整路径
                source_file_path = os.path.join(root, file)

                # 构建目标文件的完整路径，这里只需要文件名，不带源文件夹的路径
                target_file_path = os.path.join(target_dir, file)

                # 复制文件
                shutil.copy2(source_file_path, target_file_path)
                print(f"Copied {source_file_path} to {target_file_path}")

source_folder = 'E:\\网易云爬虫\\歌词文件'
target_folder = 'E:\\网易云爬虫\\歌词文件true'
#执行复制操作
copy_pdfs_to_target_dir(source_folder, target_folder)