import numpy as np
import pandas as pd

class SongRecommender():
    def __init__(self, song_id):
        self.song_id_ = song_id
        
    #cosine
    def cosine_dist(self, u, v):
        u_l2 = np.sqrt(np.sum(np.square(u),axis=1))
        v_l2 = np.sqrt(np.sum(np.square(v), axis=1)).values[0]

        numerator = pd.Series(np.dot(u,np.transpose(v)).reshape(-1,))
        dist = (numerator)/(u_l2*v_l2)
        return dist
    
    # euclidean
    def euclidean_dist(self, u, v):
        a = np.subtract(u, v)
        dist = np.sqrt(np.sum(np.square(a), axis=1))
        return dist
    
    def get_data(self):
        return pd.read_csv('input/preprocessed_numerical_data_3.csv')
    
    def get_recommendations(self, amount = 10):
        data = self.get_data()
        selectedSongId = self.song_id_
        selectedData = data[data['id'] == selectedSongId].iloc[:, 1:]
        selectedData = selectedData[selectedData.index == selectedData.index[0]]
        
        # get cosine distance
        cosDist = self.cosine_dist(data.iloc[:, 1:], selectedData)
        
        # get euclidean distance
        eucDist = self.euclidean_dist(data.iloc[:, 1:], selectedData)
        
        # merge cosine_dist and euclidean_dist
        # get total score (0 ~ 1)
        data['cos_score'] = cosDist
        data['euclidean_dist'] = eucDist
        c_max = data['cos_score'].max()
        c_min = data['cos_score'].min()
        data['cos_score'] = (data['cos_score'] - c_min) / (c_max - c_min)

        e_max = data['euclidean_dist'].max()
        e_min = data['euclidean_dist'].min()
        data['euclidean_dist'] = (data['euclidean_dist'] - e_min) / (e_max - e_min)
        data['euclidean_dist'] = 1 - data['euclidean_dist']
        data['total_score'] = 0.5*(data['euclidean_dist'] + data['cos_score'])
        
        # return recommendations
        if amount <= 0 or amount > 20:
            amount == 20
        
        data = data[data['id'] != selectedSongId].sort_values(by='total_score', ascending=False)
        idList = data.drop_duplicates(['id'])[:amount]['id'].values
        return idList