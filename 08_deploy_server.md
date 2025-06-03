# Deploy Express Server

Prepare and deploy the SmartRunning server to a free service like Render, Railway, or Fly.io.

### Steps:

1. Add a production start script to `package.json`
2. Ensure `.env.example` is present for environment config
3. Create a `Procfile` or appropriate config if needed
4. Document required environment variables
5. Deploy the server to a platform like:
   - [https://render.com](https://render.com)
   - [https://railway.app](https://railway.app)
   - [https://fly.io](https://fly.io)

### Output:

- Live API base URL
- Example API request for testing

Ensure that CORS is enabled for requests from your frontend.
