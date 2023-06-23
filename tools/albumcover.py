# -*- coding: utf-8 -*-
"""ChatGPT生成的一段修改封面的代码"""
import re
from pathlib import Path
import subprocess


def AutoAddCover(path):
    """输入文件夹，自动将文件夹下的音频文件封面替换为文件夹同名的jpg文件"""
    folder_path = Path(path)
    audio_ext = ['.mp3', '.wav']
    jpg_ext = '.jpg'

    # 循环处理文件夹中的每个MP3文件
    for file_path in folder_path.glob('*'):
        if file_path.is_file() and file_path.suffix in audio_ext:
            bHasCover = IsMusicHasCover(file_path)
            if bHasCover:
                continue

            # 构造封面文件路径
            cover_path = folder_path.joinpath(folder_path.name + jpg_ext)
            if not cover_path.is_file():
                print("{}不存在封面".format(folder_path.name))
                return False
            # 构造临时文件路径
            temp_output_path = file_path.with_suffix('.temp' + file_path.suffix)

            # 构造FFmpeg命令
            cmd = ['ffmpeg', '-i', str(file_path), '-i', str(cover_path), '-map', '0', '-map', '1',
                   '-metadata:s:v', 'title="Album cover"', '-metadata:s:v', 'comment="Cover (front)"',
                   '-c', 'copy', '-y', str(temp_output_path)]

            # 调用FFmpeg命令
            subprocess.run(cmd)

            # 删除原始文件
            file_path.unlink()

            # 将临时文件重命名为原始文件
            temp_output_path.rename(file_path)
    return True


def IsMusicHasCover(filename):
    cmd = ['ffmpeg', '-i', str(filename)]
    result = subprocess.run(cmd, capture_output=True)
    output = result.stdout.decode("utf-8") + result.stderr.decode("utf-8")

    pattern = r'Metadata:\s+title\s+:\s+"Album cover"'
    if re.search(pattern, output):
        return True
    return False
