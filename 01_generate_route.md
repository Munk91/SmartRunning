# User Authentication Routes Implementation

## Tasks
1. Create auth controller with register, login, and get profile functions
2. Implement JWT token generation utility
3. Complete auth routes implementation
4. Write tests for auth routes
5. Update necessary middleware

## Implementation Details
### Register Function
- Validate input
- Check if user already exists
- Create new user
- Generate JWT token
- Return user and token

### Login Function
- Validate input
- Find user by email
- Compare passwords
- Generate JWT token
- Return user and token

### Get Profile Function
- Return user information from request object