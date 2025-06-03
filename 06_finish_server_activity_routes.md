# Finish Server – Activity Routes

Create and integrate the `activity.routes.ts` file for the SmartRunning backend.

### Requirements:

- Define CRUD endpoints for activities:
  - `POST /api/activity` — create a new activity
  - `GET /api/activity` — list all activities
  - `GET /api/activity/:id` — get a specific activity
  - `PUT /api/activity/:id` — update an activity
  - `DELETE /api/activity/:id` — delete an activity

### Models:

Use a Mongoose model for `Activity` with fields like:

- `userId: ObjectId`
- `title: string`
- `date: Date`
- `distance: number`
- `duration: number`
- `route: GeoJSON or similar`
- `surface: string`

Update `app.ts` to enable these routes by uncommenting the line for `activityRoutes`.

Ensure validation, error handling, and responses are consistent.
