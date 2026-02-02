# CORA (Coffee Operations + Reporting Assistant)

CORA is an MVP demo for Adonai Coffee, designed to act as a marketing calendar and AI post planner.

## Features
- **Dashboard**: Quick view of post statuses and upcoming schedule.
- **Calendar**: Visual grid of scheduled posts.
- **Post Editor**: Create, edit, and schedule posts for Instagram/Facebook.
- **AI Studio**: Placeholder AI tools for generating captions and hashtags.
- **Library**: Manage media assets.

## Setup & Run

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app:**
    ```bash
    streamlit run app.py
    ```

The app will use a local SQLite database (`cora.db`) which will be automatically seeded with demo data on the first run.
