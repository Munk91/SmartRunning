import requests
import json
import streamlit as st

# Default API URL, can be overridden in session state
DEFAULT_API_URL = "http://localhost:3000/api"

def get_api_url():
    if "api_url" not in st.session_state:
        st.session_state.api_url = DEFAULT_API_URL
    return st.session_state.api_url

def set_api_url(url):
    st.session_state.api_url = url

def get_headers():
    """Get headers with authentication token if available"""
    headers = {"Content-Type": "application/json"}
    if "auth_token" in st.session_state and st.session_state.auth_token:
        headers["Authorization"] = f"Bearer {st.session_state.auth_token}"
    return headers

def handle_response(response):
    """Handle API response and error cases"""
    try:
        response.raise_for_status()  # Raise exception for 4xx/5xx responses
        return response.json()
    except requests.exceptions.HTTPError as e:
        # Try to get error details from response
        try:
            error_detail = response.json()
            error_message = error_detail.get("message", str(e))
        except:
            error_message = str(e)
        raise Exception(f"API Error: {error_message}")
    except ValueError:  # JSON decoding failed
        if response.status_code == 204:  # No content
            return {}
        raise Exception("Invalid response format from API")
    except Exception as e:
        raise Exception(f"API request failed: {str(e)}")

# Authentication APIs

def login(email, password):
    """Login user and get authentication token"""
    try:
        url = f"{get_api_url()}/auth/login"
        payload = {"email": email, "password": password}
        response = requests.post(url, json=payload)
        data = handle_response(response)
        
        # Store authentication data in session state
        if "token" in data:
            st.session_state.auth_token = data["token"]
            st.session_state.authenticated = True
            st.session_state.user_data = data.get("user", {})
            return True, data.get("user", {})
        return False, "Authentication failed: No token received"
    except Exception as e:
        return False, str(e)

def register(name, email, password):
    """Register new user"""
    try:
        url = f"{get_api_url()}/auth/register"
        payload = {"name": name, "email": email, "password": password}
        response = requests.post(url, json=payload)
        data = handle_response(response)
        
        # Store authentication data in session state
        if "token" in data:
            st.session_state.auth_token = data["token"]
            st.session_state.authenticated = True
            st.session_state.user_data = data.get("user", {})
            return True, data.get("user", {})
        return False, "Registration failed: No token received"
    except Exception as e:
        return False, str(e)

def logout():
    """Clear authentication data"""
    if "auth_token" in st.session_state:
        del st.session_state.auth_token
    st.session_state.authenticated = False
    st.session_state.user_data = None

def get_profile():
    """Get current user profile"""
    try:
        url = f"{get_api_url()}/auth/profile"
        headers = get_headers()
        response = requests.get(url, headers=headers)
        data = handle_response(response)
        return True, data
    except Exception as e:
        return False, str(e)

def update_profile(user_data):
    """Update user profile"""
    try:
        url = f"{get_api_url()}/auth/profile"
        headers = get_headers()
        response = requests.put(url, json=user_data, headers=headers)
        data = handle_response(response)
        
        # Update session state with new user data
        if "user" in data:
            st.session_state.user_data = data["user"]
        return True, data
    except Exception as e:
        return False, str(e)

# Activity APIs

def generate_route(start_location, distance, surface_preference):
    """Generate a running route via the API"""
    try:
        url = f"{get_api_url()}/activity/generate"
        headers = get_headers()
        payload = {
            "startLocation": start_location,
            "distance": float(distance),
            "surfacePreference": surface_preference
        }
        response = requests.post(url, json=payload, headers=headers)
        data = handle_response(response)
        return True, data
    except Exception as e:
        return False, str(e)

def save_activity(route_data, name=None):
    """Save generated route as an activity"""
    try:
        url = f"{get_api_url()}/activity"
        headers = get_headers()
        
        # Prepare activity data
        payload = {
            "name": name or f"Route from {route_data.get('startLocation', 'Unknown')}",
            "distance": route_data.get("distance", 0),
            "duration": route_data.get("estimatedTime", 0) * 60,  # Convert to seconds
            "startLocation": route_data.get("startLocation", ""),
            "routeData": route_data,
            "activityType": "running"
        }
        response = requests.post(url, json=payload, headers=headers)
        data = handle_response(response)
        return True, data
    except Exception as e:
        return False, str(e)

def get_activities():
    """Get all activities for the current user"""
    try:
        url = f"{get_api_url()}/activity"
        headers = get_headers()
        response = requests.get(url, headers=headers)
        data = handle_response(response)
        return True, data
    except Exception as e:
        return False, str(e)

def get_activity(activity_id):
    """Get a specific activity by ID"""
    try:
        url = f"{get_api_url()}/activity/{activity_id}"
        headers = get_headers()
        response = requests.get(url, headers=headers)
        data = handle_response(response)
        return True, data
    except Exception as e:
        return False, str(e)

def update_activity(activity_id, activity_data):
    """Update a specific activity"""
    try:
        url = f"{get_api_url()}/activity/{activity_id}"
        headers = get_headers()
        response = requests.put(url, json=activity_data, headers=headers)
        data = handle_response(response)
        return True, data
    except Exception as e:
        return False, str(e)

def delete_activity(activity_id):
    """Delete a specific activity"""
    try:
        url = f"{get_api_url()}/activity/{activity_id}"
        headers = get_headers()
        response = requests.delete(url, headers=headers)
        data = handle_response(response)
        return True, data
    except Exception as e:
        return False, str(e)