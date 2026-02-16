import os
import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from src.movieRecommendation.logging import logger
from src.movieRecommendation.entity import DataPreparationConfig


class DataPreparation:
    def __init__(self, config: DataPreparationConfig):
        self.config = config
        self.lemmatizer = WordNetLemmatizer()
        logger.info("DataPreparation initialized")

    def make_lower_case(self, text):
        text_lower = None
        text_lower = text.lower()
        return text_lower

    def remove_stop_words(self, text):
        text = text.split()
        stop_words = set(stopwords.words("english"))
        removed_stop_word_text = None
        filtered_words = [word for word in text if word not in stop_words]
        removed_stop_word_text = " ".join(filtered_words)
        return removed_stop_word_text

    def remove_numbers(self, text):
        pattern = r"[0-9]"
        removed_numbers_text = re.sub(pattern, "", text)
        return removed_numbers_text

    def remove_punctuation(self, text):
        tokenizer = RegexpTokenizer(r"[\w-]+")
        tokens = tokenizer.tokenize(text)
        removed_punctuation_text = " ".join(tokens)
        return removed_punctuation_text

    def lemmatize_text(self, text):
        tokens = word_tokenize(text)
        lemmatized = [self.lemmatizer.lemmatize(token.lower()) for token in tokens]
        return " ".join(lemmatized)

    def prepare(self):
        csv_path = os.path.join(self.config.data_path, "transformed.csv")
        logger.info(f"Starting data preparation from: {csv_path}")

        # Load data
        df = pd.read_csv(csv_path)
        logger.info(f"Loaded dataframe with shape: {df.shape}")
        logger.info(f"Columns in dataframe: {list(df.columns)}")

        # Create copy for cleaning
        df_cleaned = df.copy()
        logger.info("Created copy of dataframe for cleaning")

        # Apply text preprocessing pipeline
        logger.info(
            "Starting text preprocessing pipeline on 'concat_description' column"
        )

        logger.info("Step 1/5: Converting text to lowercase")
        df_cleaned["cleaned_description"] = df["concat_description"].apply(
            self.make_lower_case
        )

        logger.info("Step 2/5: Removing punctuation")
        df_cleaned["cleaned_description"] = df_cleaned["cleaned_description"].apply(
            self.remove_punctuation
        )

        logger.info("Step 3/5: Removing numbers")
        df_cleaned["cleaned_description"] = df_cleaned["cleaned_description"].apply(
            self.remove_numbers
        )

        logger.info("Step 4/5: Lemmatizing text")
        df_cleaned["cleaned_description"] = df_cleaned["cleaned_description"].apply(
            self.lemmatize_text
        )

        logger.info("Step 5/5: Removing stop words")
        df_cleaned["cleaned_description"] = df_cleaned["cleaned_description"].apply(
            self.remove_stop_words
        )

        logger.info("Text preprocessing pipeline completed")

        df_cleaned.drop(columns=["concat_description"], inplace=True)
        logger.info("Removed the concat_description column")
        # Log sample of cleaned text
        if len(df_cleaned) > 0:
            sample_original = df["concat_description"].iloc[0][:100]
            sample_cleaned = df_cleaned["cleaned_description"].iloc[0][:100]
            logger.info(f"Sample original text: {sample_original}...")
            logger.info(f"Sample cleaned text: {sample_cleaned}...")

        # Save prepared data
        output_path = os.path.join(self.config.root_dir, "prepared.csv")
        df_cleaned.to_csv(output_path, index=False)
        logger.info(f"Prepared data saved to: {output_path}")
        logger.info(f"Final dataframe shape: {df_cleaned.shape}")
        logger.info("Data preparation completed successfully")
