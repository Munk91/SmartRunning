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
- **User Authentication**: Login and registration forms (connects to Express backend)
- **Activity History**: Track and visualize past running activities
- **Profile Management**: User profile settings and preferences

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
- `requirements.txt`: Python dependencies

## Backend Integration

This Streamlit frontend is designed to work with the Express.js backend. To enable full functionality:

1. Ensure the Express backend is running (default: http://localhost:3000)
2. Update the API endpoint URLs in the app.py file if needed

## Technologies

- **Streamlit**: UI framework
- **OSMnx & NetworkX**: Route generation based on OpenStreetMap data
- **Folium**: Interactive map visualization
- **GPX**: Route export functionality