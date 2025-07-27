#!/bin/bash

# 检查是否提供了工作目录参数
if [ $# -ne 1 ]; then
    echo "用法: $0 <工作目录>"
    exit 1
fi

# 工作目录
work_dir="$1"

# 检查工作目录是否存在
if [ ! -d "$work_dir" ]; then
    echo "错误：工作目录 '$work_dir' 不存在"
    exit 1
fi

# 切换到工作目录
cd "$work_dir" || exit 1

# 设置目标文件大小(10MB = 10485760 bytes)
target_size=10485760
current_file=1
current_size=0

# 创建输出目录
output_dir="${work_dir}/merged_files"
mkdir -p "$output_dir"

# 初始化第一个输出文件
output_file="${output_dir}/merged_${current_file}.md"
touch "$output_file"

# 遍历工作目录下的所有文件
for file in *; do
    # 跳过目录、脚本本身和输出目录
    if [ -d "$file" ] || [ "$file" == "$(basename $0)" ] || [ "$file" == "$output_dir" ]; then
        continue
    fi
    
    # 获取文件大小
    file_size=$(stat --format=%s "$file")
    
    # 如果当前合并文件大小即将超过目标大小，创建新文件
    if [ $((current_size + file_size)) -gt $target_size ]; then
        echo "创建新文件 merged_${current_file}.txt (当前大小: $current_size 字节)"
        current_file=$((current_file + 1))
        output_file="${output_dir}/merged_${current_file}.md"
        current_size=0
    fi
    
    # 合并文件
    cat "$file" >> "$output_file"
    current_size=$((current_size + file_size))
    
    echo "已合并文件: $file (大小: $file_size 字节)"
done

echo "合并完成！文件保存在 $work_dir/$output_dir 目录下"