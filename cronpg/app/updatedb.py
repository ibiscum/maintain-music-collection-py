import plistlib
import re
import psycopg2
from psycopg2 import Error
import datetime
from hashlib import sha256
# import pprint
from settings import ITUNES_LIBRARY_FILE, ITUNES_MUSIC_DIR, \
    DB_PASSWORD, DB_SCHEMA, DB_HOST


def subst_quote(input):
    tmp = re.sub(r"'", "''", input)
    return tmp


def connect_db():
    try:
        conn = psycopg2.connect(
            user='postgres',
            password=DB_PASSWORD,
            host=DB_HOST,
            port='5432',
            database=DB_SCHEMA)
        return conn
    except (Exception, Error) as error:
        print(error)


table_itunes_data = 'CREATE TABLE IF NOT EXISTS itunes_data (\
        persistent_id varchar(100) PRIMARY KEY, \
        track_id integer,           \
        track_name text,            \
        artist text,                \
        album_artist text,          \
        album text,                 \
        genre varchar(100),         \
        disc_number smallint,       \
        disc_count smallint,        \
        track_number smallint,      \
        track_count smallint,       \
        album_year date,            \
        date_modified timestamp,    \
        date_added timestamp,       \
        volume_adjustment smallint, \
        play_count integer,         \
        play_date_utc timestamp,    \
        artwork_count smallint,     \
        sha256_id varchar(100));'


def create_table(command):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(command)
    conn.commit()
    conn.close()


def load_tracks():
    itunes_lib = ITUNES_MUSIC_DIR + "/" + ITUNES_LIBRARY_FILE
    with open(itunes_lib, 'rb') as infile:
        plist = plistlib.load(infile)

    tracks = plist['Tracks']
    return tracks


def prepare_tracks():
    tracks_db = list()
    tracks = load_tracks()

    for track in tracks.values():
        h = sha256()

        persistent_id = track['Persistent ID']
        print(persistent_id)

        track_id = track['Track ID']
        track_id_b = track_id.to_bytes(4, 'little')
        h.update(track_id_b)

        track_name = track['Name']
        track_name_b = bytes(track_name, 'utf-8')
        h.update(track_name_b)

        artist = track['Artist']
        artist_b = bytes(artist, 'utf-8')
        h.update(artist_b)

        album_artist = track['Album Artist']
        album_artist_b = bytes(album_artist, 'utf-8')
        h.update(album_artist_b)

        album = track['Album']
        album_b = bytes(album, 'utf-8')
        h.update(album_b)

        try:
            genre = track['Genre']
        except KeyError:
            genre = 'not set'
        genre_b = bytes(genre, 'utf-8')
        h.update(genre_b)

        try:
            disc_number = track['Disc Number']
        except KeyError:
            disc_number = 0
        disc_number_b = disc_number.to_bytes(2, 'little')
        h.update(disc_number_b)

        try:
            disc_count = track['Disc Count']
        except KeyError:
            disc_count = 0
        disc_count_b = disc_count.to_bytes(2, 'little')
        h.update(disc_count_b)

        try:
            track_number = track['Track Number']
        except KeyError:
            track_number = 0
        track_number_b = track_number.to_bytes(2, 'little')
        h.update(track_number_b)

        try:
            track_count = track['Track Count']
        except KeyError:
            track_count = 0
        track_count_b = track_count.to_bytes(2, 'little')
        h.update(track_count_b)

        try:
            album_year = str(track['Year']) + '-01-01'
        except KeyError:
            album_year = '1970-01-01'
        album_year_b = bytes(album_year, 'utf-8')
        h.update(album_year_b)

        date_modified = track['Date Modified']
        date_modified_b = bytes(date_modified.strftime('%s'), 'utf-8')
        h.update(date_modified_b)

        date_added = track['Date Added']
        date_added_b = bytes(date_added.strftime('%s'), 'utf-8')
        h.update(date_added_b)

        try:
            volume_adjustment = track['Volume Adjustment']
        except KeyError:
            volume_adjustment = 0
        volume_adjustment_b = volume_adjustment.to_bytes(2, byteorder='little',
                                                         signed=True)
        h.update(volume_adjustment_b)

        try:
            play_count = track['Play Count']
        except KeyError:
            play_count = 0
        play_count_b = play_count.to_bytes(2, 'little')
        h.update(play_count_b)

        try:
            play_date_utc = track['Play Date UTC']
        except KeyError:
            play_date_utc = datetime.datetime(1970, 1, 1, 0, 0, 0)
        play_date_utc_b = bytes(play_date_utc.strftime('%s'), 'utf-8')
        h.update(play_date_utc_b)

        try:
            artwork_count = track['Artwork Count']
        except KeyError:
            artwork_count = 0
        artwork_count_b = artwork_count.to_bytes(2, 'little')
        h.update(artwork_count_b)

        sha256_id = h.hexdigest()

        print(sha256_id)
        print("----------------------\n")

        track_item = {
            'persistent_id': persistent_id,
            'track_id': track_id,
            'track_name': track_name,
            'artist': artist,
            'album_artist': album_artist,
            'album': album,
            'genre': genre,
            'disc_number': disc_number,
            'disc_count': disc_count,
            'track_number': track_number,
            'track_count': track_count,
            'album_year': album_year,
            'date_modified': date_modified,
            'date_added': date_added,
            'volume_adjustment': volume_adjustment,
            'play_count': play_count,
            'play_date_utc': play_date_utc,
            'artwork_count': artwork_count,
            'sha256_id': sha256_id
        }

        tracks_db.append(track_item)

    return tracks_db


def persist_tracks():
    # ct = datetime.datetime.now()
    # ts = ct.timestamp()

    conn = connect_db()
    cur = conn.cursor()

    id_data = get_ids()

    tracks_db = prepare_tracks()

    for track in tracks_db:
        if track.get('sha256_id') not in id_data:
            command = '''INSERT INTO itunes_data (
                persistent_id,
                track_id,
                track_name,
                artist,
                album_artist,
                album, genre,
                disc_number,
                disc_count,
                track_number,
                track_count,
                album_year,
                date_modified,
                date_added,
                volume_adjustment,
                play_count,
                play_date_utc,
                artwork_count,
                sha256_id)
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s)
                ON CONFLICT (persistent_id) DO UPDATE SET
                    track_id          = EXCLUDED.track_id,
                    track_name        = EXCLUDED.track_name,
                    artist            = EXCLUDED.artist,
                    album_artist      = EXCLUDED.album_artist,
                    album             = EXCLUDED.album,
                    genre             = EXCLUDED.genre,
                    disc_number       = EXCLUDED.disc_number,
                    disc_count        = EXCLUDED.disc_count,
                    track_number      = EXCLUDED.track_number,
                    track_count       = EXCLUDED.track_count,
                    album_year        = EXCLUDED.album_year,
                    date_modified     = EXCLUDED.date_modified,
                    date_added        = EXCLUDED.date_added,
                    volume_adjustment = EXCLUDED.volume_adjustment,
                    play_count        = EXCLUDED.play_count,
                    play_date_utc     = EXCLUDED.play_date_utc,
                    artwork_count     = EXCLUDED.artwork_count,
                    sha256_id            = EXCLUDED.sha256_id;'''

            cur.execute(command, (
                track.get('persistent_id'),
                track.get('track_id'),
                track.get('track_name'),
                track.get('artist'),
                track.get('album_artist'),
                track.get('album'),
                track.get('genre'),
                track.get('disc_number'),
                track.get('disc_count'),
                track.get('track_number'),
                track.get('track_count'),
                track.get('album_year'),
                track.get('date_modified'),
                track.get('date_added'),
                track.get('volume_adjustment'),
                track.get('play_count'),
                track.get('play_date_utc'),
                track.get('artwork_count'),
                track.get('sha256_id'))
            )

    conn.commit()
    conn.close()


def get_ids():
    conn = connect_db()
    cur = conn.cursor()

    command = '''SELECT sha256_id, persistent_id FROM itunes_data;'''
    cur.execute(command)

    id_data = cur.fetchall()

    conn.commit()
    conn.close()

    return dict(id_data)
