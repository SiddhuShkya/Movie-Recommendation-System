# 🎬 CineMatch | AI-Powered Movie Recommendation System

CineMatch is a full-stack movie recommendation platform that leverages state-of-the-art NLP models to provide intelligent, content-based suggestions. Featuring a sleek, modern interface and a robust data pipeline, CineMatch ensures that your next favorite movie is just a click away.

![CineMatch UI](screenshots/webapp.png)

## ✨ Key Features

- **🧠 Intelligent AI Recommendations**: Uses HuggingFace `all-MiniLM-L6-v2` sentence transformers to compute high-dimensional embeddings for over 13,000 movies.
- **🔍 Real-time Sidebar Filter**: Instantly search and filter through the entire movie database with a responsive sidebar.
- **🖼️ Poster Integration**: Automatic merging of TMDb poster data for a rich, visual browsing experience.
- **🔄 Synced Research Pipeline**: Perfect alignment between Jupyter research notebooks and the production API, ensuring consistent results across all environments.

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python, Pandas, Scikit-learn
- **AI/ML**: HuggingFace Transformers (Sentence-Transformers), NLTK
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism), JavaScript (ES6+)
- **Templates**: Jinja2

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/SiddhuShkya/Movie-Recommendation-System.git
cd Movie-Recommendation-System
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize & Train the Model
This will download the dataset, perform data cleaning, and generate the movie embeddings.
```bash
python main.py
```

### 4. Run the Web App
```bash
python app.py
```
Visit `http://localhost:8000` in your browser.

## 📂 Project Structure

- `src/`: Core logic and data pipeline components.
- `research/`: Jupyter notebooks for data exploration and model evaluation.
- `templates/`: Frontend assets (HTML, CSS, JS).
- `artifacts/`: Generated models, cleaned data, and ingested datasets.
- `main.py`: Entry point for the data pipeline.
- `app.py`: FastAPI server for the web interface.

## 🛡️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
