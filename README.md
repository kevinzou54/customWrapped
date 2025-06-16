# Spotify Custom Tracker and Playlist Analyzer

This project is a web application that integrates with the Spotify API to provide users with a custom music tracker and playlist analysis functionality. Users can track their music listening habits over various time periods (daily, weekly, monthly, yearly) and analyze their playlists. The application is built using React for the frontend and Flask for the backend.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Backend Setup](#2-backend-setup)
  - [3. Frontend Setup](#3-frontend-setup)
  - [4. Running the Application](#4-running-the-application)
  - [5. Usage](#5-usage)
- [Contributing](#contributing)
- [License](#license)

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

## Project Structure

The project is organized into two main parts:

-   **Backend**: A Flask application that handles the server-side logic, API interactions with Spotify, and database management.
-   **Frontend**: A React application located in the `spotify-dashboard` directory. This application provides the user interface.
    -   For specific instructions on running the frontend, please refer to the `README.md` file within the `spotify-dashboard` directory.

## Getting Started

Follow these steps to set up and run the application:

### 1. Clone the Repository

```bash
git clone https://github.com/username/repository-name.git
cd repository-name
```

### 2. Backend Setup

Navigate to the backend directory and set up the Python virtual environment.

```bash
cd backend
python3 -m venv venv  # Create a virtual environment
source venv/bin/activate  # Activate the virtual environment (Linux/MacOS)
# For Windows:
# venv\Scripts\activate
pip install -r requirements.txt  # Install required Python packages
```

### 3. Frontend Setup

Navigate to the frontend directory and install the necessary Node modules.

```bash
cd ../spotify-dashboard
# (If you are in the backend directory, otherwise navigate to the project root then to spotify-dashboard)
npm install
```

### 4. Running the Application

You need to run the backend and frontend servers in **separate terminal sessions**.

**Terminal 1: Start the Backend Server**

```bash
cd backend # (If not already in the backend directory)
source venv/bin/activate # (Activate virtual environment if not already active)
# For Windows: venv\Scripts\activate
flask run
```

**Terminal 2: Start the Frontend Development Server**

```bash
cd spotify-dashboard # (If not already in the frontend directory)
npm start
```

The frontend application should now be accessible in your web browser (usually at `http://localhost:3000`).

### 5. Usage

Start by authenticating your Spotify account. The button should redirect you to a Spotify log in page which will prompt you for the relevant information.
Once you have authenticated, you will see a navigation bar which includes tabs for "Playlist Analysis", "Custom Wrapped", and "Recently Played Songs".
"Playlist Analysis" is currently not implemented. "Custom Wrapped" will allow you to organize your recently played songs into categories of daily, weekly, monthly, and yearly, displaying songs played with their playcounts during those time periods.

## Contributing

Contributions are welcome! If you have suggestions for improvements or encounter any issues, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

