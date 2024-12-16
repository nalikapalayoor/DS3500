import os
import re
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from collections import Counter
from textblob import TextBlob
from matplotlib.lines import Line2D
from test_scraper import ctrl_songs


nltk.download('stopwords')

class LyricsAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))  
        custom_stop_words = {"got", "like", "chorus", "oh", "say", "yeah", "get", "see", "like", "verse", "pre", "sza", "na", "mind", "gets", "1", "2"}
        self.stop_words.update(custom_stop_words)
        self.songs_data = {}

    def remove_stop_words(self, lyrics):
        """Remove stop words from lyrics"""
        words = re.findall(r'\w+', lyrics.lower())
        filtered_words = [word for word in words if word not in self.stop_words]
        return ' '.join(filtered_words)



    def load_lyrics_from_folder(self, folder_path, parser=None):
        """
        Load lyrics from a folder and apply custom parser
        """
        lyrics_data = {}
        for file_name in os.listdir(folder_path):
            song_name = file_name.replace('.txt', '')  
            with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as file:
                lyrics = file.read()
                if parser:
                    lyrics = parser(lyrics)  
                lyrics_data[song_name] = self.remove_stop_words(lyrics)
        return lyrics_data

    def generate_sankey(self, songs_data, k=10):
        """
        Generate a Sankey diagram showing word counts across songs
        """
        all_words = []
        for song, lyrics in songs_data.items():
            words = re.findall(r'\w+', lyrics.lower())
            all_words.extend(words)

        word_counts = Counter(all_words)
        top_words = word_counts.most_common(k)
        top_words = [word for word, _ in top_words]

        labels = list(songs_data.keys()) + top_words
        sources = []
        targets = []
        values = []

        for song_idx, (song, lyrics) in enumerate(songs_data.items()):
            words = re.findall(r'\w+', lyrics.lower())
            word_count = Counter(words)
            for word, count in word_count.items():
                if word in top_words:
                    word_idx = top_words.index(word) + len(songs_data)
                    sources.append(song_idx)
                    targets.append(word_idx)
                    values.append(count)

        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values
            )
        ))
        fig.show()

    def generate_word_freq_plot(self, songs_data):
        """
        Generate word frequency bar plots for each song
        """
        num_songs = len(songs_data)
        rows = (num_songs + 4) // 5 
        fig, axes = plt.subplots(rows, 5, figsize=(15, 8))
        axes = axes.flatten()

        for idx, (song, lyrics) in enumerate(songs_data.items()):
            words = re.findall(r'\w+', lyrics.lower())
            word_counts = Counter(words)
            top_words = word_counts.most_common(10)
            words, counts = zip(*top_words) if top_words else ([], [])
            axes[idx].barh(words, counts, color='skyblue')
            axes[idx].set_title(song)
            axes[idx].invert_yaxis()

        for ax in axes[num_songs:]:
            ax.axis('off')

        plt.tight_layout()
        plt.show()

    def sentiment_analysis(self, songs_data, ctrl_songs):
        """
        Perform sentiment analysis and plot sentiment scores for each song
        """
        song_names = []
        sentiment_scores = []
        album_colors = []

        ctrl_song_names = [song['filename'] for song in ctrl_songs]

        for song, lyrics in songs_data.items():
            blob = TextBlob(lyrics)
            sentiment = blob.sentiment.polarity

            song_names.append(song)
            sentiment_scores.append(sentiment)

            if song in ctrl_song_names:
                album_colors.append('green')  
            else:
                album_colors.append('blue')  

        plt.figure(figsize=(12, 6))
        scatter = plt.scatter(song_names, sentiment_scores, c=album_colors, alpha=0.7, edgecolors='k')

        plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)  
        plt.xticks(rotation=45, ha='right')
        plt.ylabel("Sentiment Score")
        plt.title("Sentiment Scores for Each Song")

        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Ctrl'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='SOS'),
        ]
        plt.legend(handles=legend_elements, loc='upper right')

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    analyzer = LyricsAnalyzer()

    ctrl_lyrics = analyzer.load_lyrics_from_folder("data/ctrl")
    sos_lyrics = analyzer.load_lyrics_from_folder("data/sos")

    songs_data = {**ctrl_lyrics, **sos_lyrics}

    analyzer.generate_sankey(songs_data, k=10)
    analyzer.generate_word_freq_plot(songs_data)
    analyzer.sentiment_analysis(songs_data, ctrl_songs)
