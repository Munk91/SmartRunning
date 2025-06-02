import request from 'supertest';
import mongoose from 'mongoose';
import app from '../app';
import User from '../models/user.model';
import { generateToken } from '../utils/token';

// Mock user data
const testUser = {
  name: 'Test User',
  email: 'test@example.com',
  password: 'password123',
};

// Before all tests
beforeAll(async () => {
  // Connect to a test database
  const mongoURI = process.env.MONGODB_URI || 'mongodb://localhost:27017/smartrunning_test';
  await mongoose.connect(mongoURI);
  
  // Clear the user collection before tests
  await User.deleteMany({});
});

// After all tests
afterAll(async () => {
  // Close the database connection
  await mongoose.connection.close();
});

describe('Authentication Routes', () => {
  // Clear users after each test
  afterEach(async () => {
    await User.deleteMany({});
  });

  describe('POST /api/auth/register', () => {
    it('should register a new user and return a token', async () => {
      const response = await request(app)
        .post('/api/auth/register')
        .send(testUser)
        .expect(201);

      // Check response structure
      expect(response.body).toHaveProperty('token');
      expect(response.body).toHaveProperty('user');
      expect(response.body.user).toHaveProperty('id');
      expect(response.body.user).toHaveProperty('name', testUser.name);
      expect(response.body.user).toHaveProperty('email', testUser.email);

      // Check user was created in the database
      const userCount = await User.countDocuments();
      expect(userCount).toBe(1);
    });

    it('should return 400 if user with email already exists', async () => {
      // Create a user first
      await User.create(testUser);

      // Try to create the same user again
      const response = await request(app)
        .post('/api/auth/register')
        .send(testUser)
        .expect(400);

      expect(response.body).toHaveProperty('message', 'User with this email already exists');
    });

    it('should return 400 if required fields are missing', async () => {
      const response = await request(app)
        .post('/api/auth/register')
        .send({ name: 'Test User' }) // Missing email and password
        .expect(400);

      expect(response.body).toHaveProperty('message', 'Please provide all required fields');
    });
  });

  describe('POST /api/auth/login', () => {
    beforeEach(async () => {
      // Create a test user before each login test
      const user = new User(testUser);
      await user.save();
    });

    it('should login user and return a token', async () => {
      const response = await request(app)
        .post('/api/auth/login')
        .send({
          email: testUser.email,
          password: testUser.password,
        })
        .expect(200);

      expect(response.body).toHaveProperty('token');
      expect(response.body).toHaveProperty('user');
      expect(response.body.user).toHaveProperty('email', testUser.email);
    });

    it('should return 404 if user is not found', async () => {
      const response = await request(app)
        .post('/api/auth/login')
        .send({
          email: 'nonexistent@example.com',
          password: 'password123',
        })
        .expect(404);

      expect(response.body).toHaveProperty('message', 'User not found');
    });

    it('should return 401 if password is incorrect', async () => {
      const response = await request(app)
        .post('/api/auth/login')
        .send({
          email: testUser.email,
          password: 'wrongpassword',
        })
        .expect(401);

      expect(response.body).toHaveProperty('message', 'Invalid credentials');
    });
  });

  describe('GET /api/auth/profile', () => {
    let token: string;
    let userId: string;

    beforeEach(async () => {
      // Create a user and get their token
      const user = new User(testUser);
      await user.save();
      userId = user._id?.toString() || '';
      token = generateToken(user);
    });

    it('should return user profile when authenticated', async () => {
      const response = await request(app)
        .get('/api/auth/profile')
        .set('Authorization', `Bearer ${token}`)
        .expect(200);

      expect(response.body).toHaveProperty('user');
      expect(response.body.user).toHaveProperty('id', userId);
      expect(response.body.user).toHaveProperty('email', testUser.email);
    });

    it('should return 401 if no token is provided', async () => {
      const response = await request(app)
        .get('/api/auth/profile')
        .expect(401);

      expect(response.body).toHaveProperty('message', 'Authentication required');
    });

    it('should return 401 if token is invalid', async () => {
      const response = await request(app)
        .get('/api/auth/profile')
        .set('Authorization', 'Bearer invalidtoken')
        .expect(401);

      expect(response.body).toHaveProperty('message', 'Invalid or expired token');
    });
  });
});