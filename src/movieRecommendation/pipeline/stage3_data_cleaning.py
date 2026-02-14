from src.movieRecommendation.config.configuration import ConfigurationManager
from src.movieRecommendation.components.data_preparation import DataPreparation
from src.movieRecommendation.logging import logger


class DataPreparationPipeline:
    def __init__(self):
        pass

    def initiate_data_preparation(self):
        try:
            config = ConfigurationManager()
            data_preparation_config = config.get_data_preparation_config()
            data_preparation = DataPreparation(config=data_preparation_config)
            data_preparation.prepare()
        except Exception as e:
            logger.exception(e)
            raise e
