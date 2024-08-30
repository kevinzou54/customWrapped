import React from 'react';
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Button } from '@mui/material';

const Navigation = () => {
    return (
        <AppBar position="static">
            <Toolbar>
                <Button color="inherit" component={Link} to="/dashboard">Dashboard</Button>
                <Button color="inherit" component={Link} to="/playlist-analysis">Playlist Analysis</Button>
                <Button color="inherit" component={Link} to="/custom-tracker">Custom Tracker</Button>
                <Button color="inherit" component={Link} to="/recently-played-tracks">Recently Played Songs</Button>
            </Toolbar>
        </AppBar>
    );
};

export default Navigation;
