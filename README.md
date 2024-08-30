# Spotify Custom Tracker and Playlist Analyzer

This project is a web application that integrates with the Spotify API to provide users with a custom music tracker and playlist analysis functionality. Users can track their music listening habits over various time periods (daily, weekly, monthly, yearly) and analyze their playlists. The application is built using React for the frontend and Flask for the backend.

## Features

- **Custom Tracker**: Allows users to track their Spotify listening habits over specified intervals (daily, weekly, monthly, yearly). The application fetches recently played tracks from Spotify, stores them in a SQLite database, and displays the most played songs for the selected time period.
- **Playlist Analysis**: Users can analyze their Spotify playlists, retrieving detailed statistics and information about the tracks within each playlist.

## Technologies Used

- **Frontend**:
  - React: JavaScript library for building user interfaces.
  - Material-UI: React components for faster and easier web development.
  - Axios: Promise-based HTTP client for the browser and Node.js.
  - Day.js: Minimalist JavaScript library for date manipulation.

- **Backend**:
  - Flask: Micro web framework written in Python.
  - Spotipy: A light-weight Python library for the Spotify Web API.
  - SQLite: A C-language library that implements a small, fast, self-contained SQL database engine.
  - Flask-CORS: A Flask extension for handling Cross-Origin Resource Sharing (CORS), making cross-origin AJAX possible.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Node.js** (version 14 or later)
- **npm** (Node Package Manager)
- **Python** (version 3.8 or later)
- **pip** (Python Package Installer)

## Getting Started

### 1. Clone the Repository

bash
git clone https://github.com/yourusername/spotify-custom-tracker.git
cd spotify-custom-tracker

### 2. Backend Startup
cd backend
python3 -m venv venv  # Create a virtual environment
source venv/bin/activate  # Activate the virtual environment (Linux/MacOS)
venv\Scripts\activate  # Activate the virtual environment (Windows)

pip install Flask spotipy Flask-CORS

pip install -r requirements.txt  # Install required Python packages


### 3. Run the Backend Server
flask run

### 4. Front End Setup 
cd ../frontend
npm install 

### 4. Run Development Server 
npm start

### 5. Usage
Start by authenticating your spotify account. The button should redirect you to a spotify log in page which will prompt you for the relevant information. 
Once you have authenticated you will see a navigation bar which includes tabs which say "playlist analysis", "custom wrapped", and "recently played songs".
Playlist analysis is currently not implemented. Custom wrapped will allow you to organize your recently played songs into categories of daily, weekly, monthly, and yearly 
which will display songs played with their playcounts during those time periods. 

