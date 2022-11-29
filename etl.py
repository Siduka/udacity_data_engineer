import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    This function processes a song file whose filepath has been provided as an arugment.
    It extracts the song information in order to store it into the songs table.
    Then it extracts the artist information in order to store it into the artists table.

    INPUTS: 
    * cur the cursor variable
    * filepath the file path to the song file
    """
    # open song file
    df = pd.read_json(filepath, lines = True)

    # insert song record
    song_data = [df.values[0][7], df.values[0][8], df.values[0][0], df.values[0][9],df.values[0][5]]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = [df.values[0][0], df.values[0][4], df.values[0][2], df.values[0][1],df.values[0][3]]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This function processes a log file whose filepath has been provided as an arugment.
    First, it extracts timestamp and convert it into different units and store them into time table.
    Then, it extracts the user information in order to store it into the users table.
    At last, it extracts songid, artist by joining artists and songs table to store it to songplay_data table 
    along with data from log file. artist information in order to store it into the artists table.

    INPUTS: 
    * cur the cursor variable
    * filepath the file path to the song file
    """
    # open log file
    df = pd.read_json(filepath,lines = True)

    # filter by NextSong action
    df = df[df.page == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df.ts, unit='ms')
    # add a new standardized timestamp column
    df['timestamp'] = t
    
    # insert time data records
    time_data = (t.values, t.dt.hour.values, t.dt.day.values, t.dt.week.values, t.dt.month.values, t.dt.year.values, t.dt.weekday.values)
    column_labels = ('start_time', 'hour', 'day' , 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    
    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        #song_select = ("""SELECT songs.song_id, artists.artist_id  FROM songs join artists ON songs.artist_id = artists.artist_id where songs.title = %s AND artists.name = %s AND songs.duration=%s""")

        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record, use each row ts as primary key
        songplay_data = (row.timestamp, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    This function processes function passed in.
    First, it creates a list of files in the filepath.
    Then it loops through all the files in the list and process each file by the function.

    INPUTS: 
    * cur: the cursor variable
    * conn: the connection variable
    * filepath: the filepath variable
    * func: the function to be processed
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()