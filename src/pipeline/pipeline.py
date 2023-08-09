import os
import sys
import numpy as np
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
from src.entity.config_entity  import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from src.entity.artifact_entity  import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from six.moves import urllib
from collections import namedtuple
from datetime import date
from src.config.configuration import Configuration
from src.components.ingestion import DataIngestion
from src.components.validation import Datavalidation
from src.components.transform import transform
from src.components.model_trainer import Model_trainer


    
class TrainPipeline:
    is_pipeline_running = False
    def __init__(self):
        try:
            self.training_pipline_config = TrainingPipelineConfig()
        except Exception as e:
            raise e     



    def __init__(self,config:Configuration = Configuration())->None:
        try:
            self.config = config
        except Exception as e:
            raise CustomException(e,sys) from e
        
        
        
    def start_data_ingestion(self):
        
        try:
            data_ingestion = DataIngestion(data_ingestion_config = self.config)
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise CustomException(e,sys) from e 
        

    def start_validation(self,data_ingestion_config:DataIngestion,
                            data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation = Datavalidation(data_validation_config=self.config.get_data_validation_config(),
                                             data_ingestion_config = data_ingestion_config,
                                             data_ingestion_artifact=data_ingestion_artifact)
            

            return data_validation.initiate_validation()
        except Exception as e:
            raise CustomException(e,sys) from e


    def start_transformation(self,data_ingestion_artifact:DataIngestionArtifact,
                                data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
    
        try:
            data_transformation = transform(
                data_transformation_config = self.config.get_data_transformation_config(),
                data_ingestion_artifact = data_ingestion_artifact,
                data_validation_artifact = data_validation_artifact)

            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise CustomException(e,sys) from e


    def start_model_training(self,data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer = Model_trainer(model_trainer_config=self.config.get_model_trainer_config(),
                                        data_transformation_artifact=data_transformation_artifact)   

            return model_trainer.initiate_model_training()
        except Exception as e:
            raise CustomException(e,sys) from e               



    def run_pipeline(self):
        try:
            data_ingestion_config=self.config.get_data_ingestion_config()

            data_ingestion_artifact = self.start_data_ingestion()

            data_validation_artifact = self.start_validation(data_ingestion_config=data_ingestion_config,
                                                            data_ingestion_artifact=data_ingestion_artifact)

            data_transformation_artifact = self.start_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                             data_validation_artifact=data_validation_artifact)

            model_trainer_artifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)         
        except Exception as e:
            raise CustomException(e,sys) from e

    def __del__(self):
        logging.info(f"\n{'*'*20} Training Pipeline Complete {'*'*20}\n\n")









