import request from 'supertest';
import app from '../app';

describe('App', () => {
  it('should respond to the home route', async () => {
    const response = await request(app).get('/');
    expect(response.status).toBe(200);
    expect(response.text).toContain('SmartRunning API is running!');
  });
});