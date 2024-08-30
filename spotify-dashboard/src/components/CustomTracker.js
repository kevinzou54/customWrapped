import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button, List, ListItem, ListItemText, Typography, CircularProgress, ButtonGroup } from '@mui/material';
import dayjs from 'dayjs';  // Install dayjs with `npm install dayjs`
import Navigation from './Navigation';

const CustomTracker = () => {
    const [tracks, setTracks] = useState([]);
    const [filteredTracks, setFilteredTracks] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [timeFilter, setTimeFilter] = useState('daily'); // 'daily', 'weekly', 'monthly', 'yearly'

    const fetchRecentTracks = async () => {
        setLoading(true);
        setError(null);

        try {
            await axios.get('http://127.0.0.1:5000/fetch-recent-tracks');
            fetchTracksFromDatabase();
        } catch (err) {
            setError(err.message || 'Error fetching tracks');
        } finally {
            setLoading(false);
        }
    };

    const fetchTracksFromDatabase = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await axios.get('http://127.0.0.1:5000/get-tracks');
            setTracks(response.data.tracks || []);
        } catch (err) {
            setError(err.message || 'Error fetching tracks');
        } finally {
            setLoading(false);
        }
    };

    const filterAndGroupTracks = (tracks, filterType) => {
        const now = dayjs();

        // Filter tracks based on the selected time period
        const filtered = tracks.filter(track => {
            const playedAt = dayjs(track.played_at);
            switch (filterType) {
                case 'daily':
                    return playedAt.isAfter(now.subtract(1, 'day'));
                case 'weekly':
                    return playedAt.isAfter(now.subtract(1, 'week'));
                case 'monthly':
                    return playedAt.isAfter(now.subtract(1, 'month'));
                case 'yearly':
                    return playedAt.isAfter(now.subtract(1, 'year'));
                default:
                    return true;
            }
        });

        // Group tracks by song ID and count occurrences
        const trackMap = {};
        filtered.forEach(track => {
            const key = `${track.track_name}-${track.artist_name}`; // Unique key based on track name and artist
            if (!trackMap[key]) {
                trackMap[key] = {
                    ...track,
                    count: 1,
                };
            } else {
                trackMap[key].count += 1;
            }
        });

        // Convert object to array and sort by count
        const groupedAndSortedTracks = Object.values(trackMap).sort((a, b) => b.count - a.count);
        return groupedAndSortedTracks;
    };

    // Apply filter when tracks or time filter changes
    useEffect(() => {
        setFilteredTracks(filterAndGroupTracks(tracks, timeFilter));
    }, [tracks, timeFilter]);

    // Fetch tracks when the component mounts
    useEffect(() => {
        fetchTracksFromDatabase();
    }, []);

    return (
        <div>
            <Typography variant="h4" gutterBottom>
                Custom Tracker
            </Typography>

            {/* Button to manually refresh the list */}
            <Button variant="contained" color="primary" onClick={fetchRecentTracks} disabled={loading}>
                {loading ? <CircularProgress size={24} /> : "Refresh"}
            </Button>

            {/* Display error if any */}
            {error && <Typography color="error">Error: {error}</Typography>}

            {/* Time period selection buttons */}
            <ButtonGroup color="primary" variant="contained" aria-label="outlined primary button group" style={{ margin: '20px 0' }}>
                <Button onClick={() => setTimeFilter('daily')}>Daily</Button>
                <Button onClick={() => setTimeFilter('weekly')}>Weekly</Button>
                <Button onClick={() => setTimeFilter('monthly')}>Monthly</Button>
                <Button onClick={() => setTimeFilter('yearly')}>Yearly</Button>
            </ButtonGroup>

            {/* Display tracks if available */}
            {filteredTracks.length > 0 ? (
                <List>
                    {filteredTracks.map((track, index) => (
                        <ListItem key={index} divider>
                            <ListItemText
                                primary={`${track.track_name} by ${track.artist_name}`}
                                secondary={`Album: ${track.album_name} | Played ${track.count} times | Last Played: ${new Date(track.played_at).toLocaleString()}`}
                            />
                        </ListItem>
                    ))}
                </List>
            ) : !loading && (
                <Typography>No tracks found</Typography>
            )}
        </div>
    );
};

export default CustomTracker;
