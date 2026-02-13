import os
import zipfile
import gdown
from src.movieRecommendation.logging import logger
from src.movieRecommendation.entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: "DataIngestionConfig"):
        self.config = config

    def download_data(self):
        if not os.path.exists(self.config.local_data_file):
            logger.info("Downloading dataset from Google Drive...")
            url = f"https://drive.google.com/uc?id={self.config.drive_file_id}"
            gdown.download(url, self.config.local_data_file, quiet=False)
            logger.info("File downloaded successfully!")
        else:
            logger.info(
                f"File already exists at {self.config.local_data_file}. Skipping download."
            )

    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)

        with zipfile.ZipFile(self.config.local_data_file, "r") as zip_ref:
            logger.info(f"Extracting dataset to {unzip_path}...")
            zip_ref.extractall(unzip_path)
            logger.info("Extraction complete.")
