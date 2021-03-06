import numpy as np
import pandas as pd
from sklearn.preprocessing import minmax_scale
# 검색 순서
# 1.1 검색결과 그대로 있으면 리스트 반환
# 1.2 검색결과 없으면 포함된 단어 리스트 반환

# 2 artists, id에 대해 중복 제거 리스트 최종 반환

## 1번에서 그래도 검색결과 없으면 null 리턴


def return_search_results(song_name):
    #load data
    data = pd.read_csv('input/data.csv')
    data['artists'] = data['artists'].apply(lambda x: x[1:-1].split(','))
    data = data.explode('artists')
    data['artists'] = data['artists'].apply(lambda x: x.strip("'"))
    data = data.reset_index(drop=True)

    data_copy = data.copy()
    data_copy['name'] = data['name'].apply(lambda x:x.lower()).copy()

    # 1
    song_list = data_copy[data_copy['name'] == song_name.lower()].drop_duplicates(['artists']).drop_duplicates(['id'])
    song_list = song_list.sort_values(by='popularity', ascending=False)
    if(len(song_list) == 0):
        # 2
        song_list = data_copy[data_copy['name'].apply(lambda x: True if song_name.lower() in x else False)].drop_duplicates(['artists']).drop_duplicates(['id'])
        song_list = song_list.sort_values(by='popularity', ascending=False)
        if(len(song_list) == 0):
            return song_list, song_list
        else:
            return data_copy, song_list
    else:
        return data_copy, song_list

# cosine
def cosine_dist(u, v):
    u_l2 = np.sqrt(np.sum(np.square(u),axis=1))
    v_l2 = np.sqrt(np.sum(np.square(v),axis=1)).values[0]
    
    numerator = pd.Series(np.dot(u, np.transpose(v)).reshape(-1,))
    dist = (numerator)/(u_l2*v_l2)
    return dist

# euclidean
def euclidean_dist(u, v):
    a = np.subtract(u, v)
    dist = np.sqrt(np.sum(np.square(a), axis=1))
    return dist

def recommend_songs(song_id):
    data = pd.read_csv('input/data.csv')

    song_features = [
        'id','valence','acousticness','danceability','energy',
        'instrumentalness','liveness','loudness','speechiness','tempo'
    ]

    songs = [
            'id', 'artists', 'name', 'year',
            'duration_ms','popularity'
    ]

    numerical_song_features = song_features[1:-2]
    data[numerical_song_features] = minmax_scale(data[numerical_song_features])

    data = pd.get_dummies(data, columns=['key'])
    data = pd.get_dummies(data, columns=['mode'])

    key_mode_features = ['key_0', 'key_1', 'key_2', 'key_3', 'key_4', 'key_5', 'key_6', 'key_7',
       'key_8', 'key_9', 'key_10', 'key_11', 'mode_0', 'mode_1']
    song_features = song_features + key_mode_features

    selected_data = data[data['id'] == song_id]
    selected_data = selected_data[song_features].iloc[:, 1:]

    print(song_id)

    cosine_dist_val = cosine_dist(data[song_features].iloc[:, 1:], selected_data)
    data['cos_score'] = cosine_dist_val

    euclidean_dist_val = euclidean_dist(data[song_features].iloc[:, 1:], selected_data)
    data['euclidean_dist'] = euclidean_dist_val

    # merge cosine_dist and euclidean_dist
    c_max = data['cos_score'].max()
    c_min = data['cos_score'].min()
    data['cos_score'] = (data['cos_score'] - c_min) / (c_max - c_min)

    e_max = data['euclidean_dist'].max()
    e_min = data['euclidean_dist'].min()
    data['euclidean_dist'] = (data['euclidean_dist'] - e_min) / (e_max - e_min)
    data['euclidean_dist'] = 1 - data['euclidean_dist']

    data['total_score'] = 0.5*(data['euclidean_dist'] + data['cos_score'])

    data = data[songs+['total_score']].sort_values(by='total_score', ascending=False)
    data[data['popularity'] >60 ].iloc[:20]
    data['artists'] = data['artists'].apply(lambda x: x[1:-1])
    data = data.drop_duplicates(['artists']).drop_duplicates(['id'])
    return data[1:]

def song_analysis(id):
    data = pd.read_csv('input/data.csv')
    song = data[data['id'] == id]

    selected_song_name = song.name.tolist()[0]

    song_feat_values = []

    #energy
    if (song.energy.values[0] < data.energy.quantile(0.33)):
        song_feat_values.append('잔잔함')
    elif(song.energy.values[0] > data.energy.quantile(0.66)):
        song_feat_values.append('에너지 넘침')
    else:
        song_feat_values.append('')

    #danceability
    if (song.danceability.values[0] > data.danceability.quantile(0.66)):
        song_feat_values.append('댄스곡 느낌')
    else:
        song_feat_values.append('')

    #tempo
    if (song.tempo.values[0] < data.tempo.quantile(0.33)):
        song_feat_values.append('느린 템포')
    elif ((song.tempo.values[0] >= data.tempo.quantile(0.33)) & (song.tempo.values[0] <= data.tempo.quantile(0.66))):
        song_feat_values.append('중간 템포')
    elif (song.tempo.values[0] > data.tempo.quantile(0.66)):
        song_feat_values.append('빠른 템포')
    else:
        song_feat_values.append('')
    #valence
    if (song.valence.values[0] < data.valence.quantile(0.33)):
        song_feat_values.append('슬픈 분위기')
    elif (song.valence.values[0] > data.valence.quantile(0.66)):
        song_feat_values.append('밝은 분위기')
    else:
        song_feat_values.append('')

    #loudness
    if (song.loudness.values[0] < data.loudness.quantile(0.33)):
        song_feat_values.append('조용함')
    elif (song.loudness.values[0] > data.loudness.quantile(0.66)):
        song_feat_values.append('시끄러움')
    else:
        song_feat_values.append('')

    #acousticness
    if (song.acousticness.values[0] > data.acousticness.quantile(0.85)):
        song_feat_values.append('슬픈 분위기')
    else:
        song_feat_values.append('')

    song_feat = pd.DataFrame({
        'energy': song_feat_values[0],
        'danceability': song_feat_values[1],
        'tempo': song_feat_values[2],
        'valence': song_feat_values[3],
        'loudness': song_feat_values[4],
        'acousticness': song_feat_values[5]
    }, index=[0])

    return song_feat, selected_song_name
    