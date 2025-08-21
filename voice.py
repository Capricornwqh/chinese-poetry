#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pydub import AudioSegment
import argparse
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from typing import Tuple

# 全局锁用于打印输出
print_lock = threading.Lock()

def clean_filename(filename):
    """
    清理文件名，去除B站视频信息
    
    Args:
        filename: 原始文件名
        
    Returns:
        清理后的文件名
    """
    # 去除扩展名
    name, ext = os.path.splitext(filename)
    
    # 使用正则表达式去除 (Av数字,P数字).flv 部分
    # 匹配模式：(Av\d+,P\d+)\.flv
    cleaned_name = re.sub(r'\(Av\d+,P\d+\)\.flv', '', name)
    
    # 去除末尾可能的空格
    cleaned_name = cleaned_name.strip()
    
    return cleaned_name + ext

def increase_volume_single(task_info: Tuple[str, str, int, str]) -> Tuple[bool, str]:
    """
    处理单个MP3文件的音量增加
    
    Args:
        task_info: (input_file, output_file, volume_increase_db, original_filename)
        
    Returns:
        (success, message)
    """
    input_file, output_file, volume_increase_db, original_filename = task_info
    
    try:
        # 加载MP3文件
        audio = AudioSegment.from_mp3(input_file)
        
        # 增加音量
        louder_audio = audio + volume_increase_db
        
        # 导出文件
        louder_audio.export(output_file, format="mp3")
        
        return True, f"✅ 处理完成: {original_filename}"
        
    except Exception as e:
        return False, f"❌ 处理失败 {original_filename}: {str(e)}"

def safe_print(message):
    """线程安全的打印函数"""
    with print_lock:
        print(message)

def batch_increase_volume(folder_path, volume_increase_db=5, output_prefix="", output_suffix="", max_workers=4):
    """
    批量处理文件夹下的MP3文件（并发版本）
    
    Args:
        folder_path: 文件夹路径
        volume_increase_db: 音量增加的分贝数（默认5dB）
        output_prefix: 输出文件前缀（默认为空）
        output_suffix: 输出文件后缀（默认为空）
        max_workers: 最大并发工作线程数（默认4）
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
    print(f"🚀 使用 {max_workers} 个并发线程")
    if output_prefix:
        print(f"📝 输出前缀: {output_prefix}")
    if output_suffix:
        print(f"📝 输出后缀: {output_suffix}")
    print("-" * 50)
    
    # 准备任务列表
    tasks = []
    for mp3_file in mp3_files:
        input_path = os.path.join(folder_path, mp3_file)
        
        # 清理文件名
        cleaned_filename = clean_filename(mp3_file)
        
        # 生成输出文件名
        name, ext = os.path.splitext(cleaned_filename)
        output_filename = f"{output_prefix}{name}{output_suffix}{ext}"
        output_path = os.path.join(folder_path, output_filename)
        
        print(f"🔄 {mp3_file} -> {output_filename}")
        
        # 添加到任务列表
        tasks.append((input_path, output_path, volume_increase_db, mp3_file))
    
    print(f"\n🚀 开始并发处理 {len(tasks)} 个文件...")
    
    # 使用线程池执行并发处理
    success_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_task = {executor.submit(increase_volume_single, task): task for task in tasks}
        
        # 处理完成的任务
        for future in as_completed(future_to_task):
            success, message = future.result()
            safe_print(message)
            
            if success:
                success_count += 1
            else:
                failed_count += 1
    
    # 打印处理结果统计
    print("\n" + "=" * 50)
    print(f"📊 处理完成统计:")
    print(f"✅ 成功: {success_count} 个文件")
    print(f"❌ 失败: {failed_count} 个文件")
    print(f"📁 总计: {len(tasks)} 个文件")

def main():
    parser = argparse.ArgumentParser(description="批量增加MP3文件音量（并发版本）")
    parser.add_argument("folder", help="包含MP3文件的文件夹路径")
    parser.add_argument("-v", "--volume", type=int, default=10, 
                       help="音量增加的分贝数 (默认: 10)")
    parser.add_argument("-p", "--prefix", default="", 
                       help="输出文件前缀 (默认: 无)")
    parser.add_argument("-s", "--suffix", default="", 
                       help="输出文件后缀 (默认: 无)")
    parser.add_argument("-w", "--workers", type=int, default=5,
                       help="并发工作线程数 (默认: 5)")
    
    args = parser.parse_args()
    
    # 验证并发线程数
    if args.workers < 1:
        print("❌ 并发线程数必须大于0")
        sys.exit(1)
    
    if args.workers > os.cpu_count():
        print(f"⚠️  警告: 设置的线程数({args.workers})超过CPU核心数({os.cpu_count()})")
        response = input("是否继续? (y/N): ")
        if response.lower() != 'y':
            print("操作已取消")
            sys.exit(0)
    
    # 检查依赖
    try:
        import pydub
    except ImportError:
        print("❌ 缺少依赖库 pydub")
        print("请运行: pip install pydub")
        print("注意: 可能还需要安装 ffmpeg")
        sys.exit(1)
    
    # 执行批量处理
    batch_increase_volume(args.folder, args.volume, args.prefix, args.suffix, args.workers)
    print("\n🎉 批量处理完成！")

if __name__ == "__main__":
    main()