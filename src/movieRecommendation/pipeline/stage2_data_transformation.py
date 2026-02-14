from src.movieRecommendation.config.configuration import ConfigurationManager
from src.movieRecommendation.components.data_transformation import DataTransformation
from src.movieRecommendation.logging import logger


class DataTransformationPipeline:
    def __init__(self):
        pass

    def initiate_data_transformation(self):
        try:
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            data_transformation = DataTransformation(config=data_transformation_config)
            data_transformation.transform()
        except Exception as e:
            logger.exception(e)
            raise e
