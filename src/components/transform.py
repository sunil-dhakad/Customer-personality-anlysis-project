
#filling nan values
#mersing some row
from src.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact,DataIngestionArtifact
from src.entity.config_entity import DataTransformationConfig
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder 
import os,sys
from src.utils.utils import save_object,load_data, wrapper
from src.logger import logging
from src.exception import CustomException 
from sklearn.decomposition import PCA



class transform:

    def __init__(self, data_transformation_config:DataTransformationConfig,
                        data_validation_artifact:DataValidationArtifact,
                        data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys) from e

    

    def preprocess_and_encode_data(self):
        try:
            # loading all the data

            file_path = self.data_ingestion_artifact.main_file_path
            schema_file_path = self.data_validation_artifact.schema_file_path

            df = load_data(file_path=file_path,
                            schema_file_path=schema_file_path)
            
#   #    #    #Droping null
            df.dropna(inplace=True)
            # Creating age columns
            df['Age'] = 2015 - df['Year_Birth']
#    #     #      # Creating age group 
            df.loc[df['Age'] <=19, "AgeGroup"] = "Teen"
            df.loc[(df['Age'] >=20) & (df['Age'] <= 39), "AgeGroup"] = "Adults"
            df.loc[(df['Age'] >=40) & (df['Age'] <= 65), "AgeGroup"] = "Middle Age Adults"
            df.loc[(df['Age'] >= 66), "AgeGroup"] = "Seniors"

 #   #   # #Creating some extra columns by aggregating them
            df['TotalSpendings'] = df['MntFruits'] + df['MntWines'] + df['MntMeatProducts'] + df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds']
            df['Children'] = df['Kidhome'] + df['Teenhome']

            df.Marital_Status = df.Marital_Status.replace({
                "Together" : "Married",
                "Divorced" : "Single",
                "Widow" : "Single",
                "Alone" : "Single",
                "Absurd" : "Single",
                "YOLO" : "Single"
            })

#    #    #    #Converting to datetime
            df.Dt_Customer = pd.to_datetime(df.Dt_Customer)

            
 #   #    #    # MonthEnrollement
            df['MonthEnrollement'] = (2015 - df.Dt_Customer.dt.year) * 12 + (1 - df.Dt_Customer.dt.month)

#    #    #    #Droping outliers from Age & Income
            df = df[df['Age'] < 100]
            df = df[df['Income'] < 110000]
            logging.info(f" checking shape: {df.shape}")

            df = df.drop(
                [
                'ID', 'Year_Birth', 'Kidhome', 
                'Teenhome', 'Dt_Customer', 'MntWines', 'MntFruits', 'MntMeatProducts',
                    'MntFishProducts', 'MntSweetProducts','MntGoldProds','NumDealsPurchases',
                    'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases','NumWebVisitsMonth',
                    'AcceptedCmp3','AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1',
                    'AcceptedCmp2', 'Complain', 'Z_CostContact', 'Z_Revenue', 'Response','AgeGroup'
                ],
                
                axis = 1)
            
             #Get list of categorical variables
            s = (df.dtypes == 'object')
            object_cols = list(s[s].index)

            print("Categorical variables in the dataset:", object_cols)

            LE_1 = LabelEncoder()
            LE_2 = LabelEncoder()
            LE_3 = LabelEncoder()
            df['Education'] = LE_1.fit_transform(df['Education'])
            df['Living_With'] = LE_2.fit_transform(df['Living_With'])
            df['Marital_Status'] = LE_3.fit_transform(df['Marital_Status'])
            LE = wrapper(LE_1, LE_2,LE_3)
                
            print("All features are now numerical")

            #saving the preprocessed andencoded data
            saving_file_path = self.data_transformation_config.preprocessing_data_file_path
            os.makedirs(os.path.dirname(saving_file_path), exist_ok= True)
            df.to_csv(saving_file_path, header=True , index=False)
            logging.info(f"label_encoded_preprocessed file saved in {saving_file_path}")
            # 3 label encodeding  object saving
            label_encodeding_obj_file_path = self.data_transformation_config.preprocessing_obj_file_path
            logging.info(f"encoded obj saved in {label_encodeding_obj_file_path}")
            save_object(label_encodeding_obj_file_path, LE)
            return df
    
        except Exception as e:
            raise CustomException(e, sys) from e
        


 #   #      # scaling df   
    def scaling_the_encoded_dataset(self, dataframe: pd.DataFrame):
        try:
            dataframe = dataframe.dropna()
            scaler = StandardScaler()
            scaler.fit(dataframe)
            scaled_data = pd.DataFrame(scaler.transform(dataframe),columns= dataframe.columns)
            print("All features are now scaled")

            #saving the scaled dataset
            save_scaled_file_path = self.data_transformation_config.scalling_data_file_path
            os.makedirs(os.path.dirname(save_scaled_file_path), exist_ok=True)
            scaled_data.to_csv(save_scaled_file_path, header=True, index=False)
            #saving the scaled obj


            scaled_obj_file_path = self.data_transformation_config.scalling_obj_file_path
            logging.info(f"scaled data saved in {save_scaled_file_path}")
            save_object(scaled_obj_file_path, scaler)
        except Exception as e:
            raise CustomException(e,sys)
#   #   # Applying PCA
    def start_pca(self, dataframe:pd.DataFrame)->pd.DataFrame:
        try:
            pca = PCA(n_components=6)
            pca.fit(dataframe)
            PCA_data = pd.DataFrame(pca.transform(dataframe), columns=(["col1","col2", "col3","col4","col5","col6"]))
            PCA_data.describe().T
            #saving pca dataset
            pca_file_path = self.data_transformation_config.pca_data_dir
            os.makedirs(os.path.dirname(pca_file_path), exist_ok=True)
            PCA_data.to_csv(pca_file_path, header=True, index=False)
            print("pca dataset saved")
            #saving pca obj file

            pca_obj_file_path = self.data_transformation_config.pca_obj_file_path
            os.makedirs(os.path.dirname(pca_obj_file_path), exist_ok=True)
            save_object(pca_obj_file_path,obj=pca)
            logging.info(f"Pca object saved in {pca_obj_file_path}")
            logging.info(f"pca dataset saved in {pca_obj_file_path}")
            return PCA_data
        except Exception as e:
            raise CustomException(e,sys) from e





    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            inital_data = self.data_ingestion_artifact.main_file_path
            inital_data_df0 = pd.read_csv(inital_data)
            print("encoding started")
            logging.info("encoding the categorical columns")
            preprocessed_encoded_df1 = self.preprocess_and_encode_data(inital_data_df0)
            logging.info("scaling the dataset")
            preprocessed_df2 = self.scalling_the_encoded_dataset(preprocessed_encoded_df1)
            pca_df3 = self.start_pca(dataframe=preprocessed_df2)

            self.start_clustering_the_dataset(pca_df3)



            scaled_obj_file_path = self.data_transformation_config.scalling_obj_file_path
            label_encodeding_obj_file_path = self.data_transformation_config.preprocessing_obj_file_path
         



            data_transformation_artifact = DataTransformationArtifact(
                            preprocessing_data_file_path=preprocessed_encoded_df1,
                            preprocessing_obj_file_path=self.data_transformation_config.preprocessing_obj_file_path, 
                            scalling_data_file_path=preprocessed_df2,
                            scalling_obj_file_path=self.data_transformation_config.scalling_obj_file_path,
                            pca_data_file_path=pca_df3,
                            pca_obj_file_path=self.data_transformation_config.pca_obj_file_path)
                           
            
            
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys) from e 


