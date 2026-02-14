from src.movieRecommendation.logging import logger
from src.movieRecommendation.pipeline.stage1_data_ingestion import (
    DataIngestionPipeline,
)
from src.movieRecommendation.pipeline.stage2_data_transformation import (
    DataTransformationPipeline,
)

STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
    data_ingestion = DataIngestionPipeline()
    data_ingestion.initiate_data_ingestion()
    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<")
except Exception as e:
    logger.exception(f"Error in stage {STAGE_NAME}: {e}")
    raise e

STAGE_NAME = "Data Transformation Stage"

try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
    data_transformation = DataTransformationPipeline()
    data_transformation.initiate_data_transformation()
    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<")
except Exception as e:
    logger.exception(f"Error in stage {STAGE_NAME}: {e}")
    raise e
