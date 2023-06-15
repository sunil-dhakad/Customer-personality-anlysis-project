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
from collections import namedtuple
from datetime import date
from src.config.configuration import Configuration
from src.components.ingestion import DataIngestion

class Pipeline():
    
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
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise CustomException(e,sys) from e