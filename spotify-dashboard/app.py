from flask import Flask, request, jsonify, redirect, session, url_for
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sqlite3
import os
import datetime
import time

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=['http://127.0.0.1:3000'])
app.secret_key = os.urandom(24)
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

sp_oauth = SpotifyOAuth(
    client_id='190366b387f9484c9afb517f07943550',
    client_secret='27c6a87ddf58434baca7c106cfd95ff6',
    redirect_uri='http://127.0.0.1:5000/callback',
    scope="playlist-read-private user-read-recently-played user-top-read"
)

@app.route('/')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/fetch-recent-tracks', methods=['GET'])
def fetch_recents():
    # Initialize Spotify client
    sp = spotipy.Spotify(auth_manager=sp_oauth)

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
        conn.close()
        return jsonify({"error": "Failed to fetch tracks"}), 500

    # Check if any tracks are fetched
    tracks = results['items']
    if not tracks:
        conn.close()
        return jsonify({"message": "No new tracks to add."}), 200

    # Insertion of fetched tracks into the database
    for item in tracks:
        played_at = item['played_at']
        track_id = item['track']['id']
        track_name = item['track']['name']
        artist_name = item['track']['artists'][0]['name']
        album_name = item['track']['album']['name']

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
    return jsonify({"message": "Tracks fetched and database updated"}), 200

@app.route('/get-tracks', methods=['GET'])
def get_tracks():
    conn = sqlite3.connect('tracks.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT track_name, artist_name, album_name, played_at 
        FROM recently_played_tracks
        ORDER BY played_at DESC
    ''')
    tracks = [{"track_name": row[0], "artist_name": row[1], "album_name": row[2], "played_at": row[3]} for row in cursor.fetchall()]
    conn.close()
    return jsonify({"tracks": tracks})

@app.route('/fetch-recent-tracks', methods=['GET'])
def fetch_recent_tracks():
    # Get the token and refresh if necessary
    print("Fetching recent tracks...")
    token_info = get_token()

    if not token_info:
        print("Token is invalid or expired.")
        return jsonify({'error': 'Token expired or invalid.'}), 401
    
    try:
        sp = spotipy.Spotify(auth=token_info['access_token'])
    except Exception as e:
        print(f"Error initializing Spotify client: {e}")
        return jsonify({"error": "Failed to initialize Spotify client"}), 500
    
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
        conn.close()
        return jsonify({"error": "Failed to fetch tracks"}), 500

    # Insert fetched tracks into the database
    for item in results['items']:
        played_at = item['played_at']
        track_id = item['track']['id']
        track_name = item['track']['name']
        artist_name = item['track']['artists'][0]['name']
        album_name = item['track']['album']['name']

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
    return jsonify({"message": "Tracks fetched and database updated"}), 200

@app.route('/recent-tracks', methods=['GET'])
def recent_tracks():
    conn = sqlite3.connect('tracks.db')
    cursor = conn.cursor()
    
    # Fetch the most recent tracks
    cursor.execute('''
        SELECT track_name, artist_name, album_name, played_at
        FROM recently_played_tracks
        ORDER BY played_at DESC
        LIMIT 10
    ''')

    tracks = [{"track_name": row[0], "artist_name": row[1], "album_name": row[2], "played_at": row[3]} for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({"tracks": tracks})

@app.route('/callback')
def callback():
    #session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    response = redirect('http://127.0.0.1:3000/dashboard')
    response.set_cookie('spotify_token', token_info['access_token'], samesite='Lax')
    return response

def get_token():
    token_info = sp_oauth.get_cached_token()
    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
        print(access_token)
    else:
        url = request.url
        print(url)
        print("No token found in session.")
        return None

    now = int(time.time())
    print(f"Current time: {now}, Token expires at: {token_info['expires_at']}")
    
    if token_info['expires_at'] - now < 60:
        print("Token expired, refreshing...")
        try:
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info
            print("Token refreshed:", token_info)
        except Exception as e:
            print(f"Failed to refresh token: {e}")
            return None

    return token_info





if __name__ == '__main__':
    app.run(port=5000)
