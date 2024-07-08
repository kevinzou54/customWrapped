import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime

def fetch_recents():
    # Initialize Spotify client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="190366b387f9484c9afb517f07943550",  # Replace with your actual client_id
    client_secret="27c6a87ddf58434baca7c106cfd95ff6",  # Replace with your new client_secret
    redirect_uri="http://127.0.0.1:9090",  # Ensure this matches the Redirect URI in your Spotify app settings
    scope="user-read-recently-played"
))


    # Connect to the database
    conn = sqlite3.connect('tracks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recently_played_tracks (
            played_at DATETIME PRIMARY KEY,
            track_id TEXT,
            track_name TEXT,
            artist_name TEXT,
            album_name TEXT
        )
    ''')
    conn.commit()
    print("Database commit successful.")

    # Get the most recent 'played_at' timestamp from the database
    cursor.execute('SELECT MAX(played_at) FROM recently_played_tracks')
    last_played_at = cursor.fetchone()[0]

    if last_played_at is not None:
        last_played_at_epoch = int(datetime.datetime.strptime(last_played_at, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() * 1000)
    else:
        last_played_at_epoch = None

    # Fetch tracks from Spotify API using the 'after' parameter
    try:
        if last_played_at_epoch:
            results = sp.current_user_recently_played(limit=50, after=last_played_at_epoch)
        else:
            results = sp.current_user_recently_played(limit=50)
    except Exception as e:
        print(f"Error fetching data from Spotify: {e}")
        conn.close()  # Ensure the connection is closed even when API call fails
        return

    # Check if any tracks are fetched
    tracks = results['items']
    if not tracks:
        print("No new tracks to add.")
        conn.close()
        return

    print(f"Fetched {len(tracks)} tracks from Spotify.")

    # Insertion of fetched tracks into the database
    for item in tracks:
        played_at = item['played_at']
        track_id = item['track']['id']
        track_name = item['track']['name']
        artist_name = item['track']['artists'][0]['name']
        album_name = item['track']['album']['name']

    # Using UPSERT
        sql = '''
        INSERT INTO recently_played_tracks (played_at, track_id, track_name, artist_name, album_name)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(played_at) DO UPDATE SET
        track_id=excluded.track_id,
        track_name=excluded.track_name,
        artist_name=excluded.artist_name,
        album_name=excluded.album_name;
        '''
        try:
            cursor.execute(sql, (played_at, track_id, track_name, artist_name, album_name))
            conn.commit()
        except Exception as e:
            print(f"Error inserting/updating database: {e}")
            conn.rollback()


    conn.close()

def fetch_and_print_ordered_tracks():
    conn = sqlite3.connect('/Users/kevinzou/Desktop/Spotify Wrapped Project/tracks.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT track_name, played_at FROM recently_played_tracks
        ORDER BY played_at DESC
    ''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()    

def fetch_last_10_tracks():
    # Authenticate with Spotify
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id='190366b387f9484c9afb517f07943550',
        client_secret='27c6a87ddf58434baca7c106cfd95ff6',
        redirect_uri='http://127.0.0.1:9090',
        scope='user-read-recently-played'
    ))

    # Fetch the last 10 recently played tracks
    results = sp.current_user_recently_played(limit=10)

    # Print each track's name and the played_at timestamp
    for item in results['items']:
        track_name = item['track']['name']
        played_at = item['played_at']
        print(f"Track: {track_name}, Played At: {played_at}")

def test_connection():
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id='190366b387f9484c9afb517f07943550',
            client_secret='27c6a87ddf58434baca7c106cfd95ff6',
            redirect_uri='http://127.0.0.1:9090',
            scope='user-read-recently-played'
        ))
        results = sp.current_user_recently_played(limit=1)
        print("Successfully connected to Spotify API. Recent track:", results['items'][0]['track']['name'])
    except Exception as e:
        print("Failed to connect to Spotify API:", e)

#test_connection()

# Call the function
fetch_last_10_tracks()


# Run the fetch function
fetch_recents()
# fetch_and_print_ordered_tracks()
