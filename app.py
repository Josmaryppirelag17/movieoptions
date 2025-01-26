from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Sustituye 'tu_clave_de_api' con tu clave de RapidAPI de OMDb
OMDB_API_KEY = "28110f2d"
OMDB_API_URL = "http://www.omdbapi.com/"

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

    # Hacer solicitud a la API de OMDb para obtener los detalles de la película
    url = f"{OMDB_API_URL}?t={movie_title}&apikey={OMDB_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Esto generará una excepción si la respuesta es un error (código 4xx o 5xx)
        data = response.json()

        if data.get("Response") == "True":
            # Tomamos los detalles de la película
            title = data.get("Title", "Título no disponible")
            release_date = data.get("Released", "Fecha no disponible")
            plot = data.get("Plot", "Sinopsis no disponible")
            actors = data.get("Actors", "Actores no disponibles")
        else:
            return render_template('error.html', message=f"No se encontró la película: {movie_title}.")

        return render_template('result.html', title=title, release_date=release_date, plot=plot, actors=actors)

    except requests.exceptions.RequestException as e:
        # Si ocurre cualquier error en la solicitud, mostramos un mensaje genérico
        return render_template('error.html', message="Hubo un error al conectar con OMDb. Intenta más tarde.")
    except Exception as e:
        # Si ocurre un error inesperado, lo mostramos en un mensaje
        return render_template('error.html', message=f"Ocurrió un error inesperado: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
