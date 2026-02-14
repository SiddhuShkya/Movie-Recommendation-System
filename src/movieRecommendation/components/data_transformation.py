import os
import pandas as pd
from src.movieRecommendation.logging import logger
from src.movieRecommendation.entity import DataTransformationConfig


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.columns_to_drop = [
            "positive_users",
            "positive_count",
            "negative_users",
            "negative_count",
            "vote_average",
            "vote_count",
            "status",
            "release_date",
            "revenue",
            "runtime",
            "budget",
            "poster_path",
        ]

    def drop_columns(self, df):
        initial_columns = df.shape[1]
        df.drop(columns=self.columns_to_drop, inplace=True)
        logger.info(
            f"Dropped {initial_columns - df.shape[1]} columns: {self.columns_to_drop}"
        )
        logger.info(f"Remaining columns: {list(df.columns)}")
        return df

    def clean_genres(self, x):
        import ast

        try:
            # Convert string representation of list to actual list
            if isinstance(x, str):
                x = ast.literal_eval(x)
            # Join list elements into comma-separated string
            return ", ".join([str(i).strip() for i in x])
        except:  # noqa: E722
            return str(x)

    def concat_features(self, df):
        logger.info("Starting feature concatenation")
        df["concat_description"] = None
        df["concat_description"] = (
            df["overview"].astype(str)
            + " "
            + df["genres"].astype(str)
            + " "
            + df["production_companies"].astype(str)
            + " "
            + df["original_language"].astype(str)
            + " "
        )
        logger.info(
            "Feature concatenation completed - created 'concat_description' column"
        )
        return df

    def transform(self):
        csv_path = os.path.join(self.config.data_path, "final.csv")
        logger.info(f"Starting data transformation from: {csv_path}")

        # Load data
        df = pd.read_csv(csv_path)
        logger.info(f"Loaded dataframe with shape: {df.shape}")

        # Drop columns
        df = self.drop_columns(df)

        # Clean genres
        logger.info("Cleaning genres column")
        df["genres"] = df["genres"].apply(self.clean_genres)
        logger.info("Genres cleaning completed")

        # Clean production companies
        logger.info("Cleaning production_companies column")
        df["production_companies"] = df["production_companies"].apply(
            lambda x: ", ".join([c.replace(" ", "") for c in x.split(",")])
        )
        logger.info("Production companies cleaning completed")

        # Concatenate features
        df = self.concat_features(df)

        # Save transformed data
        output_path = os.path.join(self.config.root_dir, "transformed.csv")
        df.to_csv(output_path, index=False)
        logger.info(f"Transformed data saved to: {output_path}")
        logger.info(f"Final dataframe shape: {df.shape}")
        logger.info("Data transformation completed successfully")
