import os
import sys
import pandas as pd
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging

@dataclass
class DataIngestionConfig:
    train_data_path=os.path.join("artifacts","train.csv")
    raw_data_path=os.path.join("artifacts","raw.csv")

@dataclass
class DataIngestion:
    def __init__(self):
        self.inigestion_config=DataIngestionConfig()
    def initiate_data_ingestion(self):
        logging.info("entering the data ingestion method or component")
        try:
            df=pd.read_csv("data/modified.csv")
            logging.info("read the dataset")
            os.makedirs(os.path.dirname(self.inigestion_config.train_data_path),exist_ok=True)
            """
            'self.inigestion_config.train_data_path'
                contains:"artifacts/train.csv"
                This is the FULL path including:
                    folder name → artifacts
                    file name → train.csv
            'os.path.dirname("artifacts/train.csv")'
                returns:"artifacts"
                Meaning:
                    Give me ONLY the directory/folder name.
                    It removes the filename.
            'os.makedirs("artifacts")'
                creates the folder:artifacts/
            'exist_ok=True'
                if the directory is already present it will not create new folder and give error 
            This line will finally give
                Create the folder where train.csv will be stored, and don't throw error if folder already exists.   
            """
            df.to_csv(self.inigestion_config.raw_data_path,index=False,header=True)
            """
            'df.to_csv(self.inigestion_config.raw_data_path,index=False,header=True)'
                This saves the DataFrame into a CSV file.
            'self.inigestion_config.raw_data_path'
                contains:"artifacts/raw.csv"
                Then this line becomes:df.to_csv("artifacts/raw.csv")
            'index=False'
                By default pandas adds row numbers:,movie_id,title,tags
                                                    0,1,Avatar,action sci-fi
                                                    1,2,Batman,hero dark
                output becomes cleaner:movie_id,title,tags
                                        1,Avatar,action sci-fi
                                        2,Batman,hero dark
            'header=True'
                This writes column names:movie_id,title,tags
            """
            df.to_csv(self.inigestion_config.train_data_path,index=False,header=True)
            logging.info("done dataingestion")
            return(
                self.inigestion_config.raw_data_path,
                self.inigestion_config.train_data_path

            )
            
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    obj.initiate_data_ingestion()