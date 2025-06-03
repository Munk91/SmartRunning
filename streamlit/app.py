import streamlit as st

# Page configuration
st.set_page_config(
    page_title="SmartRunning - Route Generator",
    page_icon="🏃",
    layout="wide"
)

import json
import os
import datetime

# Import API client
from api import (
    login, register, logout, get_profile, update_profile,
    generate_route as api_generate_route,
    save_activity, get_activities, get_activity, update_activity, delete_activity
)

# Check for required packages with graceful fallbacks
try:
    import folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False
    st.error("folium package not found. Please install with: pip install folium")

try:
    from streamlit_folium import folium_static
    STREAMLIT_FOLIUM_AVAILABLE = True
except ImportError:
    STREAMLIT_FOLIUM_AVAILABLE = False
    st.error("streamlit_folium package not found. Please install with: pip install streamlit-folium")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    st.error("requests package not found. Please install with: pip install requests")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    st.error("numpy package not found. Please install with: pip install numpy")

# Initialize session state for warning visibility
if 'show_requirements_warning' not in st.session_state:
    st.session_state.show_requirements_warning = True

requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
if os.path.exists(requirements_path) and st.session_state.show_requirements_warning:
    # Create columns within a warning-styled container
    st.warning("⚠️ To install all requirements at once, run: pip install -r requirements.txt")
    if st.button("✕ Dismiss", key="close_requirements_warning", type="secondary"):
        st.session_state.show_requirements_warning = False
        st.rerun()

# Import local routing module
try:
    from routing import generate_route, create_gpx, available_packages
    ROUTING_AVAILABLE = True
except ImportError:
    ROUTING_AVAILABLE = False
    st.error("routing.py module not found or has errors")

# Authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_data = None
    st.session_state.auth_token = None

# API URL configuration
if 'api_url' not in st.session_state:
    st.session_state.api_url = "http://localhost:3000/api"

# Initialize session state for current route
if 'current_route' not in st.session_state:
    st.session_state.current_route = None

# For storing activity history
if 'activity_history' not in st.session_state:
    st.session_state.activity_history = []

# Function to handle login with API
def handle_login(email, password):
    success, result = login(email, password)
    if success:
        # Successfully logged in
        st.success("Login successful!")
        return True
    else:
        # Login failed
        st.error(f"Login failed: {result}")
        return False

# Function to handle registration with API
def handle_register(name, email, password):
    success, result = register(name, email, password)
    if success:
        # Successfully registered
        st.success("Registration successful!")
        return True
    else:
        # Registration failed
        st.error(f"Registration failed: {result}")
        return False

# Function to handle logout
def handle_logout():
    logout()  # Call the API logout function
    st.success("Logged out successfully")
    st.rerun()

# UI Structure
def main():
    # Sidebar
    with st.sidebar:
        st.title("SmartRunning")
        
        if not st.session_state.authenticated:
            auth_option = st.radio("", ["Login", "Register"])
            
            if auth_option == "Login":
                with st.form("login_form"):
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    submit = st.form_submit_button("Login")
                    
                    if submit:
                        if handle_login(email, password):
                            # Login successful - handled by the function
                            st.rerun()
            else:
                with st.form("register_form"):
                    name = st.text_input("Name")
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    confirm_password = st.text_input("Confirm Password", type="password")
                    submit = st.form_submit_button("Register")
                    
                    if submit:
                        if password != confirm_password:
                            st.error("Passwords do not match")
                        elif handle_register(name, email, password):
                            # Registration successful - handled by the function
                            st.rerun()
        else:
            st.write(f"Welcome, {st.session_state.user_data['name']}!")
            
            # Navigation
            nav_selection = st.radio("Navigation", ["Route Generator", "Activity History", "Profile"])
            
            # Logout button
            # Show API connection status
            st.caption(f"Connected to API at {st.session_state.api_url}")
            
            if st.button("Logout"):
                handle_logout()
                st.rerun()

    # Main content
    if not st.session_state.authenticated:
        st.title("Welcome to SmartRunning")
        st.write("Please login or register to continue.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://images.unsplash.com/photo-1571008887538-b36bb32f4571?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80", 
                    caption="Plan your perfect run")
    else:
        if 'nav_selection' not in locals():
            nav_selection = "Route Generator"
            
        if nav_selection == "Route Generator":
            st.title("Generate Your Running Route")
            
            col1, col2 = st.columns(2)
            
            with col1:
                start_location = st.text_input("Starting Location", "Odense C, Denmark")
                distance = st.slider("Distance (km)", 1.0, 20.0, 5.0, 0.5)
                
                surface_options = ["Any", "Road", "Trail", "Mixed"]
                surface = st.selectbox("Surface Preference", surface_options)
                
                # Add API URL configuration in the sidebar
                with st.sidebar.expander("API Configuration"):
                    api_url = st.text_input("API URL", value=st.session_state.api_url)
                    if st.button("Update API URL"):
                        st.session_state.api_url = api_url
                        st.success("API URL updated")
                
                if st.button("Generate Route"):
                    with st.spinner("Generating your route..."):
                        try:
                            # Add debug info
                            st.write("Debug Info:")
                            debug_info = st.empty()
                            debug_info.info(f"Starting route generation from {start_location} for {distance} km on {surface} surface")
                            
                            # Try getting route from API first
                            if st.session_state.authenticated:
                                success, api_route_data = api_generate_route(start_location, distance, surface)
                                if success:
                                    route_data = api_route_data
                                    # Store the route in session state for later saving
                                    st.session_state.current_route = route_data
                                    debug_info.success("Route generated via API successfully!")
                                else:
                                    # If API fails, fall back to local generation
                                    debug_info.warning(f"API route generation failed: {api_route_data}. Falling back to local generation.")
                                    route_data = generate_route(start_location, distance, surface)
                            else:
                                # Not authenticated, use local generation
                                debug_info.info("Using local route generation (not logged in)")
                                route_data = generate_route(start_location, distance, surface)
                            
                            if route_data:
                                if "error" in route_data:
                                    st.warning("Route generated with limitations")
                                    st.error(route_data["error"])
                                    # More detailed debug information
                                    with st.expander("Debug Details"):
                                        st.write("Route generation encountered issues:")
                                        st.write(f"- Start location: {start_location}")
                                        st.write(f"- Distance requested: {distance} km")
                                        st.write(f"- Surface preference: {surface}")
                                        st.write(f"- Error: {route_data['error']}")
                                else:
                                    st.success("Route generated successfully!")
                                    debug_info.success("Route generation completed successfully")
                                
                                # Check if folium and numpy are available
                                if not FOLIUM_AVAILABLE or not NUMPY_AVAILABLE:
                                    st.error("Unable to create map: required packages missing")
                                    if not FOLIUM_AVAILABLE:
                                        st.info("Install folium: pip install folium")
                                    if not NUMPY_AVAILABLE:
                                        st.info("Install numpy: pip install numpy") 
                                    m = None
                                else:
                                    # We'll use a placeholder map until the routing is fully implemented
                                    m = folium.Map(location=[55.3960, 10.3883], zoom_start=13)
                                    folium.Marker([55.3960, 10.3883], tooltip="Start/End").add_to(m)
                                    
                                    # In a real implementation, we'd render the generated route
                                    # For now, draw a sample circular path
                                    # Generate circular route approximation
                                    center = [55.3960, 10.3883]
                                    radius = 0.01 * distance  # Rough approximation
                                    n_points = 20
                                    angles = np.linspace(0, 2*np.pi, n_points)
                                    coords = [(center[0] + radius * np.cos(angle), 
                                            center[1] + radius * np.sin(angle)) for angle in angles]
                                    
                                    # Add circular route to map
                                    folium.PolyLine(coords, color="blue", weight=3, opacity=0.7).add_to(m)
                                
                                # Display the map and stats
                                with col2:
                                    if m is not None and FOLIUM_AVAILABLE and STREAMLIT_FOLIUM_AVAILABLE:
                                        try:
                                            folium_static(m)
                                            st.success("Map embedded successfully!")
                                        except Exception as e:
                                            st.error(f"Error displaying map: {str(e)}")
                                            st.write("Map embedding issue. Try installing/updating your folium packages:")
                                            st.code("pip install -U folium streamlit-folium")
                                    elif m is None:
                                        st.error("Map cannot be displayed due to missing dependencies")
                                    else:
                                        st.warning("Map display requires folium and streamlit_folium packages")
                                        st.info("Install with: pip install folium streamlit-folium")
                                
                                st.subheader("Route Statistics")
                                stats_col1, stats_col2, stats_col3 = st.columns(3)
                                
                                # Use the actual calculated distance from route_data, if available
                                actual_distance = route_data.get("distance", distance)
                                stats_col1.metric("Distance", f"{actual_distance} km", 
                                                delta=f"{actual_distance - distance:.2f} km" if actual_distance != distance else None)
                                
                                # Use the estimated time from route_data, if available
                                estimated_time = route_data.get("estimated_time", round(distance * 6))
                                stats_col2.metric("Estimated Time", f"{estimated_time} min")  # Assume 6 min/km pace
                                
                                stats_col3.metric("Surface", surface)
                                
                                # Add elevation info if available
                                if "elevation_gain" in route_data:
                                    st.metric("Elevation Gain", f"{route_data['elevation_gain']} m")
                                
                                # Actions section
                                st.subheader("Actions")
                                col1, col2 = st.columns(2)
                                
                                # Save route button (only if authenticated)
                                if st.session_state.authenticated:
                                    with col1:
                                        if st.button("Save Route"):
                                            if st.session_state.current_route:
                                                with st.spinner("Saving route..."):
                                                    # Get a name for the route
                                                    route_name = f"Run on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
                                                    
                                                    # Save the route to the API
                                                    success, result = save_activity(st.session_state.current_route, route_name)
                                                    if success:
                                                        st.success(f"Route saved successfully as '{route_name}'!")
                                                    else:
                                                        st.error(f"Failed to save route: {result}")
                                            else:
                                                st.warning("No route to save. Generate a route first.")
                                else:
                                    with col1:
                                        st.warning("Log in to save routes")
                                
                                # Download option
                                with col2:
                                    try:
                                        if available_packages.get('gpxpy', False):
                                            # Generate GPX file
                                            gpx_data = create_gpx(route_data)
                                            
                                            # Log success for testing
                                            st.success("✅ GPX file generated successfully")
                                            
                                            # Sanitize filename from location
                                            safe_location = ''.join(c if c.isalnum() else '_' for c in start_location)
                                            
                                            st.download_button(
                                                label="Download GPX",
                                                data=gpx_data,
                                                file_name=f"{safe_location}_route.gpx",
                                                mime="application/gpx+xml",
                                                help="Download this route as a GPX file to use in your GPS device or other apps"
                                            )
                                            
                                            with st.expander("GPX File Details"):
                                                st.write("Your GPX file contains:")
                                                st.write(f"- {len(route_data['coordinates'])} waypoints")
                                                st.write(f"- Total distance: {route_data.get('distance', 0)} km")
                                                st.write(f"- Starting coordinates: {route_data.get('start_point', (0,0))}")
                                        else:
                                            st.warning("GPX export requires the 'gpxpy' package.")
                                            st.info("Install with: pip install gpxpy")
                                    except Exception as e:
                                        st.error(f"Error creating GPX file: {str(e)}")
                                        st.warning("Could not generate GPX file. Make sure gpxpy is installed.")
                        except Exception as e:
                            st.error(f"Error generating route: {str(e)}")
            
            with col2:
                if 'm' not in locals():
                    # Show placeholder map when no route is generated yet
                    if FOLIUM_AVAILABLE:
                        # Use coordinates from route_data if available
                        if st.session_state.current_route and 'coordinates' in st.session_state.current_route:
                            start_coords = st.session_state.current_route.get('coordinates', [[55.3960, 10.3883]])[0]
                            m = folium.Map(location=start_coords, zoom_start=13)
                        else:
                            m = folium.Map(location=[55.3960, 10.3883], zoom_start=13)
                    else:
                        m = None
                        st.error("Folium package not found. Map cannot be displayed.")
                        st.info("Install with: pip install folium")
                    if m is not None and FOLIUM_AVAILABLE and STREAMLIT_FOLIUM_AVAILABLE:
                        folium_static(m)
                    elif m is None:
                        st.error("Map cannot be displayed due to missing dependencies")
                    else:
                        st.warning("Map display requires folium and streamlit_folium packages")
                        st.info("Install with: pip install folium streamlit-folium")
                    
        elif nav_selection == "Activity History":
            st.title("Your Activity History")
            
            if not st.session_state.authenticated:
                st.warning("Please log in to view your activity history.")
            else:
                # Refresh button
                if st.button("Refresh Activities"):
                    with st.spinner("Loading activities..."):
                        success, activities = get_activities()
                        if success:
                            st.session_state.activity_history = activities
                            st.success(f"Loaded {len(activities)} activities")
                        else:
                            st.error(f"Failed to load activities: {activities}")
                
                # Display activities
                if not st.session_state.activity_history:
                    # First time load
                    with st.spinner("Loading activities..."):
                        success, activities = get_activities()
                        if success:
                            st.session_state.activity_history = activities
                        else:
                            st.error(f"Failed to load activities: {activities}")
                
                if st.session_state.activity_history:
                    # Display activities in a table
                    st.subheader(f"You have {len(st.session_state.activity_history)} saved activities")
                    
                    # Create tabs for different views
                    tab1, tab2 = st.tabs(["List View", "Map View"])
                    
                    with tab1:
                        # List view with details
                        for idx, activity in enumerate(st.session_state.activity_history):
                            with st.container():
                                col1, col2, col3 = st.columns([3, 1, 1])
                                
                                with col1:
                                    st.subheader(activity.get('name', f"Activity {idx+1}"))
                                    st.write(f"Date: {activity.get('createdAt', 'Unknown')}")
                                    st.write(f"Distance: {activity.get('distance', 0)} km")
                                    
                                with col2:
                                    duration_mins = activity.get('duration', 0) / 60  # Convert seconds to minutes
                                    st.metric("Duration", f"{duration_mins:.0f} min")
                                
                                with col3:
                                    # View button expands details
                                    if st.button("View Details", key=f"view_{idx}"):
                                        st.session_state.selected_activity = activity
                                
                                st.divider()
                    
                    with tab2:
                        # Map view of all activities
                        if FOLIUM_AVAILABLE:
                            try:
                                # Create a map centered on the first activity
                                first_activity = st.session_state.activity_history[0]
                                start_loc = first_activity.get('routeData', {}).get('coordinates', [[55.3960, 10.3883]])[0]
                                
                                m = folium.Map(location=start_loc, zoom_start=12)
                                
                                # Add routes to map with different colors
                                colors = ['blue', 'red', 'green', 'purple', 'orange', 'darkred', 'darkblue', 'darkgreen']
                                
                                for i, activity in enumerate(st.session_state.activity_history):
                                    if 'routeData' in activity and 'coordinates' in activity['routeData']:
                                        coords = activity['routeData']['coordinates']
                                        color = colors[i % len(colors)]
                                        folium.PolyLine(
                                            coords, 
                                            color=color, 
                                            weight=3, 
                                            opacity=0.7, 
                                            tooltip=activity.get('name', f"Activity {i+1}")
                                        ).add_to(m)
                                        
                                        # Add start marker
                                        folium.Marker(
                                            coords[0],
                                            tooltip=f"Start: {activity.get('name', f'Activity {i+1}')}" 
                                        ).add_to(m)
                                
                                # Display the map
                                folium_static(m)
                                
                            except Exception as e:
                                st.error(f"Error displaying activity maps: {str(e)}")
                        else:
                            st.error("Folium package is required to display maps")
                
                else:
                    st.info("No activities recorded yet. Generate and save some routes!")
                    
                # If a specific activity is selected, show details
                if 'selected_activity' in st.session_state and st.session_state.selected_activity:
                    with st.expander("Activity Details", expanded=True):
                        activity = st.session_state.selected_activity
                        
                        st.subheader(activity.get('name', "Activity Details"))
                        st.write(f"Date: {activity.get('createdAt')}")
                        st.write(f"Distance: {activity.get('distance')} km")
                        st.write(f"Duration: {activity.get('duration')/60:.1f} minutes")
                        st.write(f"Start Location: {activity.get('startLocation', 'Unknown')}")
                        
                        # Map of single activity
                        if FOLIUM_AVAILABLE and 'routeData' in activity and 'coordinates' in activity['routeData']:
                            coords = activity['routeData']['coordinates']
                            activity_map = folium.Map(location=coords[0], zoom_start=14)
                            folium.PolyLine(coords, color='blue', weight=3, opacity=0.7).add_to(activity_map)
                            folium.Marker(coords[0], tooltip="Start").add_to(activity_map)
                            folium_static(activity_map)
                        
                        # Actions for this activity
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Download GPX"):
                                if 'routeData' in activity and available_packages.get('gpxpy', False):
                                    gpx_data = create_gpx(activity['routeData'])
                                    st.download_button(
                                        label="Download GPX File",
                                        data=gpx_data,
                                        file_name=f"{activity.get('name', 'activity').replace(' ', '_')}.gpx",
                                        mime="application/gpx+xml"
                                    )
                                else:
                                    st.error("GPX creation failed. Missing route data or gpxpy package.")
                        
                        with col2:
                            if st.button("Close Details"):
                                st.session_state.selected_activity = None
            
        elif nav_selection == "Profile":
            st.title("Your Profile")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image("https://www.w3schools.com/howto/img_avatar.png", width=150)
            
            with col2:
                st.subheader(st.session_state.user_data['name'])
                st.write(f"Email: {st.session_state.user_data['email']}")
            
            with st.expander("Edit Profile"):
                with st.form("profile_form"):
                    name = st.text_input("Name", st.session_state.user_data['name'])
                    email = st.text_input("Email", st.session_state.user_data['email'])
                    current_password = st.text_input("Current Password", type="password")
                    new_password = st.text_input("New Password (leave blank to keep current)", type="password")
                    submit = st.form_submit_button("Update Profile")
                    
                    if submit:
                        # This would be replaced with an actual API call to your Express backend
                        st.success("Profile updated successfully!")

if __name__ == "__main__":
    main()