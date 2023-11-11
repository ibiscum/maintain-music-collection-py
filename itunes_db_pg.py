import os
import plistlib
import re
import psycopg2
from psycopg2 import Error
import time
import datetime
import hashlib
import pprint
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import PatternMatchingEventHandler


def subst_quote(input):
    tmp = re.sub(r"'", "''", input)
    return tmp


class WatchLibFile:
    # Set the directory on watch
    watchDirectory = "/mnt/win_Music/iTunes/"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = ModEventHandler()
        self.observer.schedule(event_handler, self.watchDirectory,
                               recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class ModEventHandler(PatternMatchingEventHandler):
    def __init__(self):
        PatternMatchingEventHandler.__init__(
            self,
            patterns=["*.xml"],
            ignore_directories=True,
            case_sensitive=False,
        )

    def on_any_event(self, event):
        print(
            "[{}] noticed: [{}] on: [{}] ".format(
                time.asctime(), event.event_type, event.src_path
            )
        )

        if event.event_type == 'created':
            conn = connect_db()
            create_table(conn)
            tracks = load_tracks()
            # persist_tracks(tracks)


def connect_db():
    try:
        conn = psycopg2.connect(user='postgres', password='secret',
                                host='localhost', port='5432',
                                database='music')
        return conn
    except (Exception, Error) as error:
        print(error)


def create_table():
    conn = connect_db()
    cur = conn.cursor()

    command = 'CREATE TABLE IF NOT EXISTS itunes_data (\
        persistent_id varchar(100) PRIMARY KEY, \
        track_id integer, name text, artist text, album_artist text, \
        album text, genre varchar(100), disc_number smallint, \
        disc_count smallint, track_number smallint, \
        track_count smallint, year date, date_modified timestamp, \
        date_added timestamp, volume_adjustment smallint, \
        play_count integer, play_date_utc timestamp, \
        artwork_count smallint, md5_id varchar(100));'

    cur.execute(command)
    conn.commit()
    conn.close()


def load_tracks():
    ITUNES_MUSIC_LIBRARY = os.environ.get('ITUNES_MUSIC_LIBRARY')
    with open(ITUNES_MUSIC_LIBRARY, 'rb') as infile:
        plist = plistlib.load(infile)

    tracks = plist['Tracks']
    return tracks


def prepare_tracks():
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


def persist_tracks_initial():
    conn = connect_db()
    cur = conn.cursor()
    tracks_db = prepare_tracks()
    pp = pprint.PrettyPrinter()

    for track in tracks_db:
        pp.pprint(track)

        command = '''INSERT INTO itunes_data (persistent_id, track_id, name,
            artist, album_artist, album, genre, disc_number, disc_count,
            track_number, track_count, year, date_modified, date_added,
            volume_adjustment, play_count, play_date_utc, artwork_count,
            md5_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s)
            ON CONFLICT (persistent_id) DO UPDATE SET
            track_id = EXCLUDED.track_id,
            name = EXCLUDED.name,
            artist = EXCLUDED.artist,
            album_artist = EXCLUDED.album_artist,
            album = EXCLUDED.album, genre = EXCLUDED.genre,
            disc_number = EXCLUDED.disc_number,
            disc_count = EXCLUDED.disc_count,
            track_number = EXCLUDED.track_number,
            track_count = EXCLUDED.track_count,
            year = EXCLUDED.year,
            date_modified = EXCLUDED.date_modified,
            date_added = EXCLUDED.date_added,
            volume_adjustment = EXCLUDED.volume_adjustment,
            play_count = EXCLUDED.play_count,
            play_date_utc = EXCLUDED.play_date_utc,
            artwork_count = EXCLUDED.artwork_count,
            md5_id = EXCLUDED.md5_id;'''

        # cur.execute(command, (
        #    persistent_id, track_id, name, artist, album_artist,
        #    album, genre, disc_number, disc_count, track_number,
        #    track_count, year, date_modified, date_added,
        #    volume_adjustment, play_count, play_date_utc,
        #    artwork_count, md5_id
        # ))
        cur.execute(command, track)

    conn.commit()
    conn.close()


def get_ids():
    conn = connect_db()
    cur = conn.cursor()

    command = '''SELECT persistent_id, md5_id FROM itunes_data;'''
    cur.execute(command)

    id_data = cur.fetchall()
    return id_data


if __name__ == '__main__':
    # init DB
    create_table()
    persist_tracks_initial()
    id_data = get_ids()
    tracks_db = prepare_tracks()

    watch = WatchLibFile()
    watch.run()
