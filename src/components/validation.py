from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import DataValidationConfig,DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
import os,sys
import pandas  as pd
from src.utils.utils import read_yaml_file

class Datavalidation:

    def __init__(self,data_validation_config:DataValidationConfig,
                 data_ingestion_config:DataIngestionConfig,
                 data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_config = data_ingestion_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_file_path = self.data_validation_config.schema_file_path
            self.inside_schema = self.read_yaml_file(file_path=self.schema_file_path)

        except Exception as e:
            raise CustomException(e,sys) from e
        
    def file_name_check_func(self,file_name):
        try:
            file_name_status = False
            sample_file_name = self.inside_schema["name"]
            if sample_file_name == file_name:
                file_name_status= True
            return file_name_status
            
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def column_check_func(self,file):
        data = pd.read_csv(file)
        columns = list(data.columns)

        for colm in columns:
            if colm not in self.inside_schema["columns"]:
                raise Exception(f"column : [{colm}] in file :[{file}] not available in schema ")
        return True
    


    def validate_schema_func(self):
        try:
            logging.info(f"validating schema")
            validation_status = False
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]
            data_file_path = os.path.join(raw_data_dir,file_name)

            for file in os.listdir(data_file_path):
                if self.file_name_check_func(file) and self.column_check_func(os.path.join(data_file_path,file)):
                    validation_status=True
            logging.info("validation is completed")
            return validation_status
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def initiate_validation(self)->DataValidationArtifact:
        try:
            self.validate_schema_func()

            data_validation_artifact = DataValidationArtifact(schema_file_path=self.data_validation_config.schema_file_path,
                                                              is_validated=True,
                                                              message="validation successful")
            
            logging.info(f"data_validation_artifact : {data_validation_artifact}")
            return data_validation_artifact
            
        except Exception as e:
            raise CustomException(e,sys) from e

    def __del__(self):
    logging.info(f"\n{'*'*20} Data Validation log completed {'*'*20}\n")


        



