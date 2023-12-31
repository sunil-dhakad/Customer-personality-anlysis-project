import os
import sys
import numpy as np
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from src.pipeline.pipeline import TrainPipeline
from src.constant import *


def main():
    try:
        pipeline = TrainPipeline()
        return pipeline.run_pipeline()
    except Exception as e:
        raise CustomException(e,sys) from e

if __name__=="__main__":
    main()