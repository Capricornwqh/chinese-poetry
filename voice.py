#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pydub import AudioSegment
import argparse

def increase_volume(input_file, output_file, volume_increase_db):
    """
    增加MP3文件的音量
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
        volume_increase_db: 音量增加的分贝数
    """
    try:
        # 加载MP3文件
        audio = AudioSegment.from_mp3(input_file)
        
        # 增加音量
        louder_audio = audio + volume_increase_db
        
        # 导出文件
        louder_audio.export(output_file, format="mp3")
        print(f"✅ 处理完成: {os.path.basename(input_file)}")
        
    except Exception as e:
        print(f"❌ 处理失败 {input_file}: {str(e)}")

def batch_increase_volume(folder_path, volume_increase_db=5, output_prefix="", output_suffix="_louder"):
    """
    批量处理文件夹下的MP3文件
    
    Args:
        folder_path: 文件夹路径
        volume_increase_db: 音量增加的分贝数（默认5dB）
        output_prefix: 输出文件前缀（默认为空）
        output_suffix: 输出文件后缀（默认"_louder"）
    """
    if not os.path.exists(folder_path):
        print(f"❌ 文件夹不存在: {folder_path}")
        return
    
    # 获取所有MP3文件
    mp3_files = [f for f in os.listdir(folder_path) 
                 if f.lower().endswith('.mp3')]
    
    if not mp3_files:
        print("❌ 文件夹中没有找到MP3文件")
        return
    
    print(f"📁 找到 {len(mp3_files)} 个MP3文件")
    print(f"🔊 将增加音量 {volume_increase_db} dB")
    if output_prefix:
        print(f"📝 输出前缀: {output_prefix}")
    if output_suffix:
        print(f"📝 输出后缀: {output_suffix}")
    print("-" * 50)
    
    # 处理每个MP3文件
    for mp3_file in mp3_files:
        input_path = os.path.join(folder_path, mp3_file)
        
        # 生成输出文件名
        name, ext = os.path.splitext(mp3_file)
        output_filename = f"{output_prefix}{name}{output_suffix}{ext}"
        output_path = os.path.join(folder_path, output_filename)
        
        # 增加音量
        increase_volume(input_path, output_path, volume_increase_db)

def main():
    parser = argparse.ArgumentParser(description="批量增加MP3文件音量")
    parser.add_argument("folder", help="包含MP3文件的文件夹路径")
    parser.add_argument("-v", "--volume", type=int, default=5, 
                       help="音量增加的分贝数 (默认: 5)")
    parser.add_argument("-p", "--prefix", default="易中天先秦诸子", 
                       help="输出文件前缀 (默认: 无)")
    parser.add_argument("-s", "--suffix", default="", 
                       help="输出文件后缀 (默认: 无)")
    
    args = parser.parse_args()
    
    # 检查依赖
    try:
        import pydub
    except ImportError:
        print("❌ 缺少依赖库 pydub")
        print("请运行: pip install pydub")
        print("注意: 可能还需要安装 ffmpeg")
        sys.exit(1)
    
    # 执行批量处理
    batch_increase_volume(args.folder, args.volume, args.prefix, args.suffix)
    print("\n🎉 批量处理完成！")

if __name__ == "__main__":
    main()