#!/bin/bash

#编写一个shell脚本(linux)，功能如下:
#在给定文件中搜索指定内容，
# 并将搜索结果(含内容出现的行号)保存到新的文件中，
# 同时结果输出到控制台
# 提示用户输入要搜索的内容

echo "请输入要搜索的内容："
read search_term

# 提示用户输入要搜索的文件
echo "请输入要搜索的文件："
read input_file

# 提示用户输入保存结果的文件名
echo "请输入保存结果的文件名："
read output_file

# 使用grep搜索内容，并将结果保存到新文件，包含行号
grep -n "$search_term" "$input_file" > "$output_file"

# 显示搜索结果
echo "搜索结果保存到 $output_file："
cat "$output_file"