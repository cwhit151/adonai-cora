import random
import time

def generate_caption(topic, tone="Warm & Inspiring"):
    """
    Simulates AI caption generation.
    In a real app, this would call OpenAI API.
    """
    # Simulate network delay
    time.sleep(1.5)
    
    templates = [
        f"Wake up and smell the hope. ☕️ Today we're thinking about {topic}. Every cup you drink supports freedom. #BrewHope",
        f"More than just coffee. It's a movement. {topic} is close to our hearts. Join us in making a difference today.",
        f"From the farm to your cup, {topic} matters. Experience the taste of ethical sourcing. 🌱",
        f"Your morning ritual, elevated. We believe in {topic} and the power of community. What's in your cup today?",
        f"Small beans, big impact. Let's talk about {topic}. Together we can change the world, one sip at a time."
    ]
    
    if tone == "Exciting":
        templates.append(f"Big news! 🚨 We are so hyped about {topic}! You don't want to miss this. Get ready!")
    elif tone == "Professional":
        templates.append(f"Adonai Coffee update: regarding {topic}. We remain committed to excellence and transparency in our supply chain.")
        
    return random.choice(templates)

def generate_hashtags(topic):
    """
    Simulates AI hashtag generation.
    """
    time.sleep(1.0)
    
    base_tags = ["#AdonaiCoffee", "#BrewHope", "#FundFreedom", "#SpecialtyCoffee"]
    topic_tags = [f"#{word}" for word in topic.split() if len(word) > 3]
    
    # Shuffle and pick a few
    all_tags = base_tags + topic_tags
    random.shuffle(all_tags)
    
    return " ".join(all_tags[:6])

def generate_draft_results(topic, platform):
    """
    Simulates generating a full post draft (caption + image suggestion).
    """
    time.sleep(2.5)
    
    caption = generate_caption(topic)
    hashtags = generate_hashtags(topic)
    
    image_suggestions = [
        "A steaming cup of coffee with morning light",
        "Close up of coffee beans in hands",
        "Barista pouring latte art",
        "Coffee farm landscape at sunset"
    ]
    
    return {
        "caption": caption,
        "hashtags": hashtags,
        "image_idea": random.choice(image_suggestions),
        "platform": platform
    }
