# Connect Frontend to Server APIs

Update the frontend app to use the SmartRunning backend APIs.

### Goals:

- On form submission (location + distance + surface), call a backend endpoint like `POST /api/activity/generate` to create/generate a running route.
- Display the resulting route on the map using the response from the backend.
- Add functionality to:
  - Save the generated route
  - Fetch and list past activities from `GET /api/activity`
  - View or edit individual activities
  - Integrate authentication:
    - Use `POST /api/auth/login` and `POST /api/auth/register` for user authentication
    - Store JWT in local storage or cookies
    - Use the token for authenticated requests to activity routes

Use `fetch` or `axios` for requests.

Make sure errors from the API are handled and displayed to the user.
