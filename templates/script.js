document.addEventListener('DOMContentLoaded', () => {
    const movieInput = document.getElementById('movieInput');
    const trainBtn = document.getElementById('trainBtn');
    const resultsGrid = document.getElementById('results');
    const loader = document.getElementById('loader');
    const movieList = document.getElementById('movieList');
    const welcomeScreen = document.getElementById('welcomeScreen');
    const resultsContent = document.getElementById('resultsContent');

    const TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500";
    const DEFAULT_POSTER = "https://via.placeholder.com/500x750?text=No+Poster+Available";

    let allMovies = [];

    const showLoader = (show) => {
        loader.style.display = show ? 'flex' : 'none';
        if (show) {
            resultsGrid.innerHTML = '';
            welcomeScreen.style.display = 'none';
            resultsContent.style.display = 'block';
        }
    };

    const fetchAllMovies = async () => {
        try {
            const response = await fetch('/movies');
            const data = await response.json();
            if (data.status === 'success') {
                allMovies = data.movies;
                renderMovieList(allMovies);
            }
        } catch (error) {
            console.error('Error fetching movies:', error);
        }
    };

    const renderMovieList = (movies) => {
        movieList.innerHTML = movies.map(movie => `
            <div class="movie-item" onclick="selectMovie('${movie.replace(/'/g, "\\'")}')">
                ${movie}
            </div>
        `).join('');
    };

    window.selectMovie = async (title) => {
        // Update active state in sidebar
        const items = document.querySelectorAll('.movie-item');
        items.forEach(item => {
            if (item.textContent.trim() === title) {
                item.classList.add('active');
                item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                item.classList.remove('active');
            }
        });

        movieInput.value = title;
        fetchRecommendations(title);
    };

    const fetchRecommendations = async (title) => {
        showLoader(true);
        try {
            const response = await fetch(`/recommend?movie_title=${encodeURIComponent(title)}`, {
                method: 'POST'
            });

            const data = await response.json();

            if (data.status === 'success') {
                renderMovies(data.recommendations);
                resultsGrid.scrollIntoView({ behavior: 'smooth' });
            } else {
                resultsGrid.innerHTML = `<p class="error-msg">${data.error || 'Something went wrong'}</p>`;
            }
        } catch (error) {
            console.error('Error:', error);
            resultsGrid.innerHTML = `<p class="error-msg">Failed to fetch recommendations.</p>`;
        } finally {
            showLoader(false);
        }
    };

    const renderMovies = (movies) => {
        resultsGrid.innerHTML = movies.map(movie => `
            <div class="movie-card" style="text-align: center;">
                <img src="${movie.poster_path ? TMDB_IMAGE_BASE + movie.poster_path : DEFAULT_POSTER}" 
                    alt="${movie.title}" 
                    class="movie-poster"
                    onerror="this.src='${DEFAULT_POSTER}'">
                    
                <div class="movie-info" 
                    style="display: flex; flex-direction: column; align-items: center;">
                    
                    <h3 class="movie-title" 
                        title="${movie.title}" 
                        style="margin: 8px 0 4px 0; text-align: center;">
                        ${movie.title}
                    </h3>

                    <div class="movie-score" 
                        style="display: flex; flex-direction: column; align-items: center;">
                        
                        <span class="score-badge" style="margin-bottom: 4px;">
                            ${(movie.similarity_score * 100).toFixed(0)}%
                        </span>
                    </div>
                </div>
            </div>
        `).join('');
    };

    movieInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const filtered = allMovies.filter(movie => movie.toLowerCase().includes(query));
        renderMovieList(filtered);
    });

    const handleTrain = async () => {
        if (!confirm('Re-training might take some time. Continue?')) return;

        trainBtn.disabled = true;
        const originalContent = trainBtn.innerHTML;
        trainBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Training...';

        try {
            const response = await fetch('/train');
            const data = await response.json();
            alert(data.message);
            fetchAllMovies(); // Refresh list after training
        } catch (error) {
            alert('Training failed: ' + error.message);
        } finally {
            trainBtn.disabled = false;
            trainBtn.innerHTML = originalContent;
        }
    };

    trainBtn.addEventListener('click', handleTrain);

    // Initial load
    fetchAllMovies();
});
