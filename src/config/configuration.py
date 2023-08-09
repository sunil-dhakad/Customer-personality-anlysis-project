import os
import sys
from src.constant import *
from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import *
from src.utils.utils import read_yaml_file
from src.entity.config_entity import DataValidationConfig,DataIngestionConfig
from src.entity.artifact_entity import DataTransformationArtifact,DataIngestionArtifact
import pandas as pd
import numpy as np


class Configuration:

    def __init__(self,config_file_path:str =CONFIG_FILE_PATH,
                 current_time_stamp:str = CURRENT_TIME_STAMP) -> None:
        try:
            self.config_info  = read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise CustomException(e,sys) from e


    def get_data_ingestion_config(self) ->DataIngestionConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir=os.path.join(
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
            )
            data_ingestion_info = self.config_info[INGESTION_CONFIG_KEY]

            dataset_download_url = data_ingestion_info[DATASET_DOWNLOAD_URL]

            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[RAW_DATA_DIR_KEY]
            )

            ingested_train_data_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[INGESTED_TRAIN_DIR_KEY]
            )
        

            data_ingestion_config=DataIngestionConfig(
                dataset_download_url=dataset_download_url,
                raw_data_dir=raw_data_dir, 
                ingested_train_dir= ingested_train_data_dir)
            
            logging.info(f"Data Ingestion config: {data_ingestion_config}")
            return data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys) from e




    def get_data_validation_config(self)->DataValidationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            data_validation_artifact_dir = os.path.join(artifact_dir,
                                                        DATA_VALIDATION_ARTIFACT_DIR,
                                                        self.time_stamp)
            
            data_validation_config = self.config_info[DATA_VALIDATION_CONFIG_KEY]

            schema_file_path = os.path.join(ROOT_DIR,
                                            data_validation_config[SCHEMA_DIR_KEY],
                                            data_validation_artifact_dir[SCHEMA_FILE_NAME_KEY])
            
            data_validation_config = DataValidationConfig(schema_file_path=schema_file_path)


            return data_validation_config

        except Exception as e:
            raise CustomException(e,sys) from e
    def get_data_transformation_config(self)->DataTransformationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_transformation_artifact_dir = os.path.join(artifact_dir,
                                                            DATA_TRANSFORMATION_ARTIFACT_DIR,
                                                            self.time_stamp)
            data_transformation_config = self.config_info(DATA_TRANSFORMATION_CONFIG_KEY)
            preproccessing_obj_file_path = os.path.join(
                                                        data_transformation_artifact_dir,
                                                        data_transformation_config[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY],
                                                        data_transformation_config[DATA_TRANSFORMATION_PREPROCESSING_DATA_FILE_NAME_KEY])

            scaled_obj_file_path = os.path.join(
                                                data_transformation_artifact_dir,
                                                data_transformation_config[SCALED_DATA_DIR_NAME_KEY],
                                                data_transformation_config[SCALED_DATA_FILE_NAME_KEY])

            pca_obj_file_path =os.path.join(data_transformation_artifact_dir,
                                             data_transformation_config[PCA_DATA_DIR_NAME_KEY],
                                             data_transformation_config[PCA_DATA_FILE_NAME_KEY])   
            
 
            transformed_train_dir=os.path.join(
                                                data_transformation_artifact_dir,
                                    data_transformation_config[DATA_TRANSFORMATION_DIR_NAME_KEY],
                                    data_transformation_config[DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY])                                

            
            data_transformation_config = DataTransformationConfig(transformed_train_dir=transformed_train_dir,
                                                                  scalling_obj_file_path=scaled_obj_file_path,
                                                                  preprocessing_obj_file_path=preproccessing_obj_file_path,
                                                                  pca_obj_file_path=pca_obj_file_path)
                                                                  
        except Exception as e:
            raise CustomException(e,sys) from e 




    def get_model_trainer_config(self)->ModelTrainerConfig:
        try:
            
            artifact_dir = self.training_pipeline_config.artifact_dir
            model_trainer_artifact_dir = os.path.join(artifact_dir,
                                                            MODEL_TRAINER_ARTIFACT_DIR,
                                                            self.time_stamp)
            
            model_trainer_config = self.config_info[MODEL_TRAINER_CONFIG_KEY]
            data_transformation_config = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]

            pca_data = os.path.join(artifact_dir,model_trainer_artifact_dir,
                                    data_transformation_config[PCA_DATA_DIR_NAME_KEY],
                                    data_transformation_config[PCA_CSV_FILE_NAME_KEY])

            cluster_data_file_path =os.path.join(model_trainer_artifact_dir,
                                                  model_trainer_config[CLUSTER_DIR_NAME_KEY],
                                                  model_trainer_config[CLUSTER_FILE_NAME_KEY])       
           
            trained_model_dir = os.path.join(artifact_dir,MODEL_TRAINER_ARTIFACT_DIR,
                                             model_trainer_config[TRAINED_MODEL_DIR_NAME_KEY])
            
            trained_model_name = model_trainer_config[TRAINED_MODEL_NAME_KEY]
            rf_model_dir = model_trainer_config[RF_MODEL_DIR]
            rf_model = model_trainer_config[RF_MODEL]



            model_trainer_config = ModelTrainerConfig(
                                    pca_data=pca_data,
                                    cluster_data_file_path=cluster_data_file_path,
                                    trained_model_dir=trained_model_dir,
                                    trained_model_name=trained_model_name,
                                    rf_model_dir=rf_model_dir,
                                    rf_model=rf_model)

        except Exception as e:
            raise CustomException(e,sys) from e

         
    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            

            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipleine config: {training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise CustomException(e,sys) from e
        