import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import itertools

from sklearn.metrics import roc_auc_score, balanced_accuracy_score, RocCurveDisplay
from sklearn.metrics import confusion_matrix, accuracy_score, roc_curve, classification_report, ConfusionMatrixDisplay, recall_score, precision_score
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression

from xgboost import XGBClassifier

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import pickle

print("Predicting survival")
print("XGBoost")

pd.set_option('display.max_colwidth', None)

MAIN_DIR = "/media/data3/quangnh/MIMICIV_AKI_AMI/"
TRAIN_FILE = "/media/data/huyennm/mimic-iv/training/fold_1/train_fold1.csv"
TEST_FILE = "/media/data/huyennm/mimic-iv/training/fold_1/test_fold1.csv"

def loading_dataset(): 
    print("\n>>> LOADING TRAIN AND TEST SET")
    train_df = pd.read_csv(TRAIN_FILE)
    test_df = pd.read_csv(TEST_FILE)

    #print(train_df)
    #print(test_df)
    categorical_cols = train_df.select_dtypes(['int64']).columns.to_list()
    categorical_cols.remove('target')
    print("categorical_cols: ", len(categorical_cols))

    num_cols = train_df.columns.to_list()
    #print("num_col: ", len(num_cols))
    num_numerical_cols = [item for item in train_df.columns.to_list() if item not in categorical_cols]
    print("num_numerical_cols: ", len(num_numerical_cols))

    print("train samples: ", train_df.shape[0])
    print("train positive: ", train_df['target'].sum())
    print("train negative: ", train_df.shape[0] - train_df['target'].sum())

    print("test samples: ", test_df.shape[0])
    print("test positive: ", test_df['target'].sum())
    print("test negative: ", test_df.shape[0] - test_df['target'].sum())

    print("Dataset: ", train_df.shape[0] + test_df.shape[0])
    print("Dataset positive: ", train_df['target'].sum() + test_df['target'].sum())
    print("Dataset negative: ", train_df.shape[0] - train_df['target'].sum() + test_df.shape[0] - test_df['target'].sum())

    y_train = train_df['target']
    X_train = train_df.drop('target',axis=1)

    y_test = test_df['target']
    X_test = test_df.drop('target',axis=1)

    print("X_train columns: ", len(X_train.columns.to_list()))
    
    return X_train, y_train, X_test, y_test

def gridsearchcv(param_grid , model, X_train, y_train):
    kf = StratifiedKFold(n_splits = 5, shuffle = True, random_state=42)
    grid = GridSearchCV(model, param_grid, cv=kf, verbose=1, scoring="roc_auc")
    grid_search = grid.fit(X_train, y_train)
    print(grid_search.best_estimator_)
    print("Best Hyperparameters:", grid_search.best_params_)
    print("Best Accuracy:", grid_search.best_score_)
    return grid_search
    
def train_model(X_train, y_train): 
    print("\n>>> TRAIN MODEL")
    
    #model = make_pipeline(StandardScaler(), LogisticRegression(solver='lbfgs', max_iter=1000))
    #model.fit(X_train, y_train)    
        
    #model = XGBClassifier()
    #model.fit(X_train, y_train)
    
    param_grid= {"objective":["binary:logistic"],
                    'colsample_bytree': [0.3, 0.5, 0.7, 1],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'max_depth': [6, 7, 8, 9, 10],
                    'gamma': [0, 0.25, 0.5, 1.0],
                    'reg_lambda': [0, 5, 10, 15, 20],
                    'alpha': [0, 5, 10, 15, 20],
                    'random_state': [42]
                }

    model = gridsearchcv(param_grid, XGBClassifier(), X_train, y_train)
    
    # save
    with open('xgboost_model.pkl','wb') as f:
        pickle.dump(model, f)
    
    return model
    
def test_model(model, X_test, y_test):     
    print("\n>>> TEST MODEL")
    y_predict = model.predict(X_test)
    #print("y_predict: ", y_predict)
    y_predict_proba = model.predict_proba(X_test)[:, 1]
    #print("y_predict_proba: ", y_predict_proba)
    print("y_predict type: ", type(y_predict))
    print("y_predict_proba type: ", type(y_predict_proba))
    
    np.save("xgboost.npy", y_predict, y_predict_proba)
    
    accuracy = accuracy_score(y_test, y_predict)
    print("accuracy", accuracy)
    balanced_accuracy = balanced_accuracy_score(y_test, y_predict)
    print("balanced accuracy:", balanced_accuracy)
    
    auc_score = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    print("AUC: ", auc_score)
    recall = recall_score(y_test, y_predict)
    print("recall: ", recall)
    precision = precision_score(y_test, y_predict)
    print("precision: ", precision)    
        
    tn, fp, fn, tp = confusion_matrix(y_test, y_predict).ravel()
    specificity = tn / (tn+fp)
    print("specificity: ", specificity)
    print("Sensitivity: ", recall)
    
    #print("Accuracy: ", (tp + tn ) / (tp + tn + fp + fn) )
    #print("Precision: ", tp / ( tp + fp ))
    #print("Recall: ", tp / (tp + fn))
    
    F1_Score = 2 * ( ( precision * recall ) / ( precision + recall ) ) 
    print("F1_Score: ", F1_Score)
    
    file_results_summary = open("xgboost_summary.csv", "w")
    file_results_summary.write("Accuracy,balanced_accuracy,AUC,recall,precision,specificity,Sensitivity,F1_Score\n")
    results = '{0:.4f}'.format(accuracy) + "," + '{0:.4f}'.format(balanced_accuracy) + "," + '{0:.4f}'.format(auc_score) + "," + '{0:.4f}'.format(recall) + "," + '{0:.4f}'.format(precision) + "," + '{0:.4f}'.format(specificity) + "," + '{0:.4f}'.format(recall) + "," + '{0:.4f}'.format(F1_Score)
    file_results_summary.write(results)
    file_results_summary.close()
    
def main(): 
    X_train, y_train, X_test, y_test = loading_dataset()
    
    model = train_model(X_train, y_train)
    #with open('rf_model.pkl', 'rb') as f:
    #    model = pickle.load(f)
    test_model(model, X_test, y_test)
    
#############################################
if __name__ == '__main__':
    main()