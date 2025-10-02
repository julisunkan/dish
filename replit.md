# GlobalKitchen - Recipe Browser & Grocery List Manager

## Overview

GlobalKitchen is a lightweight Progressive Web App (PWA) that allows users to discover recipes from around the world using TheMealDB API and manage grocery lists for selected recipes. The application is built with Flask (Python) and provides a mobile-friendly, installable experience without requiring user authentication.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Template-Based Rendering with Jinja2**
- Server-side rendering using Flask's Jinja2 templating engine
- Bootstrap 5 for responsive, mobile-first UI components
- Base template (`base.html`) provides consistent navigation and layout across all pages
- Three main views: search, recipe detail, and grocery list

**Progressive Web App (PWA) Implementation**
- Service worker (`service-worker.js`) enables offline caching and app installation
- Manifest file (`static/manifest.json`) defines app metadata for installation
- Cache-first strategy for static assets (Bootstrap CSS/JS) and routes
- Installable on mobile and desktop devices

### Backend Architecture

**Flask Application Structure**
- Monolithic Flask app with route-based organization
- Session-based state management (no user authentication required)
- Three primary routes: `/search`, `/recipe/<meal_id>`, `/add-to-grocery-list/<meal_id>`
- Static file serving for PWA assets (service worker, manifest, icons)

**Session Management**
- Flask sessions store grocery list items temporarily (no persistent storage)
- Session secret key configured via environment variable with fallback
- Grocery list persists across page visits within the same browser session

**Data Models (SQLAlchemy)**
- Recipe model: stores recipe metadata (name, cuisine, category, instructions, image)
- Ingredient model: related to recipes with foreign key relationship
- SQLite database configured but not actively used (models defined for future enhancement)
- One-to-many relationship between Recipe and Ingredient with cascade delete

**Design Rationale**: Database models are defined but unused because the app relies on TheMealDB API for recipe data. This allows future expansion to save favorite recipes locally while keeping the initial implementation simple.

### External Dependencies

**TheMealDB API Integration**
- Base URL: `https://www.themealdb.com/api/json/v1/1`
- Two endpoints utilized:
  - Search by name: `/search.php?s={name}`
  - Lookup by ID: `/lookup.php?i={meal_id}`
- Ingredient parsing handles up to 20 ingredient/measure pairs from API response
- Error handling with graceful fallbacks for network failures

**Third-Party Libraries**
- **Flask**: Web framework and routing
- **SQLAlchemy**: ORM for database models (SQLite)
- **Requests**: HTTP client for API calls
- **Bootstrap 5**: Frontend UI framework (CDN-hosted)

**Database**
- SQLite file-based database (`globalkitchen.db`)
- No remote database configuration
- Local storage suitable for development and lightweight production use

**PWA Assets**
- Service worker for offline functionality and caching
- Icon files required at `/static/icons/icon-192.png` and `/static/icons/icon-512.png`
- Manifest defines app as standalone with green theme color (#198754)