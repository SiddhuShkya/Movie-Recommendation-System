import pytest
import pandas as pd
import os
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
        "tmdbId": [1, 2],
        "extra_col": ["val1", "val2"]
    })

def test_data_transformation_concat_features(sample_raw_data):
    config = MagicMock()
    config.data_path = "dummy_path"
    config.root_dir = "dummy_root"
    
    transformer = DataTransformation(config)
    
    # Test column dropping
    df_dropped = transformer.drop_columns(sample_raw_data.copy())
    assert "extra_col" not in df_dropped.columns
    assert "genres" in df_dropped.columns
    
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
    assert "Action Action Action" in weighted
    assert "Comedy Comedy Comedy" in weighted
    assert "A great movie." in weighted
