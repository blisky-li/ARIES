import os
import json
import numpy as np
import matplotlib.pyplot as plt
import statistics

"""
高异常：0.2-0.3，其实比较难学，但是revin的模型性能都非常好，但是问题是，对0.1-0.2之间的好像效果不明显。
0。2-0.3是抖动强、大周期趋势，且出现均值漂移的。然而，0-0.05大部分是直线或者均匀波动的
0.05-0.1主要是大波浪、大周期趋势+抖动，趋势+周期
"""


def anomoly(property_path='property_txt', log_path='Select_Synth', target_path='table_use', mediate_path='property_performance', save_mediate=False, print_result=True):
    count = []

    result_sta = set()

    with open(property_path + '/stationarity.txt', 'r', encoding='utf-8') as f:
        for line in f:
            b, n  = line.strip().split(',')
            result_sta.add((int(b), int(n)))  # 假设 b 和 n 是整数

    count2 = []
    result_anomoly = dict()

    with open(property_path + '/anomoly_zscore.txt', 'r', encoding='utf-8') as f:
        for line in f:
            b, n, strength = line.strip().split(',')
            if (int(b), int(n)) not in result_sta:
                strength = int(strength)  # 将strength转换为浮点数
                key = str(strength)
                if key not in result_anomoly:
                    result_anomoly[key] = []
                result_anomoly[key].append((b, n))

    current_directory = log_path
    npz_files = [f for f in os.listdir(current_directory) if f.endswith('.npz')]

    # 遍历 .npz 文件
    for filename in npz_files:
        # 存储结果的字典
        results = {}

        name = filename.split('_')[0]
        file_path = os.path.join(current_directory, filename)

        mae = np.load(file_path)['mae']  # 假设 mae 是一个 B x N 的数组
        mse = np.load(file_path)['mse']

        # 创建 bn_mask 字典
        bn_masks = {str(i): np.zeros((mae.shape[0], mae.shape[1]), dtype=bool)
                    for i in range(4)}

        for key, values in result_anomoly.items():
            for b, n in values:
                b_index = int(b)  # 根据需要转换为适当的索引
                n_index = int(n)  # 根据需要转换为适当的索引
                if bn_masks[key].shape[0] > 10:
                    bn_masks[key][b_index, n_index] = True
                else:
                    if (b_index % 336) == 0:
                        b2 = (b_index // 336)
                        bn_masks[key][b2, n_index] = True
        # 打印结果以确认

        mask02 = bn_masks['0']
        mask24 = bn_masks['1']
        mask46 = bn_masks['2']
        mask68 = bn_masks['3']
        # mask81 = bn_masks['0.8-1.0']

        all_mae_values = []
        bn_mae_values = []

        mae02 = mae[mask02]
        mse02 = mse[mask02]

        mae24 = mae[mask24]
        mse24 = mse[mask24]

        mae46 = mae[mask46]
        mse46 = mse[mask46]

        mae68 = mae[mask68]
        mse68 = mse[mask68]

        # 假设已有mae和mse的数组，以及各个mask
        mae_values = [mae02, mae24, mae46, mae68]
        mse_values = [mse02, mse24, mse46, mse68]
        # names = ["02", "24", "46", "68", "81"]
        names = ['0', '1', '2', '3']
        mae_mean = np.mean(mae)
        mae_median = np.median(mae)

        mse_mean = np.mean(mse)
        mse_median = np.median(mse)
        if print_result:
            print('------7. Anomoly phase------')
            print(name)
            print(f"ALL MAE Mean: {mae_mean}, ALL MAE Median: {mae_median}")
            print(f"ALL MSE Mean: {mse_mean}, ALL MSE Median: {mse_median}")
        results[name] = {}
        l = []
        l2 = []
        for i, tag in enumerate(names):
            mae_mean = np.mean(mae_values[i])
            mae_median = np.median(mae_values[i])
            mse_mean = np.mean(mse_values[i])
            mse_median = np.median(mse_values[i])
            l.append(str(np.round(mae_mean, 3)))
            l.append(str(np.round(mae_median, 3)))
            l2.append(str(np.round(mse_mean, 3)))
            l2.append(str(np.round(mse_median, 3)))

            results[name][tag] = {
                'MAE': [str(int(x * 10000)) for x in mae_values[i].tolist()],
                'MSE': [str(int(x * 10000)) for x in mse_values[i].tolist()],
            }
            if print_result:
                print(mae_values[i].shape)
                print(f"Subset {tag}:")
                print(f"  MAE Mean: {mae_mean}, MAE Median: {mae_median}")
                print(f"  MSE Mean: {mse_mean}, MSE Median: {mse_median}")
                print()
        if save_mediate:
            with open(mediate_path + '/anomoly_results.json', 'a', encoding='utf-8') as json_file:
                json.dump({name: results[name]}, json_file, ensure_ascii=False)
                json_file.write('\n')  # 写入换行符以便于后续处理'
        with open(target_path + '/9anomoly_paper.txt', 'a', encoding='utf-8') as f:
            s1 = "&".join(l) + '\n'
            s2 = "&".join(l2) + '\n'
            f.write(s1)
            f.write(s2)
            l = []
            l2 = []