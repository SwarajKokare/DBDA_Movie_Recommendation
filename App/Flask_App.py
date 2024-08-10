from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:manager@localhost/movie_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load the model and data for recommendations
with open('model.pkl', 'rb') as file:
    tfidf_matrix_sparse, tfidf, movie_nlp = pickle.load(file)

# Define Movie model
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    
    genre = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    user_votes = db.Column(db.Integer, nullable=False)
    plot_synopsis = db.Column(db.Text, nullable=False)
    director = db.Column(db.String(100), nullable=False)
    poster_link = db.Column(db.String(250), nullable=False)

# Function to get recommendations based on cosine similarity
def get_recommendations(title, release_year, min_rating=0.0):
    filtered_movies = movie_nlp[(movie_nlp['Title'] == title) & (movie_nlp['Release_year'] == int(release_year))]

    if filtered_movies.empty:
        return "Movie not found in the database."

    idx = filtered_movies.index[0]

    sim_scores = cosine_similarity(tfidf_matrix_sparse[idx], tfidf_matrix_sparse).flatten()

    sim_scores_indices = np.argsort(sim_scores)[::-1]

    sim_scores_indices = sim_scores_indices[1:16]

    similar_movies = movie_nlp.iloc[sim_scores_indices]
    similar_movies = similar_movies[similar_movies['Rating'] >= min_rating]

    return similar_movies[
        ['Title', 'Rating', 'Genre', 'Director', 'User_votes', 'Plot_synopsis', 'Duration', 'Release_year',
         'Poster_Link']]


@app.route('/')
def index():
    return render_template('index_bs.html')

@app.route('/search')
def search():
    query = request.args.get('query', '')
    results = Movie.query.filter(Movie.title.ilike(f"%{query}%")).all()
    titles = [{'title': movie.title, 'release_year': movie.release_year} for movie in results]
    return jsonify(titles)

@app.route('/recommendations', methods=['GET'])
def recommendations():
    selected_title = request.args.get('selected_title', '')
    selected_release_year = request.args.get('selected_release_year', '')
    min_rating = float(request.args.get('min_rating', 0.0))

    similar_movies = get_recommendations(selected_title, selected_release_year, min_rating)

    if isinstance(similar_movies, str):
        return jsonify({"error": similar_movies})

    recommendations = []
    for _, row in similar_movies.iterrows():
        recommendations.append({
            'Title': row['Title'],
            'Rating': row['Rating'],
            'Genre': row['Genre'],
            'Director': row['Director'],
            'UserVotes': row['User_votes'],
            'PlotSynopsis': row['Plot_synopsis'],
            'Duration': row['Duration'],
            'ReleaseYear': row['Release_year'],
            'PosterLink': row['Poster_Link']
        })
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
