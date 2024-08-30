import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Typography, Container, Grid, Card, CardContent, CardActions, Button } from '@mui/material';
import PlaylistAnalysis from './PlaylistAnalysis';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import Navigation from './Navigation';

const Dashboard = () => {
    const [playlists, setPlaylists] = useState([]);
    const [selectedPlaylist, setSelectedPlaylist] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchPlaylists = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/playlists', { withCredentials: true });
                
                console.log("Playlists data:", response.data);  // Log response data

                // Ensure the data is in the expected format (items array should be present)
                if (response.data && response.data.items && Array.isArray(response.data.items)) {
                    setPlaylists(response.data.items);
                    console.log("Setting Playlists:", response.data.items);
                } else {
                    console.log("No playlists found or data is not in expected format.");
                    setPlaylists([]);
                }
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    Cookies.remove('spotify_token');
                    navigate('/');
                } else {
                    console.error('Error fetching playlists:', error);
                }
            }
        };
    
        const token = Cookies.get('spotify_token');
        if (!token) {
            navigate('/');
        } else {
            fetchPlaylists();
        }
    }, [navigate]);

    return (
        <Container>
            <Navigation />
            <Typography variant="h4" gutterBottom>
                Your Playlists
            </Typography>
            <Grid container spacing={3}>
                {playlists.length > 0 ? (
                    playlists.map((playlist) => (
                        <Grid item xs={12} sm={6} md={4} key={playlist.id}>
                            <Card>
                                <CardContent>
                                    <Typography variant="h6">{playlist.name}</Typography>
                                    <Typography variant="body2" color="textSecondary">
                                        {playlist.tracks.total} tracks
                                    </Typography>
                                    {playlist.images && playlist.images.length > 0 ? (
                                        <img
                                            src={playlist.images[0].url}
                                            alt={playlist.name}
                                            style={{ width: '100%', height: 'auto' }}
                                        />
                                    ) : (
                                        <Typography variant="body2" color="textSecondary">
                                            No image available
                                        </Typography>
                                    )}
                                </CardContent>
                                <CardActions>
                                    <Button size="small" color="primary" onClick={() => setSelectedPlaylist(playlist.id)}>
                                        View Details
                                    </Button>
                                </CardActions>
                            </Card>
                        </Grid>
                    ))
                ) : (
                    <Typography variant="body2">No playlists found.</Typography>
                )}
            </Grid>
            {selectedPlaylist && <PlaylistAnalysis playlistId={selectedPlaylist} />}
        </Container>
    );
};

export default Dashboard;
