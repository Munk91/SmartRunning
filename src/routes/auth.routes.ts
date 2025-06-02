import { Router } from 'express';
import { register, login, getProfile } from '../controllers/auth.controller';
import { authMiddlewareWrapper } from '../middleware/auth-wrapper';

const router = Router();

// Auth routes
router.post('/register', register);
router.post('/login', login);
router.get('/profile', authMiddlewareWrapper, getProfile);

export default router;
