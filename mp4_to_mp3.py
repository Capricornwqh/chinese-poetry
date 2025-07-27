import os
import argparse
from moviepy import VideoFileClip

def convert_mp4_to_mp3(input_dir, output_dir=None):
    """
    将指定目录中的所有MP4文件转换为MP3格式
    
    参数:
        input_dir (str): 包含MP4文件的目录路径
        output_dir (str, 可选): 保存MP3文件的目录路径，默认与input_dir相同
    """
    # 如果没有指定输出目录，使用输入目录
    if output_dir is None:
        output_dir = input_dir
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有MP4文件
    mp4_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.mp4')]
    total_files = len(mp4_files)
    
    if total_files == 0:
        print(f"在目录 {input_dir} 中没有找到MP4文件")
        return
    
    print(f"找到 {total_files} 个MP4文件，开始转换...")
    
    # 转换每个文件
    for i, mp4_file in enumerate(mp4_files, 1):
        mp4_path = os.path.join(input_dir, mp4_file)
        mp3_file = os.path.splitext(mp4_file)[0] + '.mp3'
        mp3_path = os.path.join(output_dir, mp3_file)
        
        print(f"[{i}/{total_files}] 正在转换: {mp4_file} -> {mp3_file}")
        
        try:
            video = VideoFileClip(mp4_path)
            audio = video.audio
            if audio is not None:
                audio.write_audiofile(mp3_path)
                audio.close()
            else:
                print(f"警告：{mp4_file} 没有音轨")
            video.close()
            print(f"[{i}/{total_files}] 转换完成: {mp3_file}")
        except Exception as e:
            print(f"转换 {mp4_file} 时出错: {str(e)}")
    
    print("所有文件转换完成！")

def main():
    parser = argparse.ArgumentParser(description='将MP4文件转换为MP3格式')
    parser.add_argument('input_dir', help='包含MP4文件的目录路径')
    parser.add_argument('--output_dir', help='保存MP3文件的目录路径 (可选)')
    
    args = parser.parse_args()
    
    convert_mp4_to_mp3(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()