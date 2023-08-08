from collections import namedtuple
import os
import sys


DataIngestionConfig = namedtuple("DataIngestionConfig",
                                 ["dataset_download_url",
                                 "raw_data_dir",
                                 "ingested_train_dir"])

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig",["artifact_dir"])


DataValidationConfig = namedtuple("DataValidationConfig",
                                  ["schema_file_path"])

DataTransformationConfig = namedtuple("DataTransformationConfig",
                                      ["transformed_train_dir",
                                       "preprocessing_obj_file_path",
                                       "scalling_obj_file_path",
                                       "pca_obj_file_path"])


ModelTrainerConfig = namedtuple("ModelTrainerConfig",["pca_data",
                                                      "trained_model_dir",
                                                      "trained_model_name",
                                                      "cluster_data_dir",
                                                      "cluster_file",
                                                      "rf_model_dir",
                                                      "rf_model"])