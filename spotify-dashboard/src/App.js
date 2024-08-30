import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import { Container, Typography, Button } from '@mui/material';
import Cookies from 'js-cookie';
import PlaylistAnalysis from './components/PlaylistAnalysis';
import CustomTracker from './components/CustomTracker';
import RecentlyPlayedTracks from './components/RecentlyPlayedTracks';

const App = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const token = Cookies.get('spotify_token');
        if (token) {
            setIsAuthenticated(true);
        } else {
            setIsAuthenticated(false);
            navigate('/');
        }
    }, [navigate]);

    const handleAuthentication = () => {
        window.location.href = 'http://127.0.0.1:5000/callback'; // Replace this with your authentication endpoint
    };

    return (
        <Container>
            <Routes>
                {/* Home Route */}
                <Route path="/" element={
                    <>
                        <Typography variant="h3" gutterBottom>
                            Spotify Playlist Analyzer
                        </Typography>
                        {!isAuthenticated && (
                            <Button variant="contained" color="primary" onClick={handleAuthentication}>
                                Authenticate with Spotify
                            </Button>
                        )}
                        {isAuthenticated && (
                            <Typography variant="h6" gutterBottom>
                                You are authenticated! Use the menu to navigate.
                            </Typography>
                        )}
                    </>
                } />

                {/* Dashboard Route */}
                <Route path="/dashboard" element={<Dashboard />} />

                {/* Playlist Analysis Route */}
                <Route path="/playlist-analysis" element={<PlaylistAnalysis />} />

                {/* Custom Tracker Route */}
                <Route path="/custom-tracker" element={<CustomTracker />} />

                <Route path="/recently-played-tracks" element={<RecentlyPlayedTracks />} />  
            </Routes>
        </Container>
    );
};

// AppWrapper to wrap the main app in the Router
const AppWrapper = () => (
    <Router>
        <App />
    </Router>
);

export default AppWrapper;
