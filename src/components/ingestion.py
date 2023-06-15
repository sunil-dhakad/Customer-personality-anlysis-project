import os
import sys
import numpy as np
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
from src.entity.config_entity  import DataIngestionConfig
from src.entity.artifact_entity  import DataIngestionArtifact
from six.moves import urllib


#fetching to local, saving it 
class DataIngestion:
    def __init__(self,data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        
        
    def download_data(self):
        try:
        
            download_url = self.data_ingestion_config.data_download_url
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            os.makedirs(raw_data_dir, exist_ok=True)
            train_file_name = os.path.basename(download_url)
            raw_train_file_path = os.path.join(raw_data_dir,train_file_name)
        
            urllib.request.urlretrieve(download_url, raw_train_file_path)
            logging.info(f"data downloded")
            return raw_train_file_path
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def savedata(self):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file = os.listdir(raw_data_dir)[0]
            main_file_path = os.path.join(raw_data_dir,file)
            dataframe = pd.read_csv(main_file_path)
        except Exception as e:
            raise CustomException(e,sys) from e
        
        data_ingestion_artifact = DataIngestionArtifact(main_file_path=main_file_path,
                                                            is_ingested=True,
                                                            message=f"Data ingestion completed successfully."
                                                            )
        logging.info(f"ingestion or saving data is done")
        return data_ingestion_artifact
        
        
    def initiate_data_ingestion(self):
        try:
            raw_train_file_path = self.download_data()
            logging.info(f"initiate data ingestion")
            return self.savedata()
        except Exception as e:
            raise CustomException(e, sys)from e
    
    