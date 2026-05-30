# MindGarden Backend API Endpoints

Base path: `/api`

> Protected endpoints require an `Authorization: Bearer <access_token>` header.

---

## Authentication

### POST `/api/auth/register/`
Create a new user account.

Request JSON:
```json
{
  "email": "user@example.com",
  "fullname": "Jane Doe",
  "password": "securepassword"
}
```

Response JSON:
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "fullname": "Jane Doe",
    "avatar": null,
    "preferred_language": "en",
    "emotional_goals": "",
    "joined_at": "2026-05-22T14:00:00Z"
  },
  "tokens": {
    "refresh": "<refresh_token>",
    "access": "<access_token>"
  }
}
```

### POST `/api/auth/login/`
Obtain JWT access and refresh tokens.

Request JSON:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

Response JSON:
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### POST `/api/auth/refresh/`
Refresh access token using a refresh token.

Request JSON:
```json
{
  "refresh": "<refresh_token>"
}
```

Response JSON:
```json
{
  "access": "<new_access_token>"
}
```

### POST `/api/auth/logout/`
Blacklist a refresh token and log out the user.

Request JSON:
```json
{
  "refresh": "<refresh_token>"
}
```

Response:
- Status `205 Reset Content`
- No body expected.

---

## User Profile

### GET `/api/users/me/`
Retrieve the current authenticated user.

Response JSON:
```json
{
  "id": 1,
  "email": "user@example.com",
  "fullname": "Jane Doe",
  "avatar": null,
  "preferred_language": "en",
  "emotional_goals": "Improve mindfulness",
  "joined_at": "2026-05-22T14:00:00Z"
}
```

### PATCH `/api/users/me/`
Update the current user's profile.

Request JSON:
```json
{
  "fullname": "Jane Doe",
  "preferred_language": "fr",
  "emotional_goals": "Practice daily breathing exercises"
}
```

Response JSON:
```json
{
  "id": 1,
  "email": "user@example.com",
  "fullname": "Jane Doe",
  "avatar": null,
  "preferred_language": "fr",
  "emotional_goals": "Practice daily breathing exercises",
  "joined_at": "2026-05-22T14:00:00Z"
}
```

---

## Journals

### GET `/api/journals/`
List journal entries for the current user.

Response JSON:
```json
[
  {
    "id": 12,
    "user": 1,
    "text": "I felt anxious today because...",
    "audio_file": null,
    "transcription": "",
    "mood": "anxious",
    "stress_score": 72,
    "sentiment_score": 0.35,
    "created_at": "2026-05-22T13:45:00Z"
  }
]
```

### POST `/api/journals/`
Create a new journal entry.

Request JSON (text entry):
```json
{
  "text": "Today I felt calm after walking in the park.",
  "audio_file": null
}
```

Response JSON:
```json
{
  "id": 13,
  "user": 1,
  "text": "Today I felt calm after walking in the park.",
  "audio_file": null,
  "transcription": "",
  "mood": "",
  "stress_score": null,
  "sentiment_score": null,
  "created_at": "2026-05-22T15:00:00Z"
}
```

> Note: Audio uploads should use `multipart/form-data` and include an `audio_file` field.

### GET `/api/journals/{id}/`
Retrieve a single journal entry.

Response JSON:
```json
{
  "id": 13,
  "user": 1,
  "text": "Today I felt calm after walking in the park.",
  "audio_file": null,
  "transcription": "",
  "mood": "",
  "stress_score": null,
  "sentiment_score": null,
  "created_at": "2026-05-22T15:00:00Z"
}
```

### PATCH `/api/journals/{id}/`
Update a journal entry's text or mood.

Request JSON:
```json
{
  "text": "I felt calm after the walk.",
  "mood": "calm"
}
```

Response JSON:
```json
{
  "id": 13,
  "user": 1,
  "text": "I felt calm after the walk.",
  "audio_file": null,
  "transcription": "",
  "mood": "calm",
  "stress_score": null,
  "sentiment_score": null,
  "created_at": "2026-05-22T15:00:00Z"
}
```

### DELETE `/api/journals/{id}/`
Delete a journal entry.

Response:
- Status `204 No Content`
- No body expected.

### POST `/api/journals/upload-audio/`
Upload an audio file for a journal entry.

Request:
- `Content-Type: multipart/form-data`
- Field: `audio_file`

Response JSON example:
```json
{
  "id": 14,
  "user": 1,
  "text": "",
  "audio_file": "http://localhost:8000/media/journals/audio/example.mp3",
  "transcription": "I felt anxious today...",
  "mood": "anxious",
  "stress_score": 78,
  "sentiment_score": 0.30,
  "created_at": "2026-05-22T15:10:00Z"
}
```

---

## Emotion Analysis

### GET `/api/emotions/`
List emotion analyses for the current user.

Response JSON:
```json
[
  {
    "id": 5,
    "user": 1,
    "journal_entry": 13,
    "stress_score": 72,
    "sadness_score": 20,
    "anxiety_score": 55,
    "positivity_score": 25,
    "emotion": "anxiety",
    "recommendation": "breathing_exercise",
    "critical_flags": [],
    "created_at": "2026-05-22T15:20:00Z"
  }
]
```

### GET `/api/emotions/{id}/`
Retrieve a single emotion analysis.

Response JSON:
```json
{
  "id": 5,
  "user": 1,
  "journal_entry": 13,
  "stress_score": 72,
  "sadness_score": 20,
  "anxiety_score": 55,
  "positivity_score": 25,
  "emotion": "anxiety",
  "recommendation": "breathing_exercise",
  "critical_flags": [],
  "created_at": "2026-05-22T15:20:00Z"
}
```

---

## Breathing Exercises

### GET `/api/breathing/exercises/`
List all breathing exercises.

Response JSON:
```json
[
  {
    "id": 1,
    "title": "4-7-8 Relaxation",
    "description": "Breathe in 4 seconds, hold 7 seconds, exhale 8 seconds.",
    "duration_seconds": 60,
    "rhythm": "4-7-8",
    "audio_guide": "http://localhost:8000/media/breathing/audio/relaxation.mp3",
    "category": "relaxation",
    "is_active": true
  }
]
```

### GET `/api/breathing/exercises/{pk}/`
Retrieve a single breathing exercise.

Response JSON:
```json
{
  "id": 1,
  "title": "4-7-8 Relaxation",
  "description": "Breathe in 4 seconds, hold 7 seconds, exhale 8 seconds.",
  "duration_seconds": 60,
  "rhythm": "4-7-8",
  "audio_guide": "http://localhost:8000/media/breathing/audio/relaxation.mp3",
  "category": "relaxation",
  "is_active": true
}
```

---

## Notifications

### GET `/api/notifications/`
List notifications for the current user.

Response JSON:
```json
[
  {
    "id": 7,
    "user": 1,
    "message": "Time for your journaling session!",
    "notification_type": "reminder",
    "is_read": false,
    "created_at": "2026-05-22T16:00:00Z"
  }
]
```

---

## Insights

### GET `/api/insights/weekly/`
Get weekly aggregated emotion statistics.

Response JSON:
```json
{
  "avg_stress": 65.4,
  "avg_sadness": 28.1,
  "avg_anxiety": 50.0,
  "avg_positivity": 35.7,
  "count": 8
}
```

### GET `/api/insights/monthly/`
Get monthly aggregated emotion statistics.

Response JSON:
```json
{
  "avg_stress": 61.2,
  "avg_sadness": 24.5,
  "avg_anxiety": 48.3,
  "avg_positivity": 37.0,
  "count": 29
}
```

---

## Documentation Endpoints

### GET `/api/schema/`
Return the OpenAPI schema JSON for the API.

### GET `/api/docs/`
Serve Swagger UI documentation.

### GET `/api/redoc/`
Serve Redoc documentation.
