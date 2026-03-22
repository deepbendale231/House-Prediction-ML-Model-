import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error 
from sklearn.model_selection import cross_val_score

model_filename = "model.pkl"
pipeline_filename = "pipeline.pkl"

def build_pipeline(num_attributes, cat_attributes):
    # Create pipelines for numerical 
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")), # step 1: impute missing values with median
        ("scaler", StandardScaler()), # step 2: standardize features
    ])

    # Create pipelines for categorical attributes
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")), # step 1: impute missing values with most frequent value
        ("onehot", OneHotEncoder()), # step 2: one hot encode categorical attributes
    ])

    # CONSTRUCT THE FULL PIPELINE
    full_pipeline = ColumnTransformer([
        ("num", num_pipeline, num_attributes), # apply num_pipeline to numerical attributes
        ("cat", cat_pipeline, cat_attributes), # apply cat_pipeline to categorical attributes
    ])
    
    return full_pipeline

if not os.path.exists(model_filename): # Check if model and pipeline files exist(in easy words if they have been saved previously)
    # LETS TRAIN THE MODEL
    housing = pd.read_csv(r"C:\Users\deepb\Desktop\gurgaon city price prediction\data\housing.csv")
    housing["income_cat"] = pd.cut(
        housing["median_income"],
        bins=[0., 1.5, 3.0, 4.5, 6.0, float("inf")],
        labels=[1, 2, 3, 4, 5]
    )

    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

    for train_index, test_index in split.split(housing, housing["income_cat"]):
        housing.loc[test_index].drop("income_cat", axis=1).to_csv('input.csv', index=False) # saving test set for future evaluation
# we drop income_cat column after the split because it was only needed for stratified splitting
        housing = housing.loc[train_index].drop("income_cat", axis=1)
        
        housing_labels = housing["median_house_value"].copy()
        housing_features = housing.drop("median_house_value", axis=1)    

    num_attributes = housing_features.drop("ocean_proximity", axis=1).columns.tolist()
    cat_attributes = ["ocean_proximity"]

    pipeline = build_pipeline(num_attributes, cat_attributes)
    housing_prepared = pipeline.fit_transform(housing_features)

    model = RandomForestRegressor()
    model.fit(housing_prepared, housing_labels)

    joblib.dump(model, model_filename) # save the trained model
    joblib.dump(pipeline, pipeline_filename) # save the pipeline
    print ("Model and pipeline have been trained and saved.")

else:
    # lets do inference ( inference means making predictions on new data using the trained model)
    model = joblib.load(model_filename) # load the trained model
    pipeline = joblib.load(pipeline_filename) # load the pipeline

    input_data = pd.read_csv('input.csv')
    transformed_data = pipeline.transform(input_data) # preprocess the input data
    predictions = model.predict(transformed_data) # make predictions
    print("Predictions:", predictions)  
    input_data['median_house_value'] = predictions

    input_data.to_csv('output.csv', index=False)
    print("Predictions saved to output.csv") 


         
