import express, { Express } from 'express';
import mongoose from 'mongoose';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

// Import routes
import authRoutes from './routes/auth.routes';
// import activityRoutes from './routes/activity.routes';

// Initialize the express app
const app: Express = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Base route
app.get('/', (req, res) => {
  res.send('SmartRunning API is running!');
});

// Use routes
app.use('/api/auth', authRoutes);
// app.use('/api/activity', activityRoutes);

export default app;
