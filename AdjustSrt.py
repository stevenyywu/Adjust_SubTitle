import re
import os

# 定义需要转写的 srt 文件位置,# 输出文件保持源文件相同路径，文件名为 adjusted_源文件名
srt_file = 'D:/OneDrive/HR HK Lessons/5310 Portfolio Optimization with R/week2/5310 week2 convex optimization problems .srt'

# 获取文件的目录路径和基本名称
directory = os.path.dirname(srt_file)
filename = os.path.basename(srt_file)
new_filename = filename.replace('.srt', '_adjusted.srt')
# 生成输出文件的完整路径
output_file = os.path.join(directory, new_filename)

# 读取srt文件内容
with open(srt_file, 'r') as file:
    content = file.read()

# 将内容按空行分割成不同的组
old_groups = re.split(r'\n\s*\n', content)

# 用于记录当前该处理 old_groups 中的第几个组
current_number = 0
# 用于在 new_groups 中的索引
index = 0
new_groups = []

for i in range(len(old_groups)):
    # 如果 i 不等于 current_number 就跳过
    if(i == current_number):
        # 提取编号、时间段和字幕文本
        group = old_groups[i].strip().split('\n')

        if len(group) >= 3:
            number = group[0]
            time_range = group[1]
            text = ' '.join(group[2:])

            if text.endswith(('.', ',', ':', ';', '?', '!')):
                # 如果字幕文本以标点符号结尾
                new_groups.append(f"{index}\n{time_range}\n{text}")
                current_number += 1
            else:
                # 合并时间段和字幕文本
                time_range_start = re.search(r'(\d{2}:\d{2}:\d{2},\d{3})', time_range).group(1)
                # next_time_range_end = re.search(r'(\d{2}:\d{2}:\d{2},\d{3})', old_groups[i + 1]).group(1)
                #获取下一个时间段的结尾时间，即正则表达式中的第二个匹配项 re.findall
                next_time_range_end = re.findall(r'(\d{2}:\d{2}:\d{2},\d{3})', old_groups[i + 1])[1]

                new_time_range = f"{time_range_start} --> {next_time_range_end}"

                current_text = text
                next_text = ' '.join(old_groups[i + 1].strip().split('\n')[2:])
                new_text = f"{current_text} {next_text}"

                new_groups.append(f"{index}\n{new_time_range}\n{new_text}")
                current_number += 2

            index += 1

# 将new_groups的内容按srt格式写入新的srt文件
with open(output_file, 'w') as file:
    file.write('\n\n'.join(new_groups))
