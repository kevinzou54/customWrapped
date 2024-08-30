import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime
import schedule
import time
import os

def fetch_recents():
    print("Starting fetch_recents...")

    # Initialize Spotify client
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id='190366b387f9484c9afb517f07943550',
            client_secret='27c6a87ddf58434baca7c106cfd95ff6',
            redirect_uri='http://127.0.0.1:9090',
            scope="user-read-recently-played"
        ))
        print("Spotify client initialized successfully.")
    except Exception as e:
        print(f"Error initializing Spotify client: {e}")
        return

    # Connect to the database
    try:
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
        print("Database setup completed.")
    except Exception as e:
        print(f"Error setting up database: {e}")
        return

    # Get the most recent 'played_at' timestamp from the database
    try:
        cursor.execute('SELECT MAX(played_at) FROM recently_played_tracks')
        last_played_at = cursor.fetchone()[0]
        print(f"Last played at timestamp in database: {last_played_at}")
    except Exception as e:
        print(f"Error fetching last played timestamp: {e}")
        conn.close()
        return

    if last_played_at is not None:
        last_played_at_epoch = int(datetime.datetime.strptime(last_played_at, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() * 1000)
    else:
        last_played_at_epoch = None

    print(f"last_played_at_epoch: {last_played_at_epoch}")

    # Fetch tracks from Spotify API using the 'after' parameter
    try:
        if last_played_at_epoch:
            print(f"Fetching tracks played after: {last_played_at_epoch}")
            results = sp.current_user_recently_played(limit=50, after=last_played_at_epoch)
        else:
            print("Fetching all recent tracks.")
            results = sp.current_user_recently_played(limit=50)
        print(f"Fetched {len(results['items'])} tracks from Spotify.")
    except Exception as e:
        print(f"Error fetching data from Spotify: {e}")
        conn.close()
        return

    # Print fetched tracks for debugging
    for item in results['items']:
        print(f"Track fetched: {item['track']['name']} at {item['played_at']}")

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

        print(f"Attempting to insert/update track: {track_name} at {played_at}")

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
            print(f"Inserted/Updated track: {track_name} at {played_at}")
        except Exception as e:
            print(f"Error inserting/updating database: {e}")
            conn.rollback()

    conn.close()
    print("Database update completed.")

def fetch_all_recent_tracks():
    print("Fetching all recent tracks without 'after' parameter for comparison.")
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id='190366b387f9484c9afb517f07943550',
            client_secret='27c6a87ddf58434baca7c106cfd95ff6',
            redirect_uri='http://127.0.0.1:9090',
            scope="user-read-recently-played"
        ))
        results = sp.current_user_recently_played(limit=50)
        print(f"Fetched {len(results['items'])} tracks from Spotify without 'after' parameter.")
        for item in results['items']:
            print(f"Track fetched: {item['track']['name']} at {item['played_at']}")
    except Exception as e:
        print(f"Error fetching data from Spotify: {e}")

def count_song_plays():
    print("Counting song plays...")
    try:
        conn = sqlite3.connect('tracks.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT track_name, artist_name, album_name, track_id, COUNT(*) as play_count
            FROM recently_played_tracks
            GROUP BY track_name, artist_name, album_name, track_id
            ORDER BY play_count DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        # Debugging: Print fetched rows
        for row in rows:
            print(f"Row: track_name={row[0]}, artist_name={row[1]}, album_name={row[2]}, track_id={row[3]}, play_count={row[4]}")
        return rows
    except Exception as e:
        print(f"Error counting song plays: {e}")
        return []
    
def create_spotify_playlist_from_db():
    print("Creating Spotify playlist from database...")
    tracks = count_song_plays()
    if not tracks:
        print("No tracks found in database.")
        return

    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id='190366b387f9484c9afb517f07943550',
            client_secret='27c6a87ddf58434baca7c106cfd95ff6',
            redirect_uri='http://127.0.0.1:9090',
            scope="playlist-modify-public"
        ))

        # Get the current user's ID
        user_id = sp.current_user()['id']
        print(f"User ID: {user_id}")

        # Create a new playlist
        playlist_name = "Most Played Tracks"
        playlist_description = "A playlist of my most played tracks"
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, description=playlist_description)
        playlist_id = playlist['id']
        print(f"Created playlist: {playlist_name} (ID: {playlist_id})")

        # Add tracks to the playlist
        track_ids = [str(row[3]) for row in tracks if isinstance(row[3], str) and len(row[3]) == 22]  # Ensure track IDs are valid Spotify IDs (22 characters long)
        print(f"Track IDs to be added: {track_ids}")  # Debugging statement
        for i in range(0, len(track_ids), 100):  # Spotify API limits to 100 tracks per request
            batch = track_ids[i:i+100]
            print(f"Adding batch to playlist: {batch}")  # Debugging statement
            sp.playlist_add_items(playlist_id, batch)
        print(f"Added {len(track_ids)} tracks to the playlist.")
    except Exception as e:
        print(f"Error creating Spotify playlist: {e}")

if os.path.exists('.cache'):
    os.remove('.cache')

def fetch_top_tracks_and_recommend():
    print("Fetching top tracks and generating recommendations...")

    # Initialize Spotify client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id='190366b387f9484c9afb517f07943550',
            client_secret='27c6a87ddf58434baca7c106cfd95ff6',
            redirect_uri='http://127.0.0.1:9090',
            scope="user-top-read user-read-recently-played playlist-modify-public"
    ))

    # Get user's top tracks
    top_tracks = sp.current_user_top_tracks(limit=5)
    seed_tracks = [track['id'] for track in top_tracks['items']]
    print("Seed Tracks:", seed_tracks)

    # Get recommendations
    recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=20)
    recommended_tracks = [(track['name'], track['artists'][0]['name']) for track in recommendations['tracks']]
    print("Recommended Tracks:", recommended_tracks)

    # Connect to the database
    conn = sqlite3.connect('tracks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommended_tracks (
            track_name TEXT,
            artist_name TEXT
        )
    ''')

    # Insert recommended tracks into the database
    for track in recommended_tracks:
        cursor.execute('''
            INSERT INTO recommended_tracks (track_name, artist_name)
            VALUES (?, ?)
        ''', track)

    conn.commit()
    conn.close()
    print("Database updated with recommended tracks.")

# Schedule the task to run periodically
schedule.every().day.at("10:00").do(fetch_top_tracks_and_recommend)

# Run immediately for testing
fetch_top_tracks_and_recommend()






# Schedule the fetch_recents function to run every 3 hours
#schedule.every(3).hours.do(fetch_recents)

# Run immediately for testing
# 
#fetch_all_recent_tracks()

# Keep the script running
# while True:
#      schedule.run_pending()
#      time.sleep(1)
