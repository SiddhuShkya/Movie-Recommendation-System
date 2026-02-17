from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import uvicorn
from fastapi import FastAPI
import pickle
import pandas as pd
from starlette.responses import RedirectResponse, JSONResponse
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Mount templates directory for assets (CSS/JS)
app.mount("/templates", StaticFiles(directory=os.path.join(os.getcwd(), "templates")), name="templates")

# Setup templates
templates = Jinja2Templates(directory="templates")

SAVED_EMBEDDING_PATH = "artifacts/model_trainer/movie_embeddings.pkl"
MOVIE_DATA_PATH = "artifacts/data_preparation/prepared.csv"
INGESTION_DATA_PATH = "artifacts/data_ingestion/final.csv"

# Global variables to store data
df = None
movie_embedding = None


# Load the movie dataframe and embeddings if they exist
def load_data():
    global df, movie_embedding
    try:
        if os.path.exists(MOVIE_DATA_PATH) and os.path.exists(SAVED_EMBEDDING_PATH):
            df = pd.read_csv(MOVIE_DATA_PATH)
            
            # Merge poster_path from ingestion data
            if os.path.exists(INGESTION_DATA_PATH):
                ingestion_df = pd.read_csv(INGESTION_DATA_PATH)
                if "poster_path" in ingestion_df.columns:
                    # Drop existing poster_path if any, then merge
                    if "poster_path" in df.columns:
                        df = df.drop(columns=["poster_path"])
                    
                    # Merge based on movie ID or title (using title as fallback if id mismatch)
                    # Checking content of final.csv earlier showed it has 'id' and 'title'
                    df = pd.merge(df, ingestion_df[['title', 'poster_path']], on='title', how='left')
                    print("✓ Poster data merged successfully")
            
            with open(SAVED_EMBEDDING_PATH, "rb") as f:
                movie_embedding = pickle.load(f)
            print("✓ Data loaded successfully")
        else:
            print("⚠ Artifacts not found. Please train the model first.")
            df = None
            movie_embedding = None
    except Exception as e:
        print(f"Error loading data: {e}")
        df = None
        movie_embedding = None


# Load data on startup
load_data()


def content_based_recommend(movie_title, df, embeddings, N=12):
    """Generate content-based recommendations"""
    try:
        # Case insensitive search
        matching_movies = df[df["title"].str.lower() == movie_title.lower()]
        if matching_movies.empty:
            return None, f"Movie '{movie_title}' not found in database"

        idx = matching_movies.index[0]
        movie_vec = embeddings[idx].reshape(1, -1)
        sims = cosine_similarity(movie_vec, embeddings).flatten()
        top_indices = sims.argsort()[::-1][1 : N + 1]

        recommendations = []
        for i in top_indices:
            movie_info = {
                "title": df.iloc[i]["title"],
                "similarity_score": round(float(sims[i]), 3)
            }
            # Add poster_path if it exists in the dataframe
            if "poster_path" in df.columns:
                movie_info["poster_path"] = df.iloc[i]["poster_path"]
            
            recommendations.append(movie_info)
            
        return recommendations, None
    except Exception as e:
        return None, str(e)


@app.get("/")
async def index(request: Request):
    """Serve the frontend index page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/movies")
async def get_movies():
    """Get list of all movies in the dataset"""
    if df is None:
        return JSONResponse(
            content={"error": "Data not loaded", "status": "error"},
            status_code=503
        )
    
    # Return alphabetical list of titles
    movie_list = sorted(df["title"].tolist())
    return JSONResponse(content={"movies": movie_list, "status": "success"})


@app.get("/health")
async def health_check():
    """Check if the service is ready"""
    status = {
        "status": "healthy",
        "model_loaded": df is not None and movie_embedding is not None,
        "data_path_exists": os.path.exists(MOVIE_DATA_PATH),
        "embeddings_path_exists": os.path.exists(SAVED_EMBEDDING_PATH),
    }
    return JSONResponse(content=status)


@app.get("/train")
async def training():
    """Train the model"""
    try:
        os.system("python main.py")
        # Reload data after training
        load_data()

        if df is not None and movie_embedding is not None:
            return JSONResponse(
                content={"message": "Training successful!", "status": "success"}
            )
        else:
            return JSONResponse(
                content={
                    "message": "Training completed but data could not be loaded",
                    "status": "warning",
                },
                status_code=500,
            )
    except Exception as e:
        return JSONResponse(
            content={"message": f"Error occurred: {e}", "status": "error"},
            status_code=500,
        )


@app.post("/recommend")
async def predict(movie_title: str, n_recommendations: int = 12):
    """Get movie recommendations"""
    # Check if data is loaded
    if df is None or movie_embedding is None:
        return JSONResponse(
            content={
                "error": "Model not loaded. Please train the model first using /train endpoint",
                "status": "error",
            },
            status_code=503,
        )

    try:
        recommendations, error = content_based_recommend(
            movie_title=movie_title,
            df=df,
            embeddings=movie_embedding,
            N=n_recommendations,
        )

        if error:
            return JSONResponse(
                content={"error": error, "status": "error"}, status_code=404
            )

        return JSONResponse(
            content={
                "movie": movie_title,
                "recommendations": recommendations,
                "status": "success",
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"error": f"Error occurred: {e}", "status": "error"},
            status_code=500,
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
