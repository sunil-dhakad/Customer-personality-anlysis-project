import os
import sys
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.logger import logging
from sklearn.cluster import KMeans
from sklearn import metrics
from src.exception import CustomException
from src.config.configuration import Configuration
from src.components.transform import DataTransformationConfig
from src.entity.artifact_entity import  DataTransformationArtifact,ModelTrainerArtifact
from src.entity.config_entity import DataTransformationConfig,ModelTrainerConfig
import pandas as pd
from src.constant import *
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


class Model_trainer:
    def __init__(self,
                config=Configuration(),
                data_transformation_config=DataTransformationConfig,
                data_transformation_artifact=DataTransformationArtifact):
        try:
            self.model_trainer_config = config.get_model_trainer_config()
            self.data_transformation_config = data_transformation_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys) from e
        

    def trainer(self):
        try:
            data=pd.read_csv(self.model_trainer_config.pca_data)

            '''
            range111 = range(1,11)
            wcss = []
            silhoutrange = []

            for i in range111:
                kmodel=KMeans(n_clusters=i,init="k-means++",random_state=42)
                kmodel.fit(data)

                wcss.append(kmodel.inertia_)
                silhoutrange.append(metrics.silhouette_score(data,kmodel.labels_))
            os.makedirs(self.model_trainer_config.trained_model_dir,exist_ok=True)
            plt.plot(range111,wcss)
            image_name=os.path.join(self.model_trainer_config.trained_model_dir,"elbow_plot.png")
            plt.save_fig(image_name)
            '''

            model=KMeans(n_clusters=5,init="k-means++",random_state=42)
            model.fit(data)

            #saving model object
            os.path.join(self.model_trainer_config.trained_model_dir,exist_ok=True)
            model_kmeans = os.path.join(self.model_trainer_config.trained_model_dir,
                                    self.model_trainer_config.trained_model_name)
            
            pickle.dump(model_kmeans,wb)
            logging.info(f"saving model in : {model_kmeans}")

            data["clustercolm"]= model.fit_predict(data)

            cluster_data_dir = self.model_trainer_config.cluster_data_dir
            cluster_data_dir = os.path.dirname(cluster_data_dir)
            os.makedirs(cluster_data_dir, exist_ok=True)
            data.to_csv(cluster_data_dir, header=True, index=False)


            #saving data and model as above

            X = data.drop(["clustercolm"],axis=1)
            Y = data["clustercolm"]

            x_train,xtest,ytrain,ytest = train_test_split(X,Y,test_size=TEST_SIZE,random_state=RANDOM_STATE)
            random_forest = RandomForestClassifier()
            random_forest.fit(x_train,ytrain)
            
            os.path.join(self.model_trainer_config.rf_model_dir,exist_ok=True)
            rf_model = os.path.join(self.model_trainer_config.rf_model_dir,
                                    self.model_trainer_config.rf_model)
            pickle.dump(rf_model,wb)
            logging.info(f"saving model in {rf_model}")

            ytrain_predicted = random_forest.predict(x_train)
            ytest_predicted= random_forest.predict(ytest)

            list_of_cluster = data['clustercolm'].unique()
            no_of_cluster = len(list_of_cluster)
            result = f"total {no_of_cluster} found in data after pca"
            logging.info(result)

            accuracy_score = accuracy_score(y_true=ytrain, y_pred=ytrain_predicted)*100
            print(f"accuracy score is {accuracy_score}")
            logging.info(f"accuracy score is {accuracy_score}")

            model_trainer_artifact = ModelTrainerArtifact(cluster_data_dir=cluster_data_dir,
                                                          model_kmeans=model_kmeans,
                                                          rf_model=rf_model,
                                                          result=result
                                                          )
            
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
           



            return model_trainer_artifact
        
        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_model_training(self)->ModelTrainerArtifact:
        try:

            data=pd.read_csv(self.model_trainer_config.pca_data)

            self.trainer()
        except Exception as e:
            raise CustomException(e.sys) from e








 











































 '''   def start_clustering_the_dataset(self, dataframe:pd.DataFrame):
        try:
            #Initiating the Agglomerative Clustering model 
            AC = AgglomerativeClustering(n_clusters=4)
            # fit model and predict clusters
            yhat_AC = AC.fit_predict(dataframe)
            dataframe["Clusters"] = yhat_AC
            #saving cluster data
            cluster_data_path = self.data_transformation_config.cluster_data_file_path
            os.makedirs(os.path.dirname(cluster_data_path))
            dataframe.to_csv(cluster_data_path,header=True, index=False)
            print(f"clusters dataset saved , there are {dataframe['Clusters'].unique()} clusters in total")
            logging.info(f"clusters dataset saved , there are {dataframe['Clusters'].unique()} clusters in total")
        except Exception as e:
            raise CustomException(e,sys) from e 

'''