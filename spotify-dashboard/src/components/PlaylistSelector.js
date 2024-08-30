import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Select, MenuItem, FormControl, InputLabel, Button, Typography } from '@mui/material';

const PlaylistSelector = ({ onSelect }) => {
    const [playlists, setPlaylists] = useState([]);
    const [authenticated, setAuthenticated] = useState(false);

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/token', { withCredentials: true })
            .then(response => {
                setAuthenticated(true);
                fetchPlaylists();
            })
            .catch(error => {
                if (error.response && error.response.status === 401) {
                    setAuthenticated(false);
                } else {
                    console.error('Error fetching token info:', error);
                }
            });
    }, []);

    const fetchPlaylists = () => {
        axios.get('http://127.0.0.1:5000/playlists', { withCredentials: true })
            .then(response => setPlaylists(response.data.items))
            .catch(error => console.error('Error fetching playlists:', error));
    };

    return (
        <div>
            {!authenticated ? (
                <Button variant="contained" color="primary" href="http://127.0.0.1:5000/">
                    Authenticate with Spotify
                </Button>
            ) : (
                <>
                    <Typography variant="h5" gutterBottom>
                        Select a Playlist
                    </Typography>
                    <FormControl fullWidth>
                        <InputLabel id="playlist-select-label">Select Playlist</InputLabel>
                        <Select
                            labelId="playlist-select-label"
                            onChange={(e) => onSelect(e.target.value)}
                        >
                            {playlists.map((playlist) => (
                                <MenuItem key={playlist.id} value={playlist.id}>
                                    {playlist.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </>
            )}
        </div>
    );
};

export default PlaylistSelector;
