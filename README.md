# KisanFlow

## AI-Powered Predictive Procurement Intelligence Platform

KisanFlow is an AI-powered agricultural procurement orchestration platform designed to reduce uncertainty for farmers and improve operational planning at procurement centres.

Instead of treating procurement as a simple slot-booking problem, KisanFlow combines:

- Farmer authentication
- Crop and quantity selection
- Procurement-centre recommendation
- Queue intelligence
- Operational prediction
- Resource recommendation
- What-if simulation
- Booking management

into a single decision-support platform.

---

## Problem

Agricultural procurement can create uncertainty for both farmers and procurement-centre operators.

### Farmers may face:

- Uncertainty about which centre to visit
- Long and unpredictable waiting times
- Lack of visibility into centre conditions
- Unnecessary travel
- Overcrowding at popular centres
- Difficulty planning procurement visits

### Procurement centres may face:

- Uneven farmer arrivals
- Queue buildup
- Resource constraints
- Difficulty anticipating operational load
- Limited decision-support tools
- Inefficient resource allocation

A conventional appointment or slot-booking system mainly manages bookings.

KisanFlow goes further by introducing an operational intelligence layer to support procurement decisions.

---

# Solution

KisanFlow acts as a decision-support layer between farmers and procurement centres.

The platform provides two primary experiences.

### Farmer Side

Farmers can:

1. Register and log in.
2. Select a crop.
3. Enter expected procurement quantity.
4. Receive suitable centre recommendations.
5. Review operational conditions.
6. Create a procurement booking.
7. Track their bookings.

### Operator Side

Operators can:

1. View procurement intelligence.
2. Monitor queue and operational conditions.
3. View operational predictions.
4. Receive resource recommendations.
5. Run what-if simulations.
6. Evaluate potential operational scenarios.

---

# Key Features

## 1. Farmer Authentication

Farmers can create accounts and securely authenticate using JWT-based authentication.

The authentication flow protects farmer-specific operations such as bookings and profile-related actions.

---

## 2. Procurement Centre Recommendation

KisanFlow recommends suitable procurement centres using multiple operational factors.

The recommendation layer considers signals such as:

- Queue length
- Estimated waiting time
- Centre capacity
- Operational status
- Resource availability
- Crop-related conditions
- Distance-related factors

This helps transform a simple "find a centre" workflow into a decision-support experience.

---

## 3. Booking Management

Authenticated farmers can create procurement bookings based on their selected crop, quantity, and recommended centre.

Bookings are stored in PostgreSQL and can be retrieved through the farmer's booking interface.

---

## 4. My Bookings

Farmers can view their existing procurement bookings from a dedicated interface.

This provides visibility into their planned procurement activity.

---

## 5. Procurement Intelligence

The operator dashboard provides centre-level operational intelligence.

It combines procurement-related signals to help operators understand the current state of a centre.

---

## 6. Operational Prediction

KisanFlow generates operational predictions using the current procurement and resource context.

The prediction layer is designed to support decisions such as:

- Anticipating operational load
- Identifying potential queue pressure
- Understanding resource requirements
- Supporting procurement planning

---

## 7. Resource Recommendation

The platform provides resource recommendations based on operational conditions.

This can help operators reason about whether additional operational resources may be required.

---

## 8. What-if Simulation

Operators can run what-if scenarios to understand how changes in operational conditions could affect procurement operations.

Example scenario inputs include changes to:

- Expected farmer arrivals
- Processing capacity
- Resource availability
- Operational load

This allows operators to explore decisions before implementing them.

---

# AI / Prediction Approach

## Current MVP

The current KisanFlow MVP uses:

> **Operational prediction + multi-factor decision logic**

It does **not** claim to use a trained machine learning model in the current prototype.

The decision and prediction layer combines operational signals such as:

- Queue length
- Estimated waiting time
- Centre capacity
- Resource availability
- Crop information
- Procurement conditions
- Centre operational state
- Distance-related factors

These signals are processed through backend decision and prediction services to produce recommendations and operational insights.

---

## Why This Approach?

A production ML model requires reliable historical procurement data.

The current prototype focuses on validating the complete procurement orchestration workflow first:

```text
Operational Data
       ↓
Decision Logic
       ↓
Prediction / Recommendation
       ↓
Farmer or Operator Action
```

---


# Future ML Evolution

With sufficient historical procurement data, KisanFlow can evolve toward trained ML models for:

- Queue waiting-time prediction
- Farmer arrival forecasting
- Procurement demand forecasting
- Centre congestion prediction
- Resource demand forecasting
- Procurement load forecasting
- Dynamic centre recommendations

Potential future ML architecture:

```text
Historical Procurement Data
          ↓
     Data Pipeline
          ↓
 Feature Engineering
          ↓
   ML Model Training
          ↓
 Model Evaluation
          ↓
 Model Serving
          ↓
 KisanFlow Decision Layer
```

---

# System Architecture
                         ┌─────────────────────┐
                         │       Farmer        │
                         │       Web App       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    React + Vite     │
                         │      Frontend       │
                         └──────────┬──────────┘
                                    │
                               REST API
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │      Backend        │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌─────────────┐       ┌─────────────┐       ┌──────────────┐
       │   Routers   │       │  Services   │       │ Repositories │
       └─────────────┘       └──────┬──────┘       └──────┬───────┘
                                     │                     │
                                     └──────────┬──────────┘
                                                ▼
                              ┌────────────────────────────┐
                              │ Decision / Intelligence    │
                              │           Layer            │
                              └──────────────┬─────────────┘
                                             │
                                             ▼
                                   ┌──────────────────┐
                                   │   PostgreSQL     │
                                   │     Database     │
                                   └──────────────────┘


# Backend Architecture

KisanFlow follows a layered backend architecture:

Router
   ↓
Service
   ↓
Repository
   ↓
SQLAlchemy ORM
   ↓
PostgreSQL

## Router Layer

Handles:

HTTP requests
Request validation
Response handling
API routing

Routers remain thin and delegate business operations to services.

## Service Layer

Contains:

Business logic
Decision logic
Authorization-related operations
Prediction logic
Recommendation logic
Simulation logic

## Repository Layer

Handles:

Database queries
Persistence
Data retrieval

Repositories do not contain business decision logic.

# ORM / Models

SQLAlchemy models represent the application's database entities.

---

# Technology Stack

## Frontend

- React
- Vite
- Tailwind CSS
- Axios
- React Router

## Backend

- Python
- FastAPI
- SQLAlchemy 2.0
- Pydantic
- JWT
- Passlib
- Alembic

## Database

- PostgreSQL

## Testing

- pytest

## Deployment

- Vercel — Frontend
- Render — FastAPI Backend
- Render PostgreSQL — Database

## Development

- Git
- GitHub
- VS Code

---

# Database

KisanFlow uses PostgreSQL for persistent application data.

The database includes entities for:

- Farmers
- Operators
- Centres
- Crops
- Prices
- Bookings
- Queues
- Resources
- Predictions
- Recommendations
- Simulations
- Feedback

Database schema changes are managed using Alembic migrations.

Migration files are located at:

```text
backend/alembic/versions/
```

---

# Farmer Workflow

```text
                 ┌───────────────┐
                 │    Farmer     │
                 └───────┬───────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Register / Login │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Select Crop +   │
                │ Quantity        │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Centre          │
                │ Recommendation  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Create Booking  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  My Bookings    │
                └─────────────────┘
```

# Operator Workflow
                ┌──────────────────────┐
                │ Operator Dashboard   │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Procurement          │
                │ Intelligence         │
                └──────────┬───────────┘
                           │
             ┌─────────────┼──────────────┐
             │             │              │
             ▼             ▼              ▼
      ┌────────────┐ ┌────────────┐ ┌──────────────┐
      │ Predictions│ │  Resource  │ │ What-if      │
      │            │ │Recommendation│ │ Simulation  │
      └────────────┘ └────────────┘ └──────────────┘


# API

The backend provides REST APIs for:

Authentication
Farmer registration
Farmer login
Farmer profile
Crops
Procurement centres
Centre intelligence
Bookings
Centre recommendations
Operator dashboard
Resource recommendations
Predictions
What-if simulations
Feedback
Health checks

---

# API Documentation

Interactive Swagger documentation is available at:

https://kisanflow-api-wzpm.onrender.com/docs

---

# Production Health Checks

The deployed backend provides:

```text
GET /health
GET /health/db

Production health endpoint:

https://kisanflow-api-wzpm.onrender.com/health

Database health endpoint:

https://kisanflow-api-wzpm.onrender.com/health/db

These endpoints verify application availability and database connectivity.
```

# Live Demo
Frontend

https://kisan-flow-eight.vercel.app/

Backend

https://kisanflow-api-wzpm.onrender.com

Swagger API Documentation

https://kisanflow-api-wzpm.onrender.com/docs

GitHub Repository

https://github.com/khawahishdabra-commits/KisanFlow


# Local Setup
Prerequisites

Install:

Python 3.13+
Node.js
npm
PostgreSQL


# Git

1. Clone Repository
git clone https://github.com/khawahishdabra-commits/KisanFlow.git
cd KisanFlow


2. Backend Setup

Navigate to the backend:

cd backend

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt


3. Backend Environment Variables

Create:

backend/.env

Example:

DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

Do not commit .env files or production secrets to GitHub.


4. Database Migration

Run:

alembic upgrade head


5. Seed Demo Data

For local development:

python -m app.seed.seed_data

This creates the demo procurement data used by the prototype.


6. Start Backend

From the backend directory:

python -m uvicorn app.main:app --reload

Backend:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs


7. Frontend Setup

Open another terminal:

cd frontend

Install dependencies:

npm install

Create:

frontend/.env

with:

VITE_API_URL=http://127.0.0.1:8000

Start the frontend:

npm run dev

Frontend:

http://localhost:5173


# License

This project is currently developed as an SIH prototype.

License information can be added according to the team's final distribution requirements.