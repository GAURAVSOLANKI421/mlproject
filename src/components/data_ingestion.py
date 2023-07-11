import os 
import sys 
from src.exception import CustomException
from src.logger import loggers
import pandas as pd 
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import Preprocessing
from src.components.data_transformation import Datapreprocessconfig
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path :str = os.path.join('artifact' , 'train.csv')
    test_data_path :str = os.path.join('artifact' , 'test.csv')
    raw_data_path :str = os.path.join('artifact' , 'raw_data.csv')


class DataIngestion:
    def __init__(self):
        self.data_config = DataIngestionConfig()

    def start_ingestion(self):
        loggers.info('reading data from data directory')
        try:
            data = pd.read_csv('notebook/data/stud.csv')
            os.makedirs(os.path.dirname(self.data_config.train_data_path),exist_ok=True)
            loggers.info("Train test split initiated")
            train_set,test_set=train_test_split(data,test_size=0.2,random_state=42)

            train_set.to_csv(self.data_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.data_config.test_data_path,index=False,header=True)

            loggers.info("Inmgestion of the data is completed")
            return (self.data_config.train_data_path,self.data_config.test_data_path )

        except Exception as e:
            loggers.error('failed to ingest data')
            raise CustomException(e,sys)
        


if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.start_ingestion()

    data_transformation=Preprocessing()
    train_arr,test_arr,_=data_transformation.startdatapreprocessing(train_data,test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))
        





# create a artifact folder and set path for train test and raw data
#using dataclass decorator and dataingestion class

# create a dataingestion class and init the config variables 
# def init 
# def initiate_data_ingestion - read data from read_csv







