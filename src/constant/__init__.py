import os
from datetime import datetime

def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

CURRENT_TIME_STAMP = get_current_time_stamp()


ROOT_DIR = os.getcwd()
CONFIG_PATH = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_PATH,CONFIG_FILE_NAME)


#ingestion variables

INGESTION_CONFIG_KEY = "data_ingestion_config"
DATASET_DOWNLOAD_URL = "dataset_download_url"
DATA_INGESTION_ARTIFACT_DIR = "ingested_data"
RAW_DATA_DIR_KEY = "raw_data_dir"
INGESTED_TRAIN_DIR_KEY = "ingested_train_dir"

# data validation variables
DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_ARTIFACT_DIR = "validated_data"
SCHEMA_DIR_KEY = "schema_dir"
SCHEMA_FILE_NAME_KEY = "schema_file_name"

# Data Transformation related variables
DATA_TRANSFORMATION_CONFIG_KEY = "data_transformation_config"
DATA_TRANSFORMATION_ARTIFACT_DIR = "data_transformation"
DATA_TRANSFORMATION_DIR_NAME_KEY = "transformed_dir"
DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY = "transformed_train_dir"
SCALED_DATA_DIR_NAME_KEY= "scaled_dir"
SCALED_DATA_FILE_NAME_KEY ="scaled_data_file_name"
SCALED_OBJ_FILE_NAME_KEY = "scaled_obj_file_name"
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY = "preprocessing_dir"
DATA_TRANSFORMATION_PREPROCESSING_DATA_FILE_NAME_KEY="preprocessing_df_file_name"
DATA_TRANSFORMATION_PREPROCESSED_OBJ_FILE_NAME_KEY = "preprocessed_object_file_name"

TARGET_COLUMN_KEY = "target_column"
DATASET_SCHEMA_COLUMNS_KEY = "Columns"

PCA_DATA_DIR_NAME_KEY = "pca_data_dir"
PCA_CSV_FILE_NAME_KEY="pca_data_file_name"
PCA_OBJ_FILE_NAME_KEY = "pca_obj_file_name"

MODEL_TRAINER_CONFIG_KEY = "model_trainer_config"
CLUSTER_DIR_NAME_KEY = "cluster_dir"
CLUSTER_FILE_NAME_KEY = "cluster_data_file_name"
TRAINED_MODEL_DIR_NAME_KEY = "trained_model_dir"
TRAINED_MODEL_NAME_KEY = "trained_model_name"
MODEL_TRAINER_ARTIFACT_DIR = "model_dir"
TRAINED_DATA_FILE_NAME_KEY="trained_data_file_name"
TRAINED_OBJ_FILE_NAME_KEY="trained_obj_file_name"
RF_MODEL_DIR ="rf_model_dir"
RF_MODEL = "rf_model.pkl"
 


# Training pipeline related variable
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"

TEST_SIZE:float = 0.33
RANDOM_STATE: float= 42
