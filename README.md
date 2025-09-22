# Hold'Em Analytics

![Main Page](assets/main-page.png)

## Description
Hold'Em Analytics is a full-stack web application that helps poker players simulate hands and calculate probabilities. Using an interactive drag-and-drop card interface, users can quickly evaluate hand strength and winning odds against multiple opponents.  

> ⚠️ Currently, the app includes the hand evaluator and odds calculator UI. Features like logging hands, user authentication, session history, and advanced analytics are in progress.

## Features (Current)
- **Interactive Drag-and-Drop Card Interface:** Move hole cards and community cards easily.
- **Texas Hold'em Probability Engine:** Monte Carlo simulations with Python multiprocessing for fast, accurate odds.
- **Hand Evaluation:** View your hand rank.
- **Odds Calculator:** Calculate win, tie, and loss probabilities against other players.

## Tech Stack
- **Frontend:** Next.js, React, Tailwind CSS, dnd-kit
- **Backend:** FastAPI, SQLModel, JWT authentication
- **Database:** PostgreSQL
- **Containerization:** Docker

## Running the Project

Build and start the application:

```bash
docker compose up --build
```

Stop the application:

```bash
docker compose down
```
