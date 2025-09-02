import os
import json
import numpy as np
import matplotlib.pyplot as plt
import statistics

"""
主要组成部分是,平稳性检测被认为是平稳的序列，大部分都是高噪声的，

主要结论： 平稳性确实，往往都是噪声，无法学习，因此在平稳序列场景下的预测是一个难题、4
    TODO: 验证平稳模型的预测效果更好
"""

def stationary(property_path='property_txt', log_path='Select_Synth', target_path='table_use', mediate_path='property_performance', save_mediate=False, print_result=True):

    # 读取 stationarity.txt 中的 (b, n) 索引
    result_sta = set()

    with open(property_path + '/stationarity.txt', 'r', encoding='utf-8') as f:
        for line in f:
            b, n = line.strip().split(',')
            result_sta.add((int(b), int(n)))  # 假设 b 和 n 是整数
    # print(result_sta)

    current_directory = log_path # 'performance_select'
    npz_files = [f for f in os.listdir(current_directory) if f.endswith('.npz')]


    name_list = []

    all_mae_mean = []
    all_mae_mid = []
    sta_mae_mean = []
    sta_mae_mid = []
    nonsta_mae_mean = []
    nonsta_mae_mid = []

    all_mse_mean = []
    all_mse_mid = []
    sta_mse_mean = []
    sta_mse_mid = []
    nonsta_mse_mean = []
    nonsta_mse_mid = []


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

        for b, n in result_sta:
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
        all_mae = mae[~bn_mask]

        bn_mse = mse[bn_mask]
        all_mse = mse[~bn_mask]
        #print(bn_mae)
        bn_mean = np.round(np.mean(bn_mae),5)
        bn_median = np.round(np.median(bn_mae),5)
        all_mean = np.round(np.mean(all_mae),5)
        all_median = np.round(np.median(all_mae),5)

        bn_mean_mse = np.round(np.mean(bn_mse),5)
        bn_median_mse = np.round(np.median(bn_mse),5)
        all_mean_mse = np.round(np.mean(all_mse),5)
        all_median_mse = np.round(np.median(all_mse),5)

        mae_mean = np.round(np.mean(mae),5)
        mae_median = np.round(np.median(mae),5)

        mse_mean = np.round(np.mean(mse),5)
        mse_median = np.round(np.median(mse),5)

        name_list.append(name)

        if print_result:

            print('------1. Stationary phase------')
            print(name)
            print(mae[0,0], mse[0,0])
            print(f"ALL MAE Mean: {mae_mean}, ALL MAE Median: {mae_median}")
            print(f"Stationarity MAE Mean: {bn_mean}, Stationarity MAE Median: {bn_median}")
            print(f"Non-stationarity MAE Mean: {all_mean}, Non-stationarity MAE Median: {all_median}")
            print(f"ALL MSE Mean: {mse_mean}, ALL MSE Median: {mse_median}")
            print(f"Stationarity MSE Mean: {bn_mean_mse}, Stationarity MSE Median: {bn_median_mse}")
            print(f"Non-stationarity MSE Mean: {all_mean_mse}, Non-stationarity MSE Median: {all_median_mse}")



        all_mae_mean.append(str(np.round(mae_mean, 3)))
        all_mae_mid.append(str(np.round(mae_median, 3)))
        sta_mae_mean.append(str(np.round(bn_mean, 3)))
        sta_mae_mid.append(str(np.round(bn_median, 3)))
        nonsta_mae_mean.append(str(np.round(all_mean, 3)))
        nonsta_mae_mid.append(str(np.round(all_median, 3)))

        all_mse_mean.append(str(np.round(mse_mean, 3)))
        all_mse_mid.append(str(np.round(mse_median, 3)))
        sta_mse_mean.append(str(np.round(bn_mean_mse, 3)))
        sta_mse_mid.append(str(np.round(bn_median_mse, 3)))
        nonsta_mse_mean.append(str(np.round(all_mean_mse, 3)))
        nonsta_mse_mid.append(str(np.round(all_median_mse, 3)))

        results[name] = {
            'Stationarity': {
                'MAE': [str(int(x * 10000)) for x in bn_mae.tolist()],
                'MSE': [str(int(x * 10000))for x in bn_mse.tolist()],
            },
            'Non-stationarity': {
                'MAE': [str(int(x * 10000)) for x in all_mae.tolist()],
                'MSE': [str(int(x * 10000)) for x in all_mse.tolist()],
            }
        }


        # 将当前结果追加写入 JSON 文件
        if save_mediate:
            with open(mediate_path + '/stationarity_results.json', 'a', encoding='utf-8') as json_file:
                json.dump({name: results[name]}, json_file, ensure_ascii=False)
                json_file.write('\n')  # 写入换行符以便于后续处理'''

    with open(target_path + '/1stationarity_paper.txt', 'w', encoding='utf-8') as f:
        for i in range(len(name_list)):
            s1 = "\\multirow{2}{*}{ \\textbf{" + '{}'.format(name_list[i]) + "}}"+'& MAE'+'&'+all_mae_mean[i]+\
                     '&'+all_mae_mid[i]+'&'+sta_mae_mean[i]+'&'+sta_mae_mid[i]+'&'+nonsta_mae_mean[i]+'&'+nonsta_mae_mid[i]
            s2 = '&' +'MSE&'+ all_mse_mean[i] +'&'+ all_mse_mid[i] +'&'+ sta_mse_mean[i] +'&'+ sta_mse_mid[i] +'&'+ nonsta_mse_mean[i] +'&' +nonsta_mse_mid[i]
            # print(s1)
            # print(s2)
            f.write(s1+'\n')
            f.write(s2+'\n')





