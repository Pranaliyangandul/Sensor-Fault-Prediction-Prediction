import pandas as pd
import numpy as np
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity import config_entity,artifact_entity
import os,sys
from xgboost import XGBClassifier
from sklearn.metrics import f1_score
from sensor import utils 

class ModelTrainer:
    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,data_transformation_artifact:artifact_entity.DataTransformationArtifact) -> None:
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise SensorException(e,sys)
        
    def model_train(self,x,y):
        try:
            xgb=XGBClassifier()
            model=xgb.fit(x,y)
            return model
        except Exception as e:
            raise SensorException(e,sys)
        
    def initiate_model_trainer(self)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Loading train and test array.")
            train_arr=utils.load_numpy_array_data(self.data_transformation_artifact.transformed_train_path)
            test_arr=utils.load_numpy_array_data(self.data_transformation_artifact.transformed_test_path)

            logging.info(f"Splitting input and target feature from both train and test arr.")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            logging.info(f"Train the model")
            model=self.model_train(x_train,y_train)

            logging.info(f"Calculating f1 train score")
            yhat_train=model.predict(x_train)
            f1_train_score=f1_score(y_train,yhat_train)

            logging.info(f"Calculating f1 test score")
            yhat_test=model.predict(x_test)
            f1_test_score=f1_score(y_test,yhat_test)

            if f1_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                expected accuracy: {self.model_trainer_config.expected_score}: model actual score: {f1_test_score}")

            logging.info(f"Checking if our model is overfiiting or not")
            diff = abs(f1_train_score-f1_test_score)

            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score diff: {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")

            #save the trained model
            logging.info(f"Saving mode object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            #prepare artifact
            logging.info(f"Prepare the artifact")
            model_trainer_artifact  = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, 
            f1_train_score=f1_train_score, f1_test_score=f1_test_score)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact

            

        except Exception as e:
            raise SensorException(e,sys)


        

        

