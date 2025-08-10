try:
    import pandas as pd
except ImportError:
    raise ImportError("The pandas library is required to run this script. Please install it with 'pip install pandas'.")

try:
    import tkinter as tk
    from tkinter import messagebox, simpledialog, scrolledtext
except ImportError:
    raise ImportError("The tkinter library is required to run this script. It is included with most Python installations.")

# Sample movie dataset
data = {
    'title': [
        'The Matrix', 'Toy Story', 'The Godfather', 'Pulp Fiction', 'Finding Nemo',
        'The Shawshank Redemption', 'The Dark Knight', 'Forrest Gump', 'Inception', 'The Lion King',
        # Bollywood movies
        '3 Idiots', 'Dangal', 'Lagaan', 'Zindagi Na Milegi Dobara', 'Queen'
    ],
    'genres': [
        'Action|Sci-Fi', 'Animation|Comedy|Family', 'Crime|Drama', 'Crime|Drama', 'Animation|Adventure|Comedy',
        'Drama', 'Action|Crime|Drama', 'Drama|Romance', 'Action|Adventure|Sci-Fi', 'Animation|Adventure|Drama',
        # Bollywood genres
        'Comedy|Drama', 'Biography|Drama|Sport', 'Adventure|Drama|Sport', 'Adventure|Comedy|Drama', 'Adventure|Comedy|Drama'
    ]
}

movies = pd.DataFrame(data)

# Preprocess genres for easier matching
movies['genres'] = movies['genres'].apply(lambda x: [g.strip().lower() for g in x.split('|')])

# Get all unique genres for GUI selection
all_genres = sorted({genre for genres in movies['genres'] for genre in genres})

def recommend_movies(preferred_genres, top_n=5):
    # Ensure preferred_genres are lowercased for matching
    preferred_genres_set = set(g.strip().lower() for g in preferred_genres)
    def score(genres):
        return len(set(genres) & preferred_genres_set)
    # Avoid SettingWithCopyWarning by working on a copy
    movies_copy = movies.copy()
    movies_copy['score'] = movies_copy['genres'].apply(score)
    # Fix: sort_values expects keyword arguments, not lists
    recommended = movies_copy[movies_copy['score'] > 0].sort_values(by='score', ascending=False)
    if recommended.empty:
        return []
    else:
        return recommended.head(top_n)[['title', 'genres', 'score']].values.tolist()

class MovieRecommenderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Movie Recommendation System")
        master.configure(bg='#f0f4f7')

        self.label = tk.Label(master, text="Select your favorite genres:", bg='#f0f4f7', font=("Arial", 12, "bold"))
        self.label.pack(pady=(10, 0))

        self.genre_vars = []
        self.genre_checks = []
        genre_frame = tk.Frame(master, bg='#f0f4f7')
        genre_frame.pack(pady=5)
        for i, genre in enumerate(all_genres):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(genre_frame, text=genre.title(), variable=var, bg='#f0f4f7', activebackground='#e0e7ef', font=("Arial", 10))
            chk.grid(row=i//3, column=i%3, sticky='w', padx=5, pady=2)
            self.genre_vars.append(var)
            self.genre_checks.append(chk)

        self.recommend_button = tk.Button(
            master,
            text="Get Recommendations",
            command=self.show_recommendations,
            bg='#1976d2', fg='white',
            activebackground='#1565c0', activeforeground='white',
            font=("Arial", 12, "bold"),
            relief=tk.RAISED, bd=3
        )
        self.recommend_button.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(master, width=50, height=10, state='disabled', wrap='word', font=("Arial", 10), bg='#e3f2fd')
        self.result_text.pack(padx=10, pady=(0, 10))

    def show_recommendations(self):
        selected_genres = [genre for genre, var in zip(all_genres, self.genre_vars) if var.get()]
        if not selected_genres:
            messagebox.showwarning("No Genres Selected", "Please select at least one genre.")
            return
        recommendations = recommend_movies(selected_genres, top_n=5)
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        if not recommendations:
            self.result_text.insert(tk.END, "No recommendations found for your genres.\n")
        else:
            self.result_text.insert(tk.END, f"Top {len(recommendations)} movie recommendations for you:\n\n")
            for title, genres, score in recommendations:
                genre_str = ', '.join([g.title() for g in genres])
                self.result_text.insert(tk.END, f"- {title} (Genres: {genre_str})\n")
        self.result_text.config(state='disabled')

def main():
    root = tk.Tk()
    app = MovieRecommenderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()