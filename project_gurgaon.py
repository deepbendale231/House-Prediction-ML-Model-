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



#1 Load your dataset
housing = pd.read_csv(r"C:\Users\deepb\Desktop\gurgaon city price prediction\data\housing.csv")

#2 Create a stratified test set meaning we will split the data based on income category
housing["income_cat"] = pd.cut(
    housing["median_income"],
    bins=[0., 1.5, 3.0, 4.5, 6.0, float("inf")],
    labels=[1, 2, 3, 4, 5]
)
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42) # random_state for reproducibility and n_splits=1 means we want only one split

for train_index, test_index in split.split(housing, housing["income_cat"]): # what we are doing here is splitting based on income category
    strat_train_set = housing.loc[train_index].drop("income_cat", axis=1) # drop income_cat column after the split
    strat_test_set = housing.loc[test_index].drop("income_cat", axis=1) 

# we will work on training set
housing = strat_train_set.copy()

#3 Seperate features and labels (features means independent variables and labels means dependent variable)
# we did this because we want to preprocess features only
housing_labels = housing["median_house_value"].copy()
housing = housing.drop("median_house_value", axis=1) 

#4 seperate numerical and categorical columns
num_attributes = housing.drop("ocean_proximity", axis=1).columns.tolist()
cat_attributes = ["ocean_proximity"]

#5 Create pipelines for numerical 
num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")), # step 1: impute missing values with median
    ("scaler", StandardScaler()), # step 2: standardize features
])

# 6 Create pipelines for categorical attributes
cat_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")), # step 1: impute missing values with most frequent value
    ("onehot", OneHotEncoder()), # step 2: one hot encode categorical attributes
])

# CONSTRUCT THE FULL PIPELINE
full_pipeline = ColumnTransformer([
    ("num", num_pipeline, num_attributes), # apply num_pipeline to numerical attributes
    ("cat", cat_pipeline, cat_attributes), # apply cat_pipeline to categorical attributes
])

#6 Transform the data using the full pipeline
housing_prepared = full_pipeline.fit_transform(housing)
print(housing_prepared)

#7 Train and evaluate different models
lin_reg = LinearRegression()
lin_reg.fit(housing_prepared, housing_labels) 
#lin_rmse = root_mean_squared_error(housing_labels, lin_reg.predict(housing_prepared)) # lin_reg is used to make predictions on training data itself
# lin_rmse is the training error 
lin_rmses= -cross_val_score(lin_reg, housing_prepared, housing_labels,
                           scoring="neg_mean_squared_error", cv=10)
print(pd.Series(lin_rmses).describe())

# Decision Tree model 
tree_reg = DecisionTreeRegressor()
tree_reg.fit(housing_prepared, housing_labels)
#tree_rmse = root_mean_squared_error(housing_labels, tree_reg.predict(housing_prepared))
tree_rmses= -cross_val_score(tree_reg, housing_prepared, housing_labels,
                           scoring="neg_mean_squared_error", cv=10)
print(pd.Series(tree_rmses).describe())

# Random Forest model
forest_reg = RandomForestRegressor()
forest_reg.fit(housing_prepared, housing_labels)
#forest_rsme = root_mean_squared_error(housing_labels, forest_reg.predict(housing_prepared))
forest_rsmes= -cross_val_score(forest_reg, housing_prepared, housing_labels,
                           scoring="neg_mean_squared_error", cv=10)
print(pd.Series(forest_rsmes).describe())
# After evaluating we can see that Random Forest is performing the best among all three models

