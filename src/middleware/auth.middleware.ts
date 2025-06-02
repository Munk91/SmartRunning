import { Response, NextFunction } from 'express';
import { Request } from '../types/express';
import jwt from 'jsonwebtoken';
import { verifyToken } from '../utils/token';
// Auth is now extended in Express namespace via express.d.ts

// Request type is extended in request-response.ts

export const authMiddleware = (req: Request, res: Response, next: NextFunction) => {
  // req.user is now available directly
  try {
    // Get token from header
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ message: 'Authentication required' });
    }
    
    const token = authHeader.split(' ')[1];
    
    // Verify token
    const decoded = verifyToken(token);
    
    if (!decoded) {
      return res.status(401).json({ message: 'Invalid or expired token' });
    }
    
    // Add user from payload
    req.user = decoded;
    
    next();
  } catch (error) {
    return res.status(401).json({ message: 'Invalid or expired token' });
  }
};