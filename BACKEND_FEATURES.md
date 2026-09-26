# Sarthak Backend Implementation Plan

This file lists all the backend features required for Sarthak. We will implement them one by one.

## 1. Core API & Database
- [x] Database Setup (PostgreSQL integration with SQLAlchemy/SQLModel).
- [x] Core Database Models (User, Video, Analysis, Conversation).
- [x] Media Upload & Storage (Endpoints to receive video/image and save temporarily).
- [x] Background Task Infrastructure (FastAPI BackgroundTasks or Celery/Redis for long-running video processing).

## 2. Video Processing Pipeline
- [x] FFmpeg Integration (Extracting audio from video).
- [x] Frame/Keyframe Extraction (Smart sampling to avoid processing every frame).
- [ ] Speech Transcription (Speech-to-text processing).
- [ ] OCR & Text Detection (Extracting on-screen text).

## 3. Multimodal AI Integration
- [x] Abstract `AIProvider` interface.
- [x] `GeminiProvider` implementation for video, image, and text reasoning.
- [x] Prompt Engineering for structured JSON extraction.

## 4. Structured Data Models (Pydantic Schemas)
- [x] GeneralAnalysis Schema
- [x] TravelAnalysis Schema
- [x] ShoppingAnalysis Schema
- [x] RecipeAnalysis Schema
- [x] FoodAnalysis Schema

## 5. Modular Agent System
- [x] Intent Detection / Router Agent (Classifies content to the correct specialized agent).
- [x] Travel Agent (Itinerary, budget, locations).
- [x] Shopping Agent (Products, prices, claims).
- [x] Recipe Agent (Ingredients, steps, grocery list).
- [x] Food/Restaurant Agent (Dishes, reviews, locations).
- [x] Fitness Agent (Workouts, form cues, reps).
- [x] Tech Tutorial Agent (Code snippets, settings).
- [x] Fashion Agent (Clothing items, brands, style).
- [x] DIY Agent (Tools, materials, step-by-step).
- [x] Finance Agent (Topics, frameworks, stock tickers).
- [x] Media Recommendation Agent (Books, movies, ratings).
- [x] General Agent (Default understanding).

## 6. Research & Verification
- [x] Web Research Module (Search web for current prices, alternatives).
- [x] Verification Engine (Cross-checking AI claims with web results and tagging source: DIRECT, SPOKEN, INFERRED, VERIFIED).

## 7. Chat & Context
- [x] Conversation Memory (Store past context for follow-up questions).
- [x] "Ask Sarthak" Endpoint (Natural language queries with context).

## 8. Final Polish
- [x] Timestamp Intelligence (Mapping extracted events to video timestamps).
- [x] Cleanup Jobs (Deleting temporary media after processing/saving).
