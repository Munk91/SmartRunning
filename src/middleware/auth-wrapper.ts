import { Response, NextFunction } from 'express';
import { Request } from '../types/express';
import { authMiddleware } from './auth.middleware';

/**
 * A wrapper around the auth middleware that complies with Express routing middleware signature
 */
export const authMiddlewareWrapper = (req: Request, res: Response, next: NextFunction): void => {
  authMiddleware(req, res, next);
};