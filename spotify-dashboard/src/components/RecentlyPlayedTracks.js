import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navigation from './Navigation';

const RecentlyPlayedTracks = () => {
    const [tracks, setTracks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchRecentTracks = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/recent-tracks');
            setTracks(response.data.tracks || []);
        } catch (err) {
            setError(err.message || 'Error fetching tracks');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRecentTracks();
    }, []);

    return (
        <div>
            <Navigation />
            <h2>Recently Played Tracks</h2>
            <button onClick={fetchRecentTracks}>Refresh</button>
            {loading ? <p>Loading...</p> : null}
            {error ? <p>Error: {error}</p> : null}
            <ul>
                {tracks.map((track, index) => (
                    <li key={index}>
                        <strong>{track.track_name}</strong> by {track.artist_name} from the album {track.album_name} (Played at: {track.played_at})
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default RecentlyPlayedTracks;
