# Movie Recommender System (MRS)

A **content-based movie recommender system** built with Python that suggests movies similar to a user’s selection, leveraging the The Movie Database (TMDB) metadata and API for movie posters.

# Project Overview

This project uses the TMDB movie metadata dataset (from Kaggle) and the TMDB API to power a movie-recommendation engine. It processes textual movie attributes, vectorises them, computes similarities using cosine similarity, and then fetches movie posters to enhance the interface.
  

# Dataset & Features

Dataset used:
- [TMDB Movie Metadata (Kaggle)](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)  
- Contains movie information such as title, genres, overview, cast, crew, keywords, etc.

Features / Pre-processing steps include:
1. Extracting textual and categorical features (e.g., genres, keywords, overview, cast/crew)  
2. Cleaning & normalising text (lowercase, remove punctuation, strip whitespace, etc.)  
3. Combining selected features into a single “feature string” for each movie  
4. Vectorising the combined text using techniques such as `CountVectorizer`.  
5. Computing cosine similarity between movie vectors to generate a similarity matrix  
6. Using the similarity matrix to recommend movies most similar to a given movie  
7. Fetching corresponding movie posters from TMDB API to display along with recommendations  

# How It Works

1. Loading and preparing the data:  
   - Load the metadata CSV from Kaggle  
   - Select necessary columns (title, overview, genres, cast, crew, keywords, etc.)  
   - Preprocess text and categorical features  
   - Combine into a unified “metadata string” for each movie  
   
2. Vectorising text data:  
   - Used `CountVectorizer` to convert the metadata strings into numeric vectors  
   - Fit the vectoriser on the training set or full dataset  
   
3. Computed similarity matrix:  
   - Use cosine similarity between all movie vectors to build a similarity matrix  
   - Store or pickle the similarity matrix for efficient lookup  
   
4. Getting recommendations:  
   - When a user selects a movie, find its index in the dataset  
   - Look up similarity scores from the similarity matrix  
   - Sort movies by descending similarity (excluding the selected movie)  
   - Return the top N similar movies  
   
5. Fetched and displayed posters:  
   - Used TMDB API endpoint(s) to fetch poster image URLs given a movie ID  
   - Display the titles + posters of the recommended movies  

# Tech Stack & Dependencies

- **Python**
- Pandas, NumPy  
- Scikit-learn (for vectorisation & cosine similarity)  
- Requests (for API calls)  
- (Optional) Flask, Streamlit or another web/UI framework for user interface  
- TMDB API for poster retrieval  

Check `requirements.txt` for full list of dependencies.

# Installation & Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/Shansinghal/MRS.git
   cd MRS

2. Install dependencies:
   ```
   pip install -r requirements.txt

4. Obtain your TMDB API key:
   Sign up/log in at https://www.themoviedb.org/
   Go to your account → Settings → API → Create new API key
   Store the key securely (for example in a .env file) and make sure your code accesses it (e.g., via os.environ["TMDB_API_KEY"])

5. Run the application:
   ```
   streamlit run app.py

7. Use the UI to select a movie and get recommendations (with posters!)


<img width="996" height="719" alt="{1EB3923D-BAF4-4ECD-B242-5923132A7701}" src="https://github.com/user-attachments/assets/796a7433-f4f4-4792-b61f-42773f931f88" />

