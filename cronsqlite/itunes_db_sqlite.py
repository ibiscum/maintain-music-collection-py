import os
import plistlib
import re
import sqlite3
import datetime
import hashlib


def subst_quote(input):
    tmp = re.sub(r"'", "''", input)
    return tmp


def connect_db():
    print('connect_db')
    try:
        con = sqlite3.connect('itunes_data.sqlite3')
        return con
    except Exception as error:
        print(error)


def create_table(con):
    print('create_table')
    cur = con.cursor()

    com = 'CREATE TABLE IF NOT EXISTS itunes_data (\
        persistent_id varchar(100) PRIMARY KEY, \
        track_id integer, name text, artist text, album_artist text, \
        album text, genre varchar(100), disc_number smallint, \
        disc_count smallint, track_number smallint, \
        track_count smallint, year date, date_modified timestamp, \
        date_added timestamp, volume_adjustment smallint, \
        play_count integer, play_date_utc timestamp, \
        artwork_count smallint, md5_id varchar(100));'

    cur.execute(com)
    con.commit()
    cur.close()


def check_rows(con):
    print('check_rows')
    cur = con.cursor()

    com = '''SELECT EXISTS (SELECT 1 from itunes_data);'''
    cur.execute(com)

    empty = cur.fetchone()
    cur.close()

    print(empty)
    return empty


def prepare_temp_table(con):
    print('prepare_temp_table')
    cur = con.cursor()

    com = '''DELETE FROM itunes_data_tmp;'''
    cur.execute(com)
    cur.close()


def load_tracks():
    print('load_tracks')
    ITUNES_MUSIC_LIBRARY = os.environ.get('ITUNES_MUSIC_LIBRARY')
    with open(ITUNES_MUSIC_LIBRARY, 'rb') as infile:
        plist = plistlib.load(infile)

    tracks = plist['Tracks']
    return tracks


def prepare_tracks():
    print('prepare_tracks')
    tracks_db = list()
    tracks = load_tracks()

    for track in tracks.values():
        persistent_id = track['Persistent ID']

        track_id = track['Track ID']
        track_id_b = bytes(track_id)

        name = track['Name']
        name_b = bytes(name, 'utf-8')

        artist = track['Artist']
        artist_b = bytes(artist, 'utf-8')

        album_artist = track['Album Artist']
        album_artist_b = bytes(album_artist, 'utf-8')

        album = track['Album']
        album_b = bytes(album, 'utf-8')

        try:
            genre = track['Genre']
        except KeyError:
            genre = 'not set'
        genre_b = bytes(genre, 'utf-8')

        try:
            disc_number = track['Disc Number']
        except KeyError:
            disc_number = 0
        disc_number_b = bytes(disc_number)

        try:
            disc_count = track['Disc Count']
        except KeyError:
            disc_count = 0
        disc_count_b = bytes(disc_count)

        try:
            track_number = track['Track Number']
        except KeyError:
            track_number = 0
        track_number_b = bytes(track_number)

        try:
            track_count = track['Track Count']
        except KeyError:
            track_count = 0
        track_count_b = bytes(track_count)

        try:
            year = str(track['Year']) + '-01-01'
        except KeyError:
            year = '1970-01-01'
        year_b = bytes(year, 'utf-8')

        date_modified = track['Date Modified']
        date_modified_b = bytes(date_modified.strftime('%s'), 'utf-8')

        date_added = track['Date Added']
        date_added_b = bytes(date_added.strftime('%s'), 'utf-8')

        try:
            volume_adjustment = track['Volume Adjustment']
        except KeyError:
            volume_adjustment = 0
        volume_adjustment_b = volume_adjustment.to_bytes(byteorder='little',
                                                         signed=True)

        try:
            play_count = track['Play Count']
        except KeyError:
            play_count = 0
        play_count_b = bytes(play_count)

        try:
            play_date_utc = track['Play Date UTC']
        except KeyError:
            play_date_utc = datetime.datetime(1970, 1, 1, 0, 0, 0)
        play_date_utc_b = bytes(play_date_utc.strftime('%s'), 'utf-8')

        try:
            artwork_count = track['Artwork Count']
        except KeyError:
            artwork_count = 0
        artwork_count_b = bytes(artwork_count)

        elements_b = b''.join([track_id_b, name_b, artist_b,
                              album_artist_b, album_b, genre_b, disc_number_b,
                              disc_count_b, track_number_b, track_count_b,
                              year_b, date_modified_b, date_added_b,
                              volume_adjustment_b, play_count_b,
                              play_date_utc_b, artwork_count_b])

        md5_id = hashlib.md5(elements_b).hexdigest()

        track_item = {
            'persistent_id': persistent_id,
            'track_id': track_id,
            'name': name,
            'artist': artist,
            'album_artist': album_artist,
            'album': album,
            'genre': genre,
            'disc_number': disc_number,
            'disc_count': disc_count,
            'track_number': track_number,
            'track_count': track_count,
            'year': year,
            'date_modified': date_modified,
            'date_added': date_added,
            'volume_adjustment': volume_adjustment,
            'play_count': play_count,
            'play_date_utc': play_date_utc,
            'artwork_count': artwork_count,
            'md5_id': md5_id
        }

        tracks_db.append(track_item)

    return tracks_db


def persist_tracks(table, con):
    print(f'persist_tracks: {table}')
    cur = con.cursor()
    tracks_db = prepare_tracks()

    for track in tracks_db:
        com = f"INSERT INTO {table} (persistent_id, track_id, name,\
            artist, album_artist, album, genre, disc_number, disc_count,\
            track_number, track_count, year, date_modified, date_added,\
            volume_adjustment, play_count, play_date_utc, artwork_count,\
            md5_id)\
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,\
                    ?, ?, ?, ?);"

        cur.execute(com, list(track.values()))

    con.commit()
    cur.close()


def get_ids(con):
    cur = con.cursor()

    com = '''SELECT persistent_id, md5_id FROM itunes_data;'''
    cur.execute(com)

    id_data = cur.fetchall()
    cur.close()

    return id_data


if __name__ == '__main__':
    # init DB
    con = connect_db()
    create_table(con)
    empty = check_rows(con)

    # fill tables
    if empty[0] == 0:
        persist_tracks('itunes_data', con)
    else:
        prepare_temp_table(con)
        persist_tracks('itunes_data_tmp', con)

    con.close()
