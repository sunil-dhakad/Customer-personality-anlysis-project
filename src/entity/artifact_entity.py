from collections import namedtuple
import os
import sys


DataIngestionArtifact = namedtuple("DataIngestionArtifact", 
                                   ["main_file_path","is_ingested", "message"])

DataValidationArtifact = namedtuple("DataValidationArtifact",
                                    ["schema_file_path","is_validated","message"])


DataTransformationArtifact = namedtuple("DataTransformationArtifact",["preprocessing_data_file_path",
                                                                       "preprocessing_obj_file_path",
                                                                       "scalling_data_file_path",
                                                                       "scalling_obj_file_path",
                                                                       "pca_file_path",
                                                                       "pca_obj_file_path"
                                                                       ])

ModelTrainerArtifact = namedtuple("ModelTrainerArtifact",[
                                                        "model_kmeans"
                                                      "cluster_data_dir",
                                                      "rf_model",
                                                      "result"])