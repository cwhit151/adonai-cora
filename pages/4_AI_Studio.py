import streamlit as st
import time
from utils.ai_stub import generate_caption, generate_hashtags, generate_draft_results
from utils.helpers import set_page_config
from utils.db import execute_command
from datetime import datetime

set_page_config(page_title="AI Studio")

st.title("✨ AI Studio")
st.markdown("Generate captions, hashtags, or full posts using our fine-tuned model.")

tab1, tab2, tab3 = st.tabs(["Caption Generator", "Hashtag Helper", "Full Auto-Draft"])

with tab1:
    st.subheader("Generate a Caption")
    topic = st.text_input("What is this post about?", "Single origin Ethiopian coffee")
    tone = st.select_slider("Select Tone", options=["Warm & Inspiring", "Professional", "Exciting"])
    
    if st.button("Generate Caption"):
        with st.spinner("AI is thinking..."):
            result = generate_caption(topic, tone)
            st.success("Here's a draft:")
            st.text_area("Result", result, height=100)
            if st.button("Copy to Clipboard"):
                st.toast("Copied!")

with tab2:
    st.subheader("Generate Hashtags")
    tag_topic = st.text_input("Post Topic", "Latte art competition")
    
    if st.button("Get Tags"):
        with st.spinner("Finding trending tags..."):
            tags = generate_hashtags(tag_topic)
            st.code(tags)

with tab3:
    st.subheader("Create Full Draft Post")
    st.info("This will generate a caption, hashtags, and suggest media, then save it as a Draft.")
    
    draft_topic = st.text_input("Enter a topic for the post", "New seasonal blend launch")
    platform = st.selectbox("Intended Platform", ["Instagram", "Facebook", "Both"])
    
    if st.button("🚀 Generate & Save Draft"):
        with st.spinner("Brewing magic..."):
            res = generate_draft_results(draft_topic, platform)
            
            # Save to DB
            execute_command('''
                INSERT INTO posts (title, platform, caption, hashtags, media_path, status, created_at)
                VALUES (?, ?, ?, ?, ?, "AI Suggested", "Draft", CURRENT_TIMESTAMP)
            ''', (
                f"AI Generated: {draft_topic}", 
                platform, 
                res['caption'], 
                res['hashtags']
            ))
            
            st.balloons()
            st.success("Draft created successfully!")
            st.json(res)
            st.markdown(f"**Image Idea:** {res['image_idea']}")
            if st.button("Go to Post Editor"):
                st.switch_page("pages/3_Post_Editor.py")
