from utils.db import execute_command, run_query
from datetime import datetime, timedelta

def seed_data():
    """Seeds the database with initial demo data if empty."""
    
    # Check if data exists
    existing_posts = run_query("SELECT count(*) as count FROM posts")
    if not existing_posts.empty and existing_posts.iloc[0]['count'] > 0:
        return

    print("Seeding database...")

    # Seed Media Assets
    assets = [
        ("assets/sample_images/coffee_morning.jpg", "manual", "coffee, lifestyle"),
        ("assets/sample_images/beans_bag.jpg", "manual", "product, beans"),
        ("assets/sample_images/latte_art.jpg", "ai", "coffee, art, cafe"),
        ("assets/sample_images/grower_story.jpg", "manual", "mission, people"),
    ]

    for path, source, tags in assets:
        execute_command(
            "INSERT INTO media_assets (media_path, source, tags) VALUES (?, ?, ?)",
            (path, source, tags)
        )

    # Seed Posts
    now = datetime.now()
    
    # 1. Posted (Past)
    execute_command('''
        INSERT INTO posts (title, platform, scheduled_at, caption, hashtags, media_path, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        "Morning Brew Launch",
        "Instagram",
        (now - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
        "Start your day with hope. ☕️ #BrewHope",
        "#coffee #morning #hope",
        "assets/sample_images/coffee_morning.jpg",
        "Posted",
        (now - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
    ))

    # 2. Scheduled (Future)
    execute_command('''
        INSERT INTO posts (title, platform, scheduled_at, caption, hashtags, media_path, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        "Farmer Spotlight: Juan",
        "Facebook",
        (now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
        "Meet Juan, one of our partner farmers. His dedication makes your cup possible. 🌱",
        "#directtrade #farmers #coffee",
        "assets/sample_images/grower_story.jpg",
        "Scheduled",
        (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    ))
    
    # 3. Draft (No schedule)
    execute_command('''
        INSERT INTO posts (title, platform, scheduled_at, caption, hashtags, media_path, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        "New Roast Coming Soon",
        "Instagram",
        None,
        "Something dark and mysterious is arriving next week...",
        "#newroast #darkroast",
        None,
        "Draft",
        now.strftime("%Y-%m-%d %H:%M:%S")
    ))

    # 4. Approved (Ready to schedule)
    execute_command('''
        INSERT INTO posts (title, platform, scheduled_at, caption, hashtags, media_path, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        "Latte Art Contest",
        "Both",
        (now + timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"),
        "Show us your best pour! Tag us to win a month of beans. 🎨",
        "#latteart #contest #barista",
        "assets/sample_images/latte_art.jpg",
        "Approved",
        (now - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S")
    ))

    print("Database seeded successfully.")
