import os
import pickle
import pandas as pd
import numpy as np
from src.movieRecommendation.logging import logger
from src.movieRecommendation.entity import ModelTrainerConfig
from langchain_huggingface import HuggingFaceEmbeddings


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def load_hf_embedding(self):
        logger.info(f"Loading HuggingFace embedding model: {self.config.model_name}")
        embedding = HuggingFaceEmbeddings(model_name=self.config.model_name)
        logger.info("HuggingFace embedding model loaded successfully")
        return embedding

    def train(self):
        logger.info("Starting model training")

        # Load data
        data_file = os.path.join(self.config.data_path, "prepared.csv")
        logger.info(f"Loading prepared data from: {data_file}")
        df = pd.read_csv(data_file)
        logger.info(f"Loaded dataframe with shape: {df.shape}")

        # Extract descriptions
        descriptions = df["cleaned_description"].tolist()
        logger.info(f"Extracted {len(descriptions)} movie descriptions")

        # Load embedding model
        embedding = self.load_hf_embedding()

        # Generate embeddings
        logger.info("Generating embeddings for all movies (this may take a while)...")
        movie_embedding = np.array(embedding.embed_documents(descriptions))
        logger.info(
            f"Embeddings generated successfully. Shape: {movie_embedding.shape}"
        )

        # Save embeddings
        embeddings_path = os.path.join(self.config.root_dir, "movie_embeddings.pkl")
        logger.info(f"Saving embeddings to: {embeddings_path}")
        with open(embeddings_path, "wb") as f:
            pickle.dump(movie_embedding, f)
        logger.info("Embeddings saved successfully")

        logger.info("Model training completed successfully")
