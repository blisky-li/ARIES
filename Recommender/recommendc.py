from recommend_testc.data_loader import read_npy
from recommend_testc.indicators_main import compute_indicators
from recommend_testc.recommend_aries import recommend_aries



if __name__ == '__main__':
    path = 'data/'
    name = 'ETTh1_sampled.npy'
    length = 336
    strid = 720
    n_job = 20
    mode = 'large'
    query = 'mae'
    samples_rate = 0.1
    data = read_npy(path, name, length, strid)
    # data2 = read_npy(path, 'ETTh1inputs.npy', length, strid)
    compute_indicators(data, n_job, name.split('.')[0], path, length, mode)
    recommend_aries(path, name.split('.')[0], query, mode, samples_rate)
    # print(data2.shape)






