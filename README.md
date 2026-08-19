# Podcast Transcript Parser
### Final Project - LING 508: Computational Techniques for Linguists

A Flask + MySQL app that parses raw podcast transcripts into cleaned,
speaker-labeled dialogue. The fully documented use case is [here](./documents/Week1_UseCases.pdf).

Podcast data source: [Podscribe](https://podscribe.com/)  
Podscribe API Documentation: https://docs.api.podscribe.com/#/paths/api-public-episode-transcript/get

## Table of Contents
- [Prerequisites](#prerequisites)
- [Running the app](#running-the-app)
- [Using the web form](#using-the-web-form)
- [API Endpoints](#api-endpoints)
- [Data Persistence](#data-persistence)
- [Running Tests](#running-tests)

## Prerequisites
- Docker Desktop installed and running

## Running the app
From the project root:
```bash
docker compose up --build
```
First startup takes ~10-15 seconds while MySQL initializes. Once ready,
open http://localhost:5000/ in a browser.

## Using the web form
1. Fill in Podcast Name, Filename, and paste a raw transcript (JSON array
   of word objects) into the Raw Transcript field. There is sample data below
2. Select "Clean" mode.
3. Click Submit — the cleaned transcript and dialogue will appear below.

### Sample data
- Podcast Name: `Will the Kawhi Trade Go Through?`
- Filename: `thezachloweshow_20260804.txt`
- Raw Transcript JSON (short sample below; a full example transcript is in
  [`test_transcript.json`](./data/test_data/test_transcript.json)):

```json
[
  {"speaker":0,"word":"Welcome","startTime":0},
  {"speaker":0,"word":"back","startTime":0.3},
  {"speaker":0,"word":"to","startTime":0.6},
  {"speaker":0,"word":"the","startTime":0.9},
  {"speaker":0,"word":"show","startTime":1.2},
  {"speaker":0,"word":"today","startTime":1.5},
  {"speaker":0,"word":"we're","startTime":1.8},
  {"speaker":0,"word":"diving","startTime":2.1},
  {"speaker":0,"word":"into","startTime":2.4},
  {"speaker":0,"word":"the","startTime":2.7},
  {"speaker":0,"word":"biggest","startTime":3.0},
  {"speaker":0,"word":"trade","startTime":3.3},
  {"speaker":0,"word":"rumors","startTime":3.6},
  {"speaker":0,"word":"rocking","startTime":3.9},
  {"speaker":0,"word":"the","startTime":4.2},
  {"speaker":0,"word":"league","startTime":4.5},
  {"speaker":0,"word":"right","startTime":4.8},
  {"speaker":0,"word":"now","startTime":5.1},
  {"speaker":2,"word":"Advertisement.","startTime":5.4},
  {"speaker":1,"word":"Thanks","startTime":5.7},
  {"speaker":1,"word":"for","startTime":6.0},
  {"speaker":1,"word":"having","startTime":6.3},
  {"speaker":1,"word":"me","startTime":6.6},
  {"speaker":1,"word":"I'm","startTime":6.9},
  {"speaker":1,"word":"excited","startTime":7.2},
  {"speaker":1,"word":"to","startTime":7.5},
  {"speaker":1,"word":"break","startTime":7.8},
  {"speaker":1,"word":"down","startTime":8.1},
  {"speaker":1,"word":"what","startTime":8.4},
  {"speaker":1,"word":"this","startTime":8.7},
  {"speaker":1,"word":"trade","startTime":9.0},
  {"speaker":1,"word":"could","startTime":9.3},
  {"speaker":1,"word":"mean","startTime":9.6},
  {"speaker":1,"word":"for","startTime":9.9},
  {"speaker":1,"word":"both","startTime":10.2},
  {"speaker":1,"word":"teams","startTime":10.5}
]
```

## Project Structure
```
├── main.py                  # Flask API server
├── app/
│   ├── models.py           # Transcript, Dialogue, Podcast dataclasses
│   ├── services.py         # TranscriptService — coordinates business logic
│   ├── transcript_processor.py  # Cleaning/speaker-labeling logic
│   └── enums.py             # ProcessingMode
├── db/
│   ├── repository.py       # Abstract repository interface
│   ├── mysql_repository.py # MySQL implementation
│   └── init.sql            # Database schema
├── web/
│   └── index.html          # Form UI
├── tests/                  # pytest test suite
├── docker-compose.yml
└── Dockerfile
```

## API Endpoints

### POST /transcripts
Creates and processes a transcript.

Example:
```bash
curl -X POST http://localhost:5000/transcripts \
-H "Content-Type: application/json" \
-d @test_payload.json
```
Returns 201 with the full transcript (including cleaned dialogue) as JSON.

### GET /transcripts/<id>
Retrieves a previously saved transcript by id.

Example:
```bash
curl http://localhost:5000/transcripts/1
```
Returns 200 with the transcript JSON, or 404 if not found.

## Data persistence
Transcript data is stored in a Docker volume and persists across restarts.
To fully reset the database: 
```bash
docker compose down -v
```
## Running tests
Tests connect to the containerized MySQL database, so the app must be running first:
```bash
docker compose up --build -d
docker compose exec app pytest -v
```