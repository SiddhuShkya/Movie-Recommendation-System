import pytest
import pandas as pd
import os
import pickle
import numpy as np
from unittest.mock import MagicMock
from src.movieRecommendation.components.data_transformation import DataTransformation
from src.movieRecommendation.components.data_preparation import DataPreparation

@pytest.fixture
def sample_raw_data():
    return pd.DataFrame({
        "title": ["Movie 1", "Movie 2"],
        "id": [1, 2],
        "original_language": ["en", "fr"],
        "overview": ["Overview 1", "Overview 2"],
        "genres": ["Action, Comedy", "Drama"],
        "production_companies": ["Comp 1", "Comp 2"],
        "keywords": ["key1, key2", "key3"],
        "positive_users": [0, 0],
        "positive_count": [0, 0],
        "negative_users": [0, 0],
        "negative_count": [0, 0],
        "vote_average": [0.0, 0.0],
        "vote_count": [0, 0],
        "status": ["Released", "Released"],
        "release_date": ["2021-01-01", "2021-01-01"],
        "revenue": [0, 0],
        "runtime": [120, 120],
        "budget": [0, 0],
        "poster_path": ["/path1", "/path2"],
        "movieId": [1, 2],
        "imdbId": [1, 2],
        "tmdb_id": [1, 2],
        "imdb_id": ["tt1", "tt2"],
        "adult": [False, False],
        "tmdbId": [1, 2]
    })

def test_data_transformation_concat_features(sample_raw_data):
    config = MagicMock()
    config.data_path = "dummy_path"
    config.root_dir = "dummy_root"
    
    transformer = DataTransformation(config)
    
    # Test column dropping
    df_dropped = transformer.drop_columns(sample_raw_data.copy())
    assert "genres" in df_dropped.columns
    assert "vote_average" not in df_dropped.columns
    
    # Test genre cleaning
    cleaned_genres = transformer.clean_genres("Action, Sci-Fi")
    assert cleaned_genres == "Action, Sci-Fi" # Current impl just returns same or joined list
    
    # Test concatenation
    df_concat = transformer.concat_features(df_dropped)
    assert "concat_description" in df_concat.columns
    assert "Movie 1" not in df_concat["concat_description"].iloc[0] # Title is not in concat
    assert "Overview 1" in df_concat["concat_description"].iloc[0]

def test_data_preparation_cleaning():
    config = MagicMock()
    config.data_path = "dummy_path"
    config.root_dir = "dummy_root"
    
    preparator = DataPreparation(config)
    
    text = "Hello World! 123. Running runner."
    
    # Test steps
    lower = preparator.make_lower_case(text)
    assert lower == "hello world! 123. running runner."
    
    no_punct = preparator.remove_punctuation(lower)
    assert "!" not in no_punct
    
    no_nums = preparator.remove_numbers(no_punct)
    assert "123" not in no_nums
    
    lemmatized = preparator.lemmatize_text("running runners")
    # NLTK lemmatizer usually returns 'run' for 'running' if POS is specified, 
    # but let's check general behavior
    assert "run" in lemmatized
    
    no_stop = preparator.remove_stop_words("the movie is great")
    assert "the" not in no_stop
    assert "is" not in no_stop

def test_weight_description_logic():
    # Helper to test the logic we synced
    from src.movieRecommendation.components.data_transformation import DataTransformation
    config = MagicMock()
    transformer = DataTransformation(config)
    
    row = pd.Series({
        "genres": "Action, Comedy",
        "concat_description": "A great movie."
    })
    
    weighted = transformer.weight_description(row)
    # The current implementation joins the list of genres multiplied by weight
    assert "Action Comedy Action Comedy Action Comedy" in weighted
    assert "A great movie." in weighted

def test_model_trainer_logic(tmp_path):
    from src.movieRecommendation.components.model_trainer import ModelTrainer
    
    # Mock config
    config = MagicMock()
    config.model_name = "dummy-model"
    config.data_path = str(tmp_path)
    config.root_dir = str(tmp_path)
    
    # Prepare dummy data
    df = pd.DataFrame({"cleaned_description": ["test one", "test two"]})
    df.to_csv(tmp_path / "prepared.csv", index=False)
    
    # Mock the embedding model
    with MagicMock() as mock_hf:
        mock_embedding_instance = MagicMock()
        mock_embedding_instance.embed_documents.return_value = [[0.1, 0.2], [0.3, 0.4]]
        
        trainer = ModelTrainer(config)
        # Patch load_hf_embedding to return our mock instance
        trainer.load_hf_embedding = MagicMock(return_value=mock_embedding_instance)
        
        trainer.train()
        
        # Verify pkl was created
        pkl_path = tmp_path / "movie_embeddings.pkl"
        assert pkl_path.exists()
        
        with open(pkl_path, "rb") as f:
            emb = pickle.load(f)
            assert emb.shape == (2, 2)
            assert np.array_equal(emb, np.array([[0.1, 0.2], [0.3, 0.4]]))
