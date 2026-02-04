# CORA (Coffee Operations + Reporting Assistant)

CORA is a marketing operations MVP built for **Adonai Coffee**.

It is designed to help small brands plan, generate, and schedule social media content using a simple calendar-based workflow — with future support for AI-generated posts and automated Instagram/Facebook publishing.

This project is currently an **MVP demo** focused on proving the concept.

---

## 🚀 What CORA Does

CORA acts as a lightweight marketing command center:

- View upcoming posts in a content calendar  
- Draft and approve marketing content  
- Upload images manually or generate AI draft ideas  
- Track post status from draft → scheduled → posted  
- Maintain a library of reusable media assets  

---

## ✅ Current MVP Features

### Dashboard
- Quick overview of post statuses  
- Upcoming scheduled content preview  
- Fast actions to create or generate posts  

### Calendar
- Visual schedule of posts by day  
- Filter posts by platform and status  

### Post Editor
- Create and manage posts with:
  - Captions  
  - Hashtags  
  - Platform selection (Instagram / Facebook)  
  - Scheduling date + status tracking  

### AI Studio (Placeholder)
- Demo tools for:
  - Caption generation  
  - Hashtag generation  
  - AI draft post creation  

*(Real OpenAI integration will be added later.)*

### Media Library
- Upload and manage content assets  
- Tag and reuse images for future posts  

---

## 🗄️ Database Setup

CORA uses a local SQLite database for MVP simplicity:

- `posts` — scheduled marketing content  
- `media_assets` — uploaded/generated images  
- `publish_logs` — future publishing + retry tracking  

The schema is structured to easily migrate into **Postgres/Supabase** for production use.

---

## 🛠 Tech Stack

- Python  
- Streamlit  
- SQLite (Postgres-ready design)  
- GitHub + Streamlit Cloud Deployment  

---

## ▶️ How to Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/cwhit151/adonai-cora.git
cd adonai-cora
