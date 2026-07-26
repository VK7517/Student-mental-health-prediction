import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler , LabelEncoder , OneHotEncoder

def get_preprocessor(X):
    num_cols = X.select_dtypes(["int","float"]).columns
    cat_cols = X.select_dtypes("object").columns
    num_transformer = Pipeline([
        ("scaler",StandardScaler())   
    ])

    cat_transformer = Pipeline([
        ("encoder",OneHotEncoder(handle_unknown="ignore"))
    ])
    preprocessor = ColumnTransformer([
        ("num",num_transformer,num_cols),
        ("cat",cat_transformer,cat_cols)
    ])
    return preprocessor