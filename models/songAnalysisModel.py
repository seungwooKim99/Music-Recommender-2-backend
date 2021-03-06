import numpy as np
import pandas as pd

class SongAnalysis():
    def __init__(self, song_id):
        self.song_id_ = song_id
        
    def get_data(self):
        return pd.read_csv('input/preprocessed_original_data_2.csv')
    
    def ExplaneFeatures(self):
        data = self.get_data()
        selectedSongId = self.song_id_
        song = data[data['song_id'] == selectedSongId]
        
        song_feat_values = []
        
        #energy
        if (song.energy.values[0] < data.energy.quantile(0.33)):
            song_feat_values.append('#잔잔함')
        elif(song.energy.values[0] > data.energy.quantile(0.66)):
            song_feat_values.append('#에너제틱')

        #danceability
        if (song.danceability.values[0] > data.danceability.quantile(0.66)):
            song_feat_values.append('#댄스곡')

        #tempo
        if (song.tempo.values[0] < data.tempo.quantile(0.33)):
            song_feat_values.append('#느린템포')
        elif ((song.tempo.values[0] >= data.tempo.quantile(0.33)) & (song.tempo.values[0] <= data.tempo.quantile(0.66))):
            song_feat_values.append('#중간템포')
        elif (song.tempo.values[0] > data.tempo.quantile(0.66)):
            song_feat_values.append('#빠른템포')

        #valence
        if (song.valence.values[0] < data.valence.quantile(0.33)):
            song_feat_values.append('#슬픈분위기')
        elif (song.valence.values[0] > data.valence.quantile(0.66)):
            song_feat_values.append('#밝은분위기')


        #loudness
        if (song.loudness.values[0] < data.loudness.quantile(0.33)):
            song_feat_values.append('#조용함')
        elif (song.loudness.values[0] > data.loudness.quantile(0.66)):
            song_feat_values.append('#화려함')
        
        return song_feat_values