import { IUser } from './user';

// Auth request is now defined in express.d.ts

export interface UserResponse {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

export const formatUserResponse = (user: IUser): UserResponse => {
  return {
    id: user._id?.toString() || '',
    name: user.name,
    email: user.email,
    createdAt: user.createdAt,
  };
};