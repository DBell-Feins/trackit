# TrackIt

TrackIt is a Django project designed to make daily weight tracking easy and fun. It ships with an elegant data entry system and a powerful analytics engine that keeps you on track. The whole thing is tied together with an API for 3rd party access.

### Common features

#### Users
- Credentialed user
- User has email/password/role/associated login metadata (last login, last failure, etc.)
- Every credentialed user has a profile

#### Profiles
- A profile contains information that's important to the user.
- A profile has demographic information
    - Date of birth
    - Height
    - Starting weight
    
#### Goals
  - A collection of:
      - Start date
      - Target date
      - Start weight
      - Target weight
  - Manages a user's goal at any given time.
    
#### WeighIns
- A collection of user weight data.
- Contains a record of a user's weight on a given date.

### Entry features

The Entry app is a simple set of routing tools that expose an endpoint so the frontend can POST data. All requests to the entry app must be authenticated. Auth will be basic at first but later revisions will leverage OAuth.

The Entry app will parse the POST request, create the requisite models, and pass them to the storage engine.

### Analyze features

The Analyze app allows a user to track his/her progress. The first version will contain predefined analysis sets (graph of weight over time, graph of weight to goal, graph of goal comparisons, etc.) but later versions will allow the user to create their own analysis.

The Analyze app will also contain an API that allows consumers to request data sliced in different ways.