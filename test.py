#!/usr/bin/env python3
# filepath: /home/jason/jason/DonnieSaysBuy/lookup_test.py

import os
from truthbrush.api import Api
import json
from get_content import extract_plain_text, transcribe_youtube_link, transcribe_media_content, get_post_content

def test_get_latest_trump_post():
    """Get and parse the most recent post by Donald Trump on Truth Social"""
    
    try:
        # Initialize API (will use environment credentials)
        print("Initializing API...")
        api = Api()
        
        # Look up Donald Trump's user
        trump_handle = "realDonaldTrump"
        print(f"Looking up user: {trump_handle}")
        trump_user = api.lookup(user_handle=trump_handle)
        
        if not trump_user:
            print(f"Could not find user with handle: {trump_handle}")
            return False
        
        print(f"\nUser found: {trump_user.get('display_name')} (@{trump_user.get('username')})")
        
        # Get the most recent post
        print("\nFetching most recent post...")
        
        # pull_statuses returns an iterator, so we just need the first item
        latest_post = None
        for post in api.pull_statuses(trump_user.get('username'), replies=False, verbose=True):
            latest_post = post
            break  # Just get the first post
        
        if not latest_post:
            print("No posts found")
            return False
        
        # Parse and display the post
        print("\n== Latest Trump Post ==")
        print(f"Date: {latest_post.get('created_at')}")
        print(f"Content: {latest_post.get('content')}")
        print(f"URL: https://truthsocial.com/@{trump_user.get('username')}/posts/{latest_post.get('id')}")
        
        # Show metrics
        print(f"Likes: {latest_post.get('favourites_count')}")
        print(f"Reposts: {latest_post.get('reblogs_count')}")
        print(f"Replies: {latest_post.get('replies_count')}")
        
        print("\nFull post data:")
        print(json.dumps(latest_post, indent=2))
        
        return True
    
    except Exception as e:
        print(f"Error getting latest Trump post: {e}")
        return False

# Tests for get_content functions
def test_get_content():
    """Test get_content functions with sample JSON files."""
    base = os.path.dirname(__file__)
    mappings = [
        ('post_text.json', get_post_content),
        ('post_with_link.json', get_post_content),
        ('post_with_media.json', get_post_content),
    ]
    for filename, func in mappings:
        path = os.path.join(base, filename)
        try:
            with open(path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue
        print(f"--- Testing {func.__name__} on {filename} ---")
        try:
            text = func(data)
            print(text, "\n")
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")

if __name__ == "__main__":
    # print("Truth Social - Donald Trump's Latest Post")
    # print("----------------------------------------")
    # test_get_latest_trump_post()
    test_get_content()