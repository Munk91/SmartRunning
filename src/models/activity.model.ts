import mongoose, { Schema } from 'mongoose';
import { IActivity } from '../types/activity';

const ActivitySchema: Schema = new Schema(
  {
    user: { 
      type: Schema.Types.ObjectId, 
      ref: 'User',
      required: true 
    },
    activityType: { 
      type: String, 
      required: true,
      enum: ['run', 'walk', 'hike', 'cycle']
    },
    distance: { 
      type: Number, 
      required: true 
    },
    duration: { 
      type: Number, 
      required: true 
    },
    startTime: { 
      type: Date, 
      required: true 
    },
    endTime: { 
      type: Date, 
      required: true 
    },
    averagePace: { 
      type: Number, 
      required: true 
    },
    calories: { 
      type: Number, 
      default: 0 
    },
    location: {
      type: {
        type: String,
        enum: ['LineString'],
        default: 'LineString'
      },
      coordinates: {
        type: [[Number]],
        default: []
      }
    },
    elevationGain: { 
      type: Number, 
      default: 0 
    },
    notes: { 
      type: String, 
      default: '' 
    }
  },
  { timestamps: true }
);

// Create geospatial index
ActivitySchema.index({ location: '2dsphere' });

export default mongoose.model<IActivity>('Activity', ActivitySchema);