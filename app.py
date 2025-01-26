from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Configuración de la API
API_KEY = "29f005f4c4bf034d8a7fc1c13f6b3126"  # Sustituye con tu clave de API de TMDb
TMDB_API_URL = "https://api.themoviedb.org/3/search/movie"

@app.route('/')
def home():
    """Página inicial"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_movie():
    """Buscar película y mostrar resultados"""
    movie_title = request.form.get('movie_title')

    if not movie_title:
        return render_template('error.html', message="Por favor, ingresa el título de una película.")

    # Hacer solicitud a la API de TMDb
    params = {
        "api_key": API_KEY,
        "query": movie_title,
        "language": "es-ES"  # Configuración para obtener resultados en español
    }

    response = requests.get(TMDB_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            # Tomamos el primer resultado de la lista de películas
            movie = data['results'][0]
            title = movie.get('title', "Título no disponible")
            release_date = movie.get('release_date', "Fecha no disponible")
            overview = movie.get('overview', "Sinopsis no disponible")
            return render_template('result.html', title=title, release_date=release_date, overview=overview)
        else:
            return render_template('error.html', message=f"No se encontraron resultados para: {movie_title}.")
    else:
        return render_template('error.html', message="Hubo un error al conectarse con TMDb. Intenta más tarde.")

if __name__ == '__main__':
    app.run(debug=True)
