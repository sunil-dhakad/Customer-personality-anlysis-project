from collections import namedtuple
import os
import sys


DataIngestionConfig = namedtuple("DataIngestionConfig",
                                 ["data_download_url","raw_data_dir","ingested_train_dir"])

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig",["artifact_dir"])