import yaml,sys
import numpy as np
import os, sys
import numpy as np
import dill
import pandas as pd
from src.constant import *
from src.exception import CustomException








def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e,sys) from e