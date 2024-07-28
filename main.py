import pandas as pd
import numpy as np
import matplotlib.pyplot as plt # For data visualization
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader


df = pd.read_csv("/Users/geoffreylee/Downloads/imdb_movie_data_2023.csv")

class MovieDataSet(Dataset):
    def __init__(self, data_dir):
        self.data = pd.read_csv(data_dir)
        self.data = self.data[['Moive Name', 'Rating', 'Votes', 'Meta Score', 'Genre', 'PG Rating', 'Year', 'Duration']]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        movie = self.data.iloc[idx]
        sample = {
            'movie_name': movie['Moive Name'],
            'rating': movie['Rating'],
            'votes': movie['Votes'],
            'meta_score': movie['Meta Score'],
            'genre': movie['Genre'],
            'pg_rating': movie['PG Rating'],
            'year': movie['Year'],
            'duration': movie['Duration']
        }
        return sample
    
    @property 
    def classes(self):
        return self.data.classes
