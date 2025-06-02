import random
import sys
import os

# Dict to track which packages are available
available_packages = {}

# Function to check if a package is available
def check_package(package_name):
    try:
        __import__(package_name)
        available_packages[package_name] = True
        return True
    except ImportError:
        available_packages[package_name] = False
        print(f"Warning: {package_name} not available. Some features may be limited.")
        return False

# Check for required packages
check_package('osmnx')
check_package('networkx')
check_package('numpy')
check_package('geopy')
check_package('geopandas')
check_package('folium')
check_package('gpxpy')

# Only import if available
if available_packages['numpy']:
    import numpy as np
if available_packages['geopy']:
    try:
        from geopy.geocoders import Nominatim
        # Initialize geocoder
        geolocator = Nominatim(user_agent="smartrunning_app")
    except Exception as e:
        print(f"Error initializing Nominatim: {e}")
        geolocator = None
if available_packages['osmnx']:
    import osmnx as ox
if available_packages['networkx']:
    import networkx as nx
if available_packages['geopandas']:
    import geopandas as gpd
if available_packages['folium']:
    import folium
if available_packages['gpxpy']:
    import gpxpy
    import gpxpy.gpx

def generate_route(start_location, distance, surface_preference="Any"):
    """
    Generate a running route based on the given parameters
    
    Args:
        start_location (str): Address or location name
        distance (float): Desired distance in kilometers
        surface_preference (str): Preferred surface type (Any, Road, Trail, Mixed)
        
    Returns:
        dict: Route data including coordinates, distance, and metadata
        
    Raises:
        ValueError: If required packages are missing or location cannot be geocoded
    """
    missing_packages = []
    # Check if required packages are available
    for package in ['numpy', 'geopy']:
        if not available_packages.get(package, False):
            missing_packages.append(package)
    
    if missing_packages:
        error_msg = f"Cannot generate route: Missing required packages: {', '.join(missing_packages)}"
        print(error_msg)
        raise ValueError(error_msg)

    try:
        # Get coordinates from location name
        if 'geopy' not in available_packages or geolocator is None:
            # If geocoding not available, use default coordinates (Odense C, Denmark)
            print("Geocoding not available, using default coordinates")
            start_point = (55.3960, 10.3883)  # Odense C, Denmark coordinates
            return {
                "coordinates": [(55.3960, 10.3883)],
                "start_point": (55.3960, 10.3883),
                "distance": distance,
                "surface_type": surface_preference,
                "elevation_gain": 0,
                "estimated_time": round(distance * 6),
                "error": "Geocoding service not available. Using default location (Odense C, Denmark)."
            }
        else:
            try:
                location = geolocator.geocode(start_location)
                if not location:
                    error_msg = f"Could not find location: {start_location}. Please enter a valid location."
                    print(error_msg)
                    return {
                        "coordinates": [(55.3960, 10.3883)],
                        "start_point": (55.3960, 10.3883),
                        "distance": distance,
                        "surface_type": surface_preference,
                        "elevation_gain": 0,
                        "estimated_time": round(distance * 6),
                        "error": error_msg
                    }
                else:
                    start_point = (location.latitude, location.longitude)
            except:
                error_msg = f"Error geocoding location: {start_location}. Please check the input."
                print(error_msg)
                return {
                    "coordinates": [(55.3960, 10.3883)],
                    "start_point": (55.3960, 10.3883),
                    "distance": distance,
                    "surface_type": surface_preference,
                    "elevation_gain": 0,
                    "estimated_time": round(distance * 6),
                    "error": error_msg
                }
        
        print(f"Generating route from {start_point} for {distance} km on {surface_preference}")
        
        # In a full implementation, we would:
        # 1. Download the street network using OSMnx
        # 2. Apply filters based on surface preference
        # 3. Use NetworkX to generate routes of specified distance
        # 4. Return the optimal route
        
        # Check if OSMnx is available to generate a real route
        if not available_packages.get('osmnx', False) or not available_packages.get('networkx', False):
            return {
                "coordinates": [(start_point[0], start_point[1])],
                "start_point": start_point,
                "distance": distance,
                "surface_type": surface_preference,
                "elevation_gain": 0,
                "estimated_time": round(distance * 6),
                "error": "Required routing libraries (osmnx, networkx) not available. Using a simplified route."
            }
        
        # For this placeholder, we'll return a simple dictionary with mock data
        
        # Get surface filter for this preference
        surface_filter, handle_missing_surface = get_surface_filter(surface_preference)
        
        # In a real implementation, we'd use these filters with OSMnx:
        # G = ox.graph_from_point(start_point, dist=distance*1000/2, filters=surface_filter)
        # Then process the graph to handle edges with missing surface tags using handle_missing_surface function
        
        # Generate a simple circular route as a placeholder
        # In a real implementation, this would be replaced with actual routing logic
        if available_packages.get('numpy', False):
            # Use numpy for calculation if available
            # Make distance calculation more precise by adjusting the radius
            # A proper circle with circumference = distance
            radius_km = distance / (2 * np.pi)  # Exact calculation for a circular route
            num_points = int(distance * 10)  # 10 points per km for smooth route
            
            route_coords = []
            for i in range(num_points):
                angle = 2 * np.pi * i / num_points
                # Convert km to latitude/longitude degrees (approximate)
                lat_offset = radius_km * np.cos(angle) / 111.32
                lng_offset = radius_km * np.sin(angle) / (111.32 * np.cos(start_point[0] * np.pi / 180))
                
                lat = start_point[0] + lat_offset
                lng = start_point[1] + lng_offset
                route_coords.append((lat, lng))
            
            # Add the start point to close the loop
            route_coords.append(route_coords[0])
        else:
            # Fallback to a simpler calculation if numpy is not available
            import math
            radius_km = distance / (2 * math.pi)
            num_points = int(distance * 10)
            
            route_coords = []
            for i in range(num_points):
                angle = 2 * math.pi * i / num_points
                # Convert km to latitude/longitude degrees (approximate)
                lat_offset = radius_km * math.cos(angle) / 111.32
                lng_offset = radius_km * math.sin(angle) / (111.32 * math.cos(start_point[0] * math.pi / 180))
                
                lat = start_point[0] + lat_offset
                lng = start_point[1] + lng_offset
                route_coords.append((lat, lng))
            
            # Add the start point to close the loop
            route_coords.append(route_coords[0])
        
        # Calculate actual distance from the generated coordinates
        # This is a more accurate measure of the actual route distance
        if available_packages.get('numpy', False):
            # Calculate actual distance using great-circle distance formula
            def haversine(coord1, coord2):
                # Calculate the great circle distance between two points 
                # on the earth specified in decimal degrees
                lat1, lon1 = coord1
                lat2, lon2 = coord2
                # Convert decimal degrees to radians
                lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
                # Haversine formula
                dlon = lon2 - lon1
                dlat = lat2 - lat1
                a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
                c = 2 * np.arcsin(np.sqrt(a))
                km = 6371 * c  # Radius of earth in kilometers
                return km
                
            # Calculate total distance along route
            total_distance = 0.0
            for i in range(len(route_coords)-1):
                total_distance += haversine(route_coords[i], route_coords[i+1])
            actual_distance = round(total_distance, 2)
            
            # Print debug info about distance
            print(f"Requested distance: {distance} km, Actual route distance: {actual_distance} km")
        else:
            # Fallback if numpy isn't available
            actual_distance = distance
        
        # Prepare response
        route_data = {
            "coordinates": route_coords,
            "start_point": start_point,
            "distance": actual_distance,
            "surface_type": surface_preference,
            "elevation_gain": round(random.uniform(distance * 5, distance * 20)),  # Mock elevation data
            "estimated_time": round(distance * 6)  # Assumes 6 min/km pace
        }
        
        return route_data
    
    except Exception as e:
        error_msg = f"Error generating route: {str(e)}"
        print(error_msg)
        # Return a minimal route data object to prevent app crashes
        return {
            "coordinates": [(55.3960, 10.3883), (55.3961, 10.3884), (55.3960, 10.3883)],  # Minimal triangle
            "start_point": (55.3960, 10.3883),
            "distance": distance,
            "surface_type": surface_preference,
            "elevation_gain": 0,
            "estimated_time": round(distance * 6),
            "error": error_msg
        }

def create_gpx(route_data):
    """
    Create a GPX file from route data
    
    Args:
        route_data (dict): Route information including coordinates
        
    Returns:
        str: GPX file content as string
    """
    if not available_packages.get('gpxpy', False):
        raise ImportError("gpxpy package is required for GPX export")
        
    gpx = gpxpy.gpx.GPX()
    
    # Create track with name and description
    track = gpxpy.gpx.GPXTrack()
    track.name = "SmartRunning Route"
    track.type = "Running"
    track.description = f"{route_data.get('distance', 0)} km {route_data.get('surface_type', 'Run')}" 
    gpx.tracks.append(track)
    
    # Create segment
    segment = gpxpy.gpx.GPXTrackSegment()
    track.segments.append(segment)
    
    # Add waypoint for start/end
    if 'start_point' in route_data:
        start = gpxpy.gpx.GPXWaypoint(
            latitude=route_data['start_point'][0], 
            longitude=route_data['start_point'][1],
            name="Start/End"
        )
        gpx.waypoints.append(start)
    
    # Add points
    for point in route_data["coordinates"]:
        # Add elevation if available (mock for now)
        track_point = gpxpy.gpx.GPXTrackPoint(point[0], point[1])
        segment.points.append(track_point)
    
    # Add metadata
    gpx.creator = "SmartRunning App"
    
    # Generate the XML content
    gpx_xml = gpx.to_xml()
    
    # Validate by reading back the GPX file and print details to server log
    validate_gpx(gpx_xml, route_data)
    
    return gpx_xml


def validate_gpx(gpx_xml, original_data):
    """
    Validates GPX content by reading it back and comparing with original data
    
    Args:
        gpx_xml (str): The GPX XML content
        original_data (dict): The original route data used to create the GPX
    """
    try:
        # Skip validation if gpxpy isn't available
        if not available_packages.get('gpxpy', False):
            print("GPX validation skipped: gpxpy package not available")
            return
            
        # Parse the XML back to a GPX object
        parsed_gpx = gpxpy.parse(gpx_xml)
        
        # Print validation info to server log
        print("\n===== GPX VALIDATION =====")
        print(f"GPX Creator: {parsed_gpx.creator}")
        print(f"Number of tracks: {len(parsed_gpx.tracks)}")
        
        if parsed_gpx.tracks:
            track = parsed_gpx.tracks[0]
            print(f"Track name: {track.name}")
            print(f"Track type: {track.type}")
            print(f"Track description: {track.description}")
            
            total_points = sum(len(segment.points) for segment in track.segments)
            print(f"Total points in track: {total_points}")
            
            # Validate number of points
            expected_points = len(original_data.get('coordinates', []))
            if total_points == expected_points:
                print(f"✅ Point count matches original data: {total_points}")
            else:
                print(f"❌ Point count mismatch! GPX: {total_points}, Original: {expected_points}")
        
        # Check waypoints
        print(f"Number of waypoints: {len(parsed_gpx.waypoints)}")
        if parsed_gpx.waypoints:
            for i, waypoint in enumerate(parsed_gpx.waypoints):
                print(f"Waypoint {i+1}: {waypoint.name} at {waypoint.latitude}, {waypoint.longitude}")
        
        # Calculate length
        length_2d = parsed_gpx.length_2d() / 1000  # Convert to km
        expected_length = original_data.get('distance', 0)
        print(f"Route length: {length_2d:.2f} km (expected: {expected_length:.2f} km)")
        
        print("===== END GPX VALIDATION =====\n")
        
    except Exception as e:
        print(f"Error validating GPX: {str(e)}")
        print("First 100 chars of GPX XML:")
        print(gpx_xml[:100] + "..." if len(gpx_xml) > 100 else gpx_xml)

def get_surface_filter(surface_preference):
    """
    Return OSM filters based on surface preference
    
    Args:
        surface_preference (str): User's surface preference
        
    Returns:
        dict: OSM filter for network retrieval and a function to handle missing surface tags
    """
    # Define surface-specific filter
    if surface_preference == "Road":
        highway_filter = {'highway': ['primary', 'secondary', 'tertiary', 'residential', 'service']}
        # Function to handle missing surface tags - assume paved for roads
        def handle_missing_surface(edge_data):
            if 'surface' not in edge_data:
                edge_data['surface'] = 'paved'
            return edge_data
    elif surface_preference == "Trail":
        highway_filter = {'highway': ['path', 'footway', 'track']}
        # Function to handle missing surface tags - assume unpaved for trails
        def handle_missing_surface(edge_data):
            if 'surface' not in edge_data:
                edge_data['surface'] = 'unpaved'
            return edge_data
    elif surface_preference == "Mixed":
        highway_filter = {'highway': ['primary', 'secondary', 'tertiary', 'residential', 
                          'service', 'path', 'footway', 'track']}
        # Function to handle missing surface tags - make best guess based on highway type
        def handle_missing_surface(edge_data):
            if 'surface' not in edge_data:
                if edge_data.get('highway') in ['primary', 'secondary', 'tertiary', 'residential', 'service']:
                    edge_data['surface'] = 'paved'
                elif edge_data.get('highway') in ['path', 'footway', 'track']:
                    edge_data['surface'] = 'unpaved'
                else:
                    edge_data['surface'] = 'unknown'
            return edge_data
    else:  # "Any"
        highway_filter = {'highway': ['primary', 'secondary', 'tertiary', 'residential', 
                          'service', 'path', 'footway', 'track']}
        # Function to handle missing surface tags - accept all surfaces
        def handle_missing_surface(edge_data):
            if 'surface' not in edge_data:
                edge_data['surface'] = 'unknown'
            return edge_data
    
    return highway_filter, handle_missing_surface