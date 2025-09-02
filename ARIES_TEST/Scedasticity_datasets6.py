import os
import json
import numpy as np
import matplotlib.pyplot as plt
import statistics

"""
本来应该就是有平稳序列被归到这一部分
之前存在：在平稳性检测中被误判的非平稳序列中的某一部分（有B,N的序列没有通过平稳检测），但被归为同方差。

主要组成部分是完全是趋势的直线。在边缘存在平稳序列+周期性的组合，但是它们无法通过平稳性检测，但是确实同方差、

同方差的，比如趋势序列，平稳的周期等等，其性能都不错。异方差的可能还是稍微难一些。

"""



def scedasticity(property_path='property_txt', log_path='Select_Synth', target_path='table_use', mediate_path='property_performance', save_mediate=False, print_result=True):
    count = []
    # 读取 scedasticity.txt 中的 (b, n) 索引
    result_sta = set()

    with open(property_path + '/stationarity.txt', 'r', encoding='utf-8') as f:
        for line in f:
            b, n = line.strip().split(',')
            result_sta.add((int(b), int(n)))  # 假设 b 和 n 是整数

    count2 = []
    result_sca = set()
    with open(property_path + '/scedasticity.txt', 'r', encoding='utf-8') as f:
        for line in f:
            b, n = line.strip().split(',')
            if (int(b), int(n)) not in result_sta:
                result_sca.add((int(b), int(n)))

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
        all_mae_values = []
        bn_mae_values = []

        bn_mask = np.zeros(mae.shape, dtype=bool)

        for b, n in result_sca:
            if bn_mask.shape[0] > 10:
                bn_mask[b, n] = True
            else:
                if (b % 336) == 0:
                    b2 = (b // 336)
                    bn_mask[b2, n] = True
        # 获取文件的 (b, n) 索引
        # print(bn_mask)
            # 根据布尔数组分类
        bn_mae = mae[bn_mask]
        bn_mse = mse[bn_mask]

        for b, n in result_sta:
            if bn_mask.shape[0] > 10:
                bn_mask[b, n] = True
            else:
                if (b % 336) == 0:
                    b2 = (b // 336)
                    bn_mask[b2, n] = True

        all_mae = mae[~bn_mask]
        all_mse = mse[~bn_mask]

        #print(bn_mae)
        bn_mean = np.round(np.mean(bn_mae), 5)
        bn_median = np.round(np.median(bn_mae), 5)
        all_mean = np.round(np.mean(all_mae), 5)
        all_median = np.round(np.median(all_mae), 5)

        bn_mean_mse = np.round(np.mean(bn_mse), 5)
        bn_median_mse = np.round(np.median(bn_mse), 5)
        all_mean_mse = np.round(np.mean(all_mse), 5)
        all_median_mse = np.round(np.median(all_mse), 5)

        mae_mean = np.round(np.mean(mae), 5)
        mae_median = np.round(np.median(mae), 5)

        mse_mean = np.round(np.mean(mse), 5)
        mse_median = np.round(np.median(mse), 5)
        l = []
        l2 = []
        l.append(str(np.round(bn_mean, 3)))
        l.append(str(np.round(bn_median, 3)))
        l.append(str(np.round(all_mean, 3)))
        l.append(str(np.round(all_median, 3)))
        l2.append(str(np.round(bn_mean_mse, 3)))
        l2.append(str(np.round(bn_median_mse, 3)))
        l2.append(str(np.round(all_mean_mse, 3)))
        l2.append(str(np.round(all_median_mse, 3)))
        if print_result:
            print('------6. Scedasticity phase------')
            print(name)
            print(f"ALL MAE Mean: {mae_mean}, ALL MAE Median: {mae_median}")
            print(f"Homo-Scedasticity MAE Mean: {bn_mean}, Homo-Scedasticity MAE Median: {bn_median}")
            print(f"Hetro-Scedasticity MAE Mean: {all_mean}, Hetro-Scedasticity MAE Median: {all_median}")
            print(f"ALL MSE Mean: {mse_mean}, ALL MSE Median: {mse_median}")
            print(f"Homo-Scedasticity MSE Mean: {bn_mean_mse}, Homo-Scedasticity MSE Median: {bn_median_mse}")
            print(f"Hetro-Scedasticity MSE Mean: {all_mean_mse}, Hetro-Scedasticity MSE Median: {all_median_mse}")

        with open(target_path + '/8scedasticity_paper.txt', 'a', encoding='utf-8') as f:
            s1 = "&".join(l) + '\n'
            s2 = "&".join(l2) + '\n'
            f.write(s1)
            f.write(s2)
            l = []
            l2 = []
        results[name] = {
            'Homo-Scedasticity': {
                'MAE': [str(int(x * 10000)) for x in bn_mae.tolist()],
                'MSE': [str(int(x * 10000))for x in bn_mse.tolist()],
            },
            'Hetro-Scedasticity': {
                'MAE': [str(int(x * 10000)) for x in all_mae.tolist()],
                'MSE': [str(int(x * 10000)) for x in all_mse.tolist()],
            }
        }
        if save_mediate:
            with open(mediate_path + '/scedasticity_results.json', 'a', encoding='utf-8') as json_file:
                json.dump({name: results[name]}, json_file, ensure_ascii=False)
                json_file.write('\n')  # 写入换行符以便于后续处理''''''

