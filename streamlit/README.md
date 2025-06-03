# SmartRunning - Streamlit Frontend

This is the Streamlit frontend component of the SmartRunning application, providing route generation and data visualization capabilities.

## Deployment to Streamlit Cloud

Follow these steps to deploy the SmartRunning app to Streamlit Cloud:

### 1. Create a GitHub Repository

1. Create a new GitHub repository
2. Push your project code to this repository
   ```
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/smartrunning.git
   git push -u origin main
   ```

### 2. Sign up for Streamlit Cloud

1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account

### 3. Deploy the App

1. From the Streamlit Cloud dashboard, click "New app"
2. Select your GitHub repository
3. Choose the branch (main)
4. Set the Main file path to `streamlit/app.py`
5. Configure app resources if needed (usually the defaults are fine)
6. Click "Deploy"

### 4. Configuration Settings

The app includes a `.streamlit/config.toml` file with custom theming. This will be automatically applied when deployed.

### 5. Updating the App

When you want to update your app:
1. Push changes to your GitHub repository
2. Streamlit Cloud will automatically redeploy your app

### 6. Troubleshooting

If you encounter issues with dependencies:
- Check the app logs in the Streamlit Cloud dashboard
- Ensure all required packages are listed in `requirements.txt`
- Verify that your app works locally using the same Python version as Streamlit Cloud

## Features

- **Route Generator**: Create custom running routes based on desired distance and surface preference
- **Map Visualization**: Interactive maps showing generated routes
- **User Authentication**: Login and registration forms connected to Express backend
- **Activity History**: Track and visualize past running activities
- **Profile Management**: User profile settings and preferences
- **GPX Export**: Download routes as GPX files compatible with GPS devices and fitness apps

## Backend Integration

This Streamlit frontend connects to the SmartRunning Express.js backend through RESTful APIs. The following endpoints are used:

- Authentication endpoints:
  - `POST /api/auth/login`: User login
  - `POST /api/auth/register`: User registration
  - `GET /api/auth/profile`: Get user profile

- Activity endpoints:
  - `POST /api/activity/generate`: Generate a running route
  - `POST /api/activity`: Save an activity
  - `GET /api/activity`: Retrieve all activities
  - `GET /api/activity/:id`: Get a specific activity
  - `PUT /api/activity/:id`: Update an activity
  - `DELETE /api/activity/:id`: Delete an activity

## Setup Instructions

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Project Structure

- `app.py`: Main Streamlit application
- `routing.py`: Route generation logic using OSMnx and NetworkX
- `api.py`: API client for communicating with the backend
- `requirements.txt`: Python dependencies
- `.streamlit/config.toml`: Streamlit configuration and theming

## Technologies

- **Streamlit**: UI framework
- **OSMnx & NetworkX**: Route generation based on OpenStreetMap data
- **Folium**: Interactive map visualization
- **GPX**: Route export functionality
- **Requests**: API communication with backend