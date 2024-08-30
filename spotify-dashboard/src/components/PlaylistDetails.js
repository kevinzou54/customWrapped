import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Typography, Grid } from '@mui/material';

const PlaylistDetails = ({ playlistId }) => {
    const [audioFeatures, setAudioFeatures] = useState([]);

    useEffect(() => {
        if (playlistId) {
            axios.get(`http://127.0.0.1:5000/playlist/${playlistId}`, { withCredentials: true })
                .then(response => setAudioFeatures(response.data))
                .catch(error => console.error('Error fetching playlist details:', error));
        }
    }, [playlistId]);

    return (
        <div>
            <Typography variant="h4">Playlist Audio Features</Typography>
            {audioFeatures.length > 0 ? (
                <Grid container spacing={2}>
                    {audioFeatures.map((feature, index) => (
                        <Grid item xs={12} sm={6} md={4} key={index}>
                            <Typography variant="body1">
                                {feature.track_name} - {feature.artist_name}
                            </Typography>
                            <Typography variant="body2">
                                Danceability: {feature.danceability} <br />
                                Energy: {feature.energy} <br />
                                Tempo: {feature.tempo}
                            </Typography>
                        </Grid>
                    ))}
                </Grid>
            ) : (
                <Typography variant="body1">Select a playlist to view audio features</Typography>
            )}
        </div>
    );
};

export default PlaylistDetails;
