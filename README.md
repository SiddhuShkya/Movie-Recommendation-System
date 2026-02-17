# 🎬 CineMatch | AI-Powered Movie Recommendation System

CineMatch is a full-stack movie recommendation platform that leverages state-of-the-art NLP models to provide intelligent, content-based suggestions. Featuring a sleek, modern interface and a robust data pipeline, CineMatch ensures that your next favorite movie is just a click away.

![CineMatch UI](screenshots/webapp.png)

---

## ✨ Key Features

- **🧠 Intelligent AI Recommendations**: Uses HuggingFace `all-MiniLM-L6-v2` sentence transformers to compute high-dimensional embeddings for over 13,000 movies.
- **🔍 Real-time Sidebar Filter**: Instantly search and filter through the entire movie database with a responsive sidebar.
- **🖼️ Poster Integration**: Automatic merging of TMDb poster data for a rich, visual browsing experience.
- **🔄 Synced Research Pipeline**: Perfect alignment between Jupyter research notebooks and the production API, ensuring consistent results across all environments.

---

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python, Pandas, Scikit-learn
- **AI/ML**: HuggingFace Transformers (Sentence-Transformers), NLTK
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism), JavaScript (ES6+)
- **Templates**: Jinja2

---

## 📂 Project Structure

```bash
.
├── 📂 artifacts/           # Data & model artifacts generated per stage
├── 📂 config/              # YAML configuration for pipeline settings
├── 📂 research/            # Jupyter notebooks for model experimentation
├── 📂 screenshots/         # Web application UI previews
├── 📂 src/                 # Production Python source code
│   └── 📂 movieRecommendation/ # Modular application logic
├── 📂 templates/           # Frontend assets (HTML, CSS, JS)
├── 🐍 app.py               # FastAPI web server entry point
├── 🐍 main.py              # Data pipeline execution entry point
├── 🐳 Dockerfile           # Web app container configuration
├── 🐳 docker-compose.yaml  # Docker Compose orchestration
├── 📄 requirements_app.txt # Lightweight app-only dependencies
└── 📄 requirements_pipeline.txt # Heavy pipeline & research dependencies
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/SiddhuShkya/Movie-Recommendation-System.git
cd Movie-Recommendation-System
```

### 2. Install Dependencies

Depending on whether you want to train the model or just run the app, choose the appropriate file:

**For Model Training & Research (Heavy):**
```bash
pip install -r requirements_pipeline.txt
```

**For Running the Web App (Lightweight):**
```bash
pip install -r requirements_app.txt
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

---

## 🐳 Docker Support (Web App Only)

Run the CineMatch web application in a lightweight container using Docker:

### Using Docker Compose (Recommended)
```bash
docker-compose up --build
```

### Using Docker CLI
```bash
# Build the image
docker build -t cinematch .

# Run the container
docker run -p 8000:8000 cinematch
```

---

## 🛡️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
