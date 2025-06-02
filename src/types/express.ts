import { Request as ExpressRequest } from 'express';

// Extend the Request interface from express
export interface Request extends ExpressRequest {
  user?: {
    userId: string;
    email: string;
  };
}