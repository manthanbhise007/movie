import os
import sys
import pickle
import pandas as pd
from dataclasses import dataclass

from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer

from src.exception import CustomException
from src.logger import logging

from src.utils import save_objects

@dataclass
class DataTransfomationConfig:
    processed_data_path: str=os.path.join('artifacts',"train.csv")

    vectorizer_path: str=os.path.join('artifacts','vector.pkl')

    vectors_path:str=os.path.join('artifacts','vectors.pkl')

    transformed_movies_path:str=os.path.join('artifacts','transformed_movies.pkl')

@dataclass
class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransfomationConfig()

    def stem_text(self,text):
        ps=PorterStemmer()
        if not isinstance(text, str):
            return ""
        y=[]
        for word in text.split():
            y.append(ps.stem(word))
        return " ".join(y)
    
    def initiate_data_transformation(self):
        logging.info("initiating data transformation")

        try:
            logging.info("Loading processed dataset")
            movies=pd.read_csv(self.data_transformation_config.processed_data_path)
            required_columns = ["movie_id", "title", "tags"]
            for col in required_columns:
                if col not in movies.columns:
                    raise Exception(f"Missing required column: {col}")
            logging.info("All required columns are present")
            movies["tags"] = movies["tags"].apply(self.stem_text)
            cv = CountVectorizer(max_features=5000,stop_words="english")
            vectors = cv.fit_transform(movies["tags"]).toarray()
            os.makedirs("artifacts", exist_ok=True)
            save_objects(obj=cv,file_path=self.data_transformation_config.vectorizer_path)
            save_objects(obj=vectors,file_path=self.data_transformation_config.vectors_path)
            save_objects(obj=movies,file_path=self.data_transformation_config.transformed_movies_path)
            return (
                self.data_transformation_config.transformed_movies_path,
                self.data_transformation_config.vectors_path
            )
        except Exception as e:
            raise CustomException(e,sys)