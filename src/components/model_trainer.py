import os
import sys
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from src.utils import save_objects

@dataclass
class ModelTrainingConfig:
    vectors_path=os.path.join('artifacts','vectors.pkl')
    transformed_movies_path=os.path.join('artifacts','transformed_movies.pkl')
    similarity_path=os.path.join('artifacts','similarity.pkl')

@dataclass
class ModelTraining:
    def __init__(self):
        self.model_trainer_config=ModelTrainingConfig()

    def recommend(self, movie, movies, similarity):

    # Convert to lowercase for matching
        movie = movie.lower()

    # Convert titles to lowercase
        movies["title"] = movies["title"].str.lower()

    # Check movie exists
        if movie not in movies["title"].values:

            print("Movie not found in dataset")
            return

    # Fetch movie index
        movie_index = movies[
            movies["title"] == movie
         ].index[0]

        print(f"\nMovie Index: {movie_index}")

    # Fetch similarity scores
        distances = similarity[movie_index]

        print(f"Total distances: {len(distances)}")

    # Sort similarity scores
        movie_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )[1:6]

        print("\nRecommended Movies:\n")

        for i in movie_list:

         print(
            movies.iloc[i[0]].title
        )
            
    
    def initiate_model_training(self):
        logging.info("initializing training")
        try:
            logging.info("loading path of vectores")
            with open(self.model_trainer_config.vectors_path,'rb')as f:
                vectors=pickle.load(f)
            logging.info("vectors loaded successfully")
            logging.info("loading movies dataframe")
            with open(self.model_trainer_config.transformed_movies_path,"rb") as file:
                movies = pickle.load(file)
            logging.info("loaded movies dataframe successfully")
            similarity=cosine_similarity(vectors)
            save_objects(obj=similarity,file_path=self.model_trainer_config.similarity_path)
            input_movie=input("Enter a movie to give you recommendation: ")
            self.recommend(input_movie,movies,similarity)


        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    trainer = ModelTraining()
    trainer.initiate_model_training()


