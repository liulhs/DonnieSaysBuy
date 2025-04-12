#!/usr/bin/env python3
# filepath: /home/jason/jason/DonnieSaysBuy/lookup_test.py

import os
from truthbrush.api import Api
import json

def test_lookup_simple():
    """Simple test of Truth Social lookup for user liulhs"""
    
    try:
        # Initialize API (will use environment credentials)
        print("Initializing API...")
        api = Api()
        
        # Look up the user
        print("Looking up user: liulhs")
        user = api.lookup(user_handle="liulhs")
        
        # Print result
        if user:
            print("\nUser found!")
            print(f"ID: {user.get('id')}")
            print(f"Username: {user.get('username')}")
            print(f"Display name: {user.get('display_name')}")
            print(f"Followers: {user.get('followers_count')}")
            print(f"Following: {user.get('following_count')}")
            print(f"Posts: {user.get('statuses_count')}")
            print(f"Verified: {user.get('verified')}")
            
            print("\nAll user data:")
            print(json.dumps(user, indent=2)[:1000] + "..." if len(json.dumps(user, indent=2)) > 1000 else json.dumps(user, indent=2))
            return True
        else:
            print("No user data returned")
            return False
    
    except Exception as e:
        print(f"Error looking up user: {e}")
        return False

if __name__ == "__main__":
    print("Truth Social User Lookup Test")
    print("----------------------------")
    test_lookup_simple()