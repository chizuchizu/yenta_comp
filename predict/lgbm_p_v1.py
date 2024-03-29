import lightgbm as lgb
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle


N_FOLDS = 4

params = {
    'objective': 'multiclass',
    'metric': 'multi_logloss',
    'num_class': 4,
    'learning_rate': 0.1,
    'max_depth': 7,
    'num_leaves': 31,
    'max_bin': 31,
    'colsample_bytree': 0.8,
    'subsample': 0.8,
    'nthread': -1,
    'bagging_freq': 1,
    'verbose': -1,
    'seed': 1,
}

train = pd.read_pickle("../data/train_v1.pkl")
test = pd.read_pickle("../data/test_v1.pkl")
target = pd.read_csv("../data/train.csv")["score"].astype(int)
kfold = KFold(n_splits=N_FOLDS, shuffle=True, random_state=24)
pred = np.zeros((test.shape[0], 4))
for fold, (train_idx, valid_idx) in enumerate(kfold.split(train, target)):
    print(fold + 1)
    x_train, x_valid = train.loc[train_idx], train.loc[valid_idx]
    y_train, y_valid = target[train_idx], target[valid_idx]

    d_train = lgb.Dataset(x_train, label=y_train)
    d_valid = lgb.Dataset(x_valid, label=y_valid)
    estimator = pickle.load(open(f"../models/lgbm_v1_{fold}.pkl", "rb"))

    y_pred = estimator.predict(test)
    pred += y_pred / N_FOLDS

ss = pd.read_csv("../data/test.csv")
ss["score"] = np.argmax(pred, axis=1).astype(float)
ss.to_csv("../outputs/lgbm_v1_1.csv", index=False)
print()
