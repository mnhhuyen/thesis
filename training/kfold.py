import os
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from config.config_param import final_data_path

df = pd.read_csv(final_data_path)

target_column = 'target'

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for fold, (train_index, test_index) in enumerate(skf.split(df, df[target_column])):
    
    train_data = df.iloc[train_index]
    test_data = df.iloc[test_index]

    folder_name = f'fold_{fold + 1}'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    train_data.to_csv(f'{folder_name}/train_fold{fold + 1}.csv', index=False)
    test_data.to_csv(f'{folder_name}/test_fold{fold + 1}.csv', index=False)

    print(f'Fold {fold + 1}: Train and test data saved.')
