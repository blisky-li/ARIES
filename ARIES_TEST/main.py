from Stationarity_datasets1 import stationary
from Trendstrength_datasets2 import trend
from Season_datasets3 import season
from Volatillity_datatsets4 import volatillity
from Memory_datasets5 import memory
from Scedasticity_datasets6 import scedasticity
from Anomoly_datasets7 import anomoly
import os
import sys

property_path = 'property_txt' # Source path of Synth's property
log_path = 'Select_Synth' # Source path of ARIES's forecasting performances on Synth
target_path = 'table_use' # Target path of performance records
mediate_path = 'property_performance' # Mediate files for further research; Json files: Model: Batch(B): MAE & MSE performance of each series(N)
save_mediate = False # Save mediate files ?
print_result = True # Print file processes

if not os.path.exists(property_path):
    print(f"Error: Directory does not exist -> {property_path}")
    sys.exit(1)

if not os.path.exists(log_path):
    print(f"Error: Directory does not exist -> {log_path}")
    sys.exit(1)

if save_mediate and not os.path.exists(mediate_path):
    os.makedirs(mediate_path)
elif save_mediate and os.path.exists(mediate_path):
    for filename in os.listdir(mediate_path):
        file_path = os.path.join(mediate_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

if not os.path.exists(target_path):
    os.makedirs(target_path)
else:
    for filename in os.listdir(target_path):
        file_path = os.path.join(target_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

stationary(property_path, log_path, target_path, mediate_path, save_mediate, print_result)
trend(property_path, log_path, target_path, mediate_path, save_mediate, print_result)
season(property_path, log_path, target_path, mediate_path, save_mediate, print_result)
volatillity(property_path, log_path, target_path, mediate_path, save_mediate, print_result)
memory(property_path, log_path, target_path, mediate_path, save_mediate, print_result)
scedasticity(property_path, log_path, target_path, mediate_path, save_mediate, print_result)
anomoly(property_path, log_path, target_path, mediate_path, save_mediate, print_result)





