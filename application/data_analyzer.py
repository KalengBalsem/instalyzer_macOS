import pandas as pd 
import sqlite3

from . import DB_NAME

def analyze_data(username, iteration):
    con = sqlite3.connect(f'instance/{DB_NAME}')

    owner_id = con.execute(f"SELECT id FROM Profile WHERE username='{username}'").fetchone()[0]
    df = pd.read_sql_query(f"SELECT * FROM Post WHERE owner_id={owner_id}", con)

    requested_posts_count = (iteration+1)*12
    df = df.iloc[:requested_posts_count+1]

    # DATA CLEANING
    # initialize datetime column + adding day column
    df['timestamp'] = pd.to_datetime(df['timestamp'], format="%d/%m/%Y %H:%M:%S")

    # make a weekday column and time
    df['weekday'] = df['timestamp'].dt.day_name()
    #####

    # 1. Popular Upload Day (chart_type: BAR)
    sorted_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    popularUploadDay = df.groupby('weekday')['likes_count'].mean().reindex(sorted_days).fillna(0)
    popularUploadDay_x = [_ for _ in popularUploadDay.index]
    popularUploadDay_y = [_ for _ in popularUploadDay]
    ####

    # 2. Popular Upload Time (chart_type: BAR)
    df['hour'] = df['timestamp'].dt.hour
    popularUploadTime = df.groupby('hour')['likes_count'].mean()
    popularUploadTime_x = [_ for _ in popularUploadTime.index]
    popularUploadTime_y = [_ for _ in popularUploadTime]
    ####

    # 3. posts performance based on likes & comments (chart_type: LINE)
    postsPerformance_x = [i for i in df.iloc[::-1].index]
    postsPerformance_y1 = [i for i in df.iloc[::-1]['likes_count']]
    postsPerformance_y2 = [i for i in df.iloc[::-1]['comments_count']]
    ####

    # 4. top hashtags (upper 20)
    hash = {}
    for _ in df['hashtags']:
        for i in _.split():
            if not i.startswith('#'): continue
            if i not in [key for (key, value) in hash.items()]:
                hash[i] = 1
            else:
                hash[i] += 1

    # return 20 most frequent hashtags
    sorted_hash = sorted(hash.items(), key=lambda x:x[1], reverse=True)
    top_hashtags = sorted_hash[:10]
    ####

    # 5. top caption words
    word = {}
    for _ in df['caption']:
        for i in _.split():
            if i.startswith('#'): 
                continue
            if i not in [key for (key, value) in word.items()]:
                word[i] = 1
            else:
                word[i] += 1

    # return 20 most frequent hashtags
    sorted_word = sorted(word.items(), key=lambda x:x[1], reverse=True)
    for i in sorted_word:
        if len(i[0]) <= 1:
            sorted_word.remove(i)
    top_words = sorted_word[:10]
    ####

    # 6. daily posts volume
    postsVolume = df.groupby('weekday').count().iloc[:, 0].reindex(sorted_days).fillna(0)
    postsVolume_x = [i for i in postsVolume.index]
    postsVolume_y = [i for i in postsVolume]
    ####

    # 7. posts ratio of 3 content type: sidecar, image, video (chart_type: PIE)
    postsRatio = df.groupby('post_type').count()['id']
    postsRatio_x = [i for i in postsRatio.index]
    postsRatio_y = [i for i in postsRatio]
    ####
    
    # 8. Posts List
    most_liked_posts = [i for i in df.sort_values(['likes_count'], ascending=False)['url'].iloc[:20]]
    most_commented_posts =  [i for i in df.sort_values(['comments_count'], ascending=False)['url'].iloc[:20]]
    ####

    analyzed_data = {
        'popularUploadDay': [{ 'x': popularUploadDay_x, 'y': popularUploadDay_y}],
        'popularUploadTime': [{ 'x': popularUploadTime_x, 'y': popularUploadTime_y}],
        'postsPerformance': [{ 'x': postsPerformance_x, 'y1': postsPerformance_y1, 'y2': postsPerformance_y2}],
        'top_hashtags': [{'top_hashtags': top_hashtags}],
        'top_words': [{'top_words': top_words}],
        'postsVolume': [{ 'x': postsVolume_x, 'y': postsVolume_y}],
        'postsRatio': [{ 'x': postsRatio_x, 'y': postsRatio_y}],
        'most_liked_posts': [{'most_liked_posts': most_liked_posts}],
        'most_commented_posts': [{'most_commented_posts': most_commented_posts}]
    }

    return analyzed_data