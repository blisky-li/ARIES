from recommend_testc.recommend import recommend
from recommend_testc.recommend_validation import recommend_validation

target_dataset = 'PEMS08'
recommend_metrics = 'mae'
recommend_mode = 'large'
samples_rate = 1
recommend_validation(target_dataset, recommend_metrics, recommend_mode, samples_rate)
# recommend(target_dataset, recommend_metrics, recommend_mode, samples_rate)

