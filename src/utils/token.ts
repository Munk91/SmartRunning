import jwt from 'jsonwebtoken';
import { IUser } from '../types/user';

/**
 * Generate a JWT token for the user
 * @param user User object
 * @returns JWT token
 */
export const generateToken = (user: IUser): string => {
  const payload = {
    userId: user._id,
    email: user.email,
  };

  const secret = process.env.JWT_SECRET || 'default_secret_replace_in_production';
  const options = {
    expiresIn: '7d' as const, // Token expires in 7 days
  };

  return jwt.sign(payload, secret, options);
};

/**
 * Verify a JWT token
 * @param token JWT token
 * @returns Decoded token payload or null if invalid
 */
export const verifyToken = (token: string): any => {
  try {
    const secret = process.env.JWT_SECRET || 'default_secret_replace_in_production';
    return jwt.verify(token, secret);
  } catch (error) {
    return null;
  }
};