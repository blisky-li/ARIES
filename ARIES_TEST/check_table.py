import os
import json
import numpy as np
import matplotlib.pyplot as plt
import statistics

# 获取当前工作目录
current_directory = os.getcwd()

# 列出所有txt文件
txt_files = [f for f in os.listdir(current_directory) if f.endswith('.txt')]

# 确保文件列表不为空
if not txt_files:
    print("没有找到任何txt文件。")
else:
    # 假设txt_files已定义，current_directory为当前目录
    file_contents = []
    for file in txt_files:
        with open(os.path.join(current_directory, file), 'r') as f:
            file_contents.append(f.readlines())

    # 假设所有文件行数相同
    num_lines = len(file_contents[0])

    # 拼接每一行的内容
    result = []
    for i in range(num_lines):
        concatenated_line = '&'.join(
            file_contents[j][i].strip().replace('nan', '-') for j in range(len(file_contents))
        )
        result.append(concatenated_line)

    # 统计第一行中&的数量
    first_line = result[0]  # 第一行拼接后的内容

    count_ampersands = first_line.count('&')
    print(f"第一行中 '&' 的数量是: {count_ampersands}")

    # 将数据按列分组
    columns = list(zip(*[line.split('&') for line in result]))

    # 处理并排除前两列字符串以及nan值
    highlighted_result = []
    for col in columns:
        # 排除前两列的字符串和nan值，并转换为浮动数字
        cleaned_col = [(float(val) if val.replace('.', '', 1).isdigit() else None) for val in col]

        # 奇数行和偶数行分开处理
        odd_indexed_values = [(val, idx) for idx, val in enumerate(cleaned_col) if val is not None and idx % 2 == 1]
        even_indexed_values = [(val, idx) for idx, val in enumerate(cleaned_col) if val is not None and idx % 2 == 0]

        # 对奇数行排序
        sorted_odd = sorted(odd_indexed_values, key=lambda x: x[0])
        top_10_odd = sorted_odd[-10:]  # 后10名
        bottom_10_odd = sorted_odd[:10]  # 前10名
        top_5_odd = sorted_odd[-5:]  # 后5名
        bottom_5_odd = sorted_odd[:5]  # 前5名

        # 对偶数行排序
        sorted_even = sorted(even_indexed_values, key=lambda x: x[0])
        top_10_even = sorted_even[-10:]  # 后10名
        bottom_10_even = sorted_even[:10]  # 前10名
        top_5_even = sorted_even[-5:]  # 后5名
        bottom_5_even = sorted_even[:5]  # 前5名

        # 计算需要高亮的索引
        red_odd_indexes = {idx for _, idx in top_5_odd}  # 后5标红
        blue_odd_indexes = {idx for _, idx in bottom_5_odd}  # 前5标蓝
        red2_odd_indexes = {idx for _, idx in top_10_odd if idx not in red_odd_indexes}
        blue2_odd_indexes = {idx for _, idx in bottom_10_odd if idx not in blue_odd_indexes}  # 前10排除前5和后10排除后5标绿

        red_even_indexes = {idx for _, idx in top_5_even}  # 后5标红
        blue_even_indexes = {idx for _, idx in bottom_5_even}  # 前5标蓝
        red2_even_indexes = {idx for _, idx in top_10_even if idx not in red_even_indexes}
        blue2_even_indexes = {idx for _, idx in bottom_10_even if idx not in blue_even_indexes}  # 前10排除前5和后10排除后5标绿

        # 重新构建这一列，替换符合条件的值为LaTeX颜色标记
        highlighted_column = []
        for idx, val in enumerate(col):
            # 前两列的字符串保持原样
            if idx < 2:
                highlighted_column.append(val)
            elif val == 'nan' or val == '-':
                highlighted_column.append(val)  # 保留"nan"或"-"
            else:
                # 其他值如果是最大值或最小值就加颜色
                if idx in red_odd_indexes or idx in red_even_indexes:
                    highlighted_column.append(f'\\cellcolor{{red!30}}{val}')
                elif idx in red2_odd_indexes or idx in red2_even_indexes:
                    highlighted_column.append(f'\\cellcolor{{red!15}}{val}')
                elif idx in blue_odd_indexes or idx in blue_even_indexes:
                    highlighted_column.append(f'\\cellcolor{{blue!30}}{val}')
                elif idx in blue2_odd_indexes or idx in blue2_even_indexes:
                    highlighted_column.append(f'\\cellcolor{{blue!15}}{val}')
                else:
                    highlighted_column.append(val)

        # 更新最终结果
        highlighted_result.append(highlighted_column)

    # 将结果拼接成新的行
    print(len(highlighted_result))
    final_result = []
    for i in range(num_lines):
        final_result.append('&'.join(highlighted_result[j][i] for j in range(count_ampersands+1)) + r'\\')
        if i % 2 == 1:
            final_result.append(r'\hline')

    # 输出结果
    for line in final_result:
        print(line)

    # 打印或者返回最终的拼接结果
    '''for line in final_result:
        print(line)'''

    '''for i in range(len(final_result)):
        print(final_result[i] + r'\\')
        if i % 2 == 1:
            print(r'\hline')'''
    #'
    ''' 打印或者返回最终的拼接结果
    for line in final_result:
        print(line)'''
    '''# 读取所有txt文件的内容
    file_contents = []
    for file in txt_files:
        with open(os.path.join(current_directory, file), 'r') as f:
            file_contents.append(f.readlines())

    # 假设所有文件行数相同
    num_lines = len(file_contents[0])

    # 拼接每一行的内容
    result = []
    for i in range(num_lines):
        # 获取第i行所有文件的内容，删除换行符并替换nan为"-"
        concatenated_line = '&'.join(
            file_contents[j][i].strip().replace('nan', '-') for j in range(len(file_contents))
        )
        result.append(concatenated_line)
        # 统计第一行中&的数量
    first_line = result[0]  # 第一行拼接后的内容
    count_ampersands = first_line.count('&')

        # 输出结果
    print(f"第一行中 '&' 的数量是: {count_ampersands}")
    for i in range(len(result)):
        print(result[i]+r'\\')
        if i % 2 == 1:
            print(r'\hline')'''
    '''# 输出拼接后的结果
    with open('result.txt', 'w', encoding='utf-8') as f:
        for i in result:
            f.write(i+r'\\')'''


