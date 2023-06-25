import pandas as pd
import numpy as np
import sys
import os
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder , StandardScaler
from src.exception import CustomException
from src.logger import loggers
from dataclasses import dataclass
from src.utils import Saveobj

@dataclass
class Datapreprocessconfig:
    preprocessor_path = os.path.join('artifact','preprocessor.pkl')
    train_data_path :str = os.path.join('artifact' , 'train.csv')

class Preprocessing:
    def __init__(self):
        self.preprocessor_path = Datapreprocessconfig()

    def dataprocessorobj(self):
        """ 
        This function does data transforation
        """
        try:
            loggers.info('transformation started')
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            numerical_pipelines = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ('scaler',StandardScaler(with_mean=False))
                ]
            )

            categorical_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder',OneHotEncoder()),
                    ('scaler',StandardScaler(with_mean=False))
                ]
            )
            loggers.info('transformation completed')
            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline',numerical_pipelines,numerical_columns),
                    ('cat_pipeline',categorical_pipeline,categorical_columns)
                ]
                
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
    def startdatapreprocessing(self, train_path , test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            loggers.info("Read train and test data completed")

            loggers.info("Obtaining preprocessing object")

            preprocessing_obj=self.dataprocessorobj()

            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            loggers.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            loggers.info(f"Saved preprocessing object.")

            Saveobj.save_obj(

                file_path=self.preprocessor_path.preprocessor_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.preprocessor_path.preprocessor_path,
            )
        except Exception as e :
            raise CustomException(e,sys)


            


