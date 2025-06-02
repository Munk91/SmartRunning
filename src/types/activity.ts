import { Document, Types } from 'mongoose';

export interface IActivity extends Document {
  user: Types.ObjectId;
  activityType: string;
  distance: number;
  duration: number;
  startTime: Date;
  endTime: Date;
  averagePace: number;
  calories: number;
  location: {
    type: string;
    coordinates: number[][];
  };
  elevationGain: number;
  notes: string;
  createdAt: Date;
  updatedAt: Date;
}