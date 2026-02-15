from src.movieRecommendation.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from src.movieRecommendation.entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataPreparationConfig,
    ModelTrainerConfig,
)
from src.movieRecommendation.utils.common import read_yaml, create_directories
from pathlib import Path


class ConfigurationManager:
    def __init__(self, config_path=CONFIG_FILE_PATH, params_path=PARAMS_FILE_PATH):
        self.config = read_yaml(config_path)
        self.params = read_yaml(params_path)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            drive_file_id=config.drive_file_id,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir,
        )
        return data_ingestion_config

    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        create_directories([config.root_dir])
        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir, data_path=config.data_path
        )
        return data_transformation_config

    def get_data_preparation_config(self) -> DataPreparationConfig:
        config = self.config.data_preparation
        create_directories([config.root_dir])
        data_preparation_config = DataPreparationConfig(
            root_dir=config.root_dir, data_path=config.data_path
        )
        return data_preparation_config

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        create_directories([config.root_dir])
        model_trainer_config = ModelTrainerConfig(
            root_dir=Path(config.root_dir),
            data_path=Path(config.data_path),
            model_name=config.model_name,
            model_path=Path(config.model_path),
        )
        return model_trainer_config
