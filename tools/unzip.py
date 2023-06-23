# -*- coding: UTF-8 -*-
# 胡乱写的解压脚本

import os
import zipfile


def fixbug(zip_file):
    # 处理文件乱码
    name_to_info = zip_file.NameToInfo
    for name, info in name_to_info.copy().items():
        try:
            real_name = name.encode("cp437").decode('gbk')
            print(real_name)
        except UnicodeEncodeError:
            continue
        if real_name != name:
            info.filename = real_name
            del name_to_info[name]
            name_to_info[real_name] = info
    return zip_file


def unzip_files():
    current_folder = os.getcwd()  # 获取当前文件夹路径
    for filename in os.listdir(current_folder):
        if filename.endswith('.zip'):  # 仅处理ZIP文件
            folder_name = os.path.splitext(filename)[0]  # 使用文件名创建目标文件夹
            folder_path = os.path.join(current_folder, folder_name)
            with fixbug(zipfile.ZipFile(filename, 'r')) as zip_ref:
                zip_ref.extractall(folder_path)


unzip_files()

# 将lrc文件提取到表层
import shutil


def find_all_folders():
    current_folder = os.getcwd()  # 获取当前目录路径
    all_folders = [os.path.join(current_folder, folder) for folder in os.listdir(current_folder) if
                   os.path.isdir(os.path.join(current_folder, folder))]
    return all_folders


# 调用函数查找当前目录下的所有文件夹
folders = find_all_folders()


def extract_deep_lrc_files(root_folder):
    for foldername, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.lrc'):
                lrc_filepath = os.path.join(foldername, filename)
                destination_folder = root_folder
                if foldername != destination_folder:
                    print(destination_folder)
                    print(lrc_filepath)
                    shutil.copy(lrc_filepath, destination_folder)
                    os.remove(lrc_filepath)


for folder in folders:
    extract_deep_lrc_files(folder)
