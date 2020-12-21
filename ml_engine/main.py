from logging import config
import os
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn

import logging
import hydra


logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)




def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


@hydra.main(config_path='conf', config_name='config')
def main(cfg):

    warnings.filterwarnings("ignore")
    np.random.seed(40)

    # Read the wine-quality csv file from the URL
    csv_url = (
        "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    )
    try:
        data = pd.read_csv(csv_url, sep=";")
    except Exception as e:
        logger.exception(
            "Unable to download training & test CSV, check your internet connection. Error: %s", e
        )

    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    alpha = cfg.model.alpha
    l1_ratio = cfg.model.l1_ratio

    mlflow.set_tracking_uri('http://tracking:5000')


    os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://minio:9000"
    os.environ["AWS_ACCESS_KEY_ID"] = "minio-access-key"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "minio-secret-key"


    with mlflow.start_run():
        mlflow.sklearn.autolog()
        
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)
        predicted_qualities = lr.predict(test_x)

        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        print('where to write:', mlflow.get_artifact_uri())

        mlflow.log_artifact(os.path.join(os.getcwd(), '.hydra/config.yaml'))
        mlflow.log_artifact(os.path.join(os.getcwd(), '.hydra/hydra.yaml'))
        mlflow.log_artifact(os.path.join(os.getcwd(), '.hydra/overrides.yaml'))
        mlflow.log_artifact(os.path.join(os.getcwd(), 'main.log'))


if __name__ == "__main__":
    main()
