import pandas as pd
from sqlalchemy import create_engine, text

# Load the CSV file
csv_file = '/home/shraddha/Downloads/sql_data.csv'  # Update this path to the correct one
df = pd.read_csv(csv_file)

if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

df.rename(columns={
    'Release year': 'Release_year',
    'User votes': 'User_votes',
    'Plot synopsis': 'Plot_synopsis',
    'Poster Link': 'Poster_Link'
}, inplace=True)

# Database connection details
db_username = 'root'
db_password = 'manager'
db_host = 'localhost'  # or your database host
db_name = 'movie_database'

# Create a connection to the database
engine = create_engine(f'mysql+mysqlconnector://{db_username}:{db_password}@{db_host}')

# Create the database
with engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS movie_database"))

# Connect to the newly created database
engine = create_engine(f'mysql+mysqlconnector://{db_username}:{db_password}@{db_host}/{db_name}')

# Create the table
create_table_query = text("""
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    release_year INT,
    genre VARCHAR(255),
    duration VARCHAR(50),
    rating FLOAT,
    user_votes INT,
    plot_synopsis TEXT,
    director VARCHAR(255),
    poster_link TEXT
);
""")
with engine.connect() as conn:
    conn.execute(create_table_query)

# Load the data into the table
df.to_sql(name='movies', con=engine, if_exists='append', index=False)
