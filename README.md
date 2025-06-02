# SmartRunning

A comprehensive application for tracking running activities, generating custom running routes, managing goals, and analyzing performance statistics.

## Features

- User authentication system
- Running activity tracking (distance, duration, pace, etc.)
- Custom running route generation based on desired distance and preferences
- Interactive map visualization
- Activity statistics and analytics
- Goals setting and tracking
- Social sharing features

## Tech Stack

### Backend (Node.js/Express)
- **Backend**: Node.js, Express, TypeScript
- **Database**: MongoDB with Mongoose
- **Authentication**: JWT
- **Testing**: Jest

### Frontend (Streamlit)
- **UI Framework**: Streamlit
- **Route Generation**: OSMnx, NetworkX
- **Map Visualization**: Folium
- **Data Processing**: Pandas, NumPy, GeoPandas

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- MongoDB (local or Atlas)
- Python (3.8 or higher)

### Backend Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/SmartRunning.git
   cd SmartRunning
   ```

2. Install backend dependencies
   ```bash
   npm install
   ```

3. Create a `.env` file in the root directory with the following variables
   ```
   PORT=3000
   MONGODB_URI=mongodb://localhost:27017/smartrunning
   JWT_SECRET=your_jwt_secret_here
   NODE_ENV=development
   ```

4. Start the development server
   ```bash
   npm run dev
   ```

### Frontend Installation

1. Navigate to the Streamlit directory
   ```bash
   cd streamlit
   ```

2. Install Python dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application
   ```bash
   streamlit run app.py
   ```

## Available Scripts

### Backend
- `npm start` - Start the production server
- `npm run dev` - Start the development server with hot-reloading
- `npm run build` - Build the TypeScript code
- `npm run lint` - Lint the code using ESLint
- `npm run format` - Format the code using Prettier
- `npm test` - Run the tests

## Project Structure

```
├── src/                # Node.js/Express backend
│   ├── config/         # Configuration files
│   ├── controllers/    # Route controllers
│   ├── middleware/     # Express middleware
│   ├── models/         # Mongoose models
│   ├── routes/         # Express routes
│   ├── services/       # Business logic
│   ├── types/          # TypeScript type definitions
│   ├── utils/          # Utility functions
│   ├── app.ts          # Express app
│   ├── server.ts       # Server entry point
│   └── __tests__/      # Test files
├── streamlit/          # Python/Streamlit frontend
│   ├── app.py          # Main Streamlit application
│   ├── routing.py      # Route generation logic
│   └── requirements.txt # Python dependencies
├── dist/               # Compiled JavaScript
├── .env                # Environment variables
├── .env.example        # Example environment variables
└── package.json        # Project dependencies
```

## License

This project is licensed under the ISC License.

## Acknowledgments

- Thanks to all contributors