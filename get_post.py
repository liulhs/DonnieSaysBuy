from api import Api
import json

def get_post_by_username_and_id(username: str, post_id: str):
    """
    Fetch a specific post by username and post ID from Truth Social.
    Args:
        username (str): The username (e.g., 'realDonaldTrump')
        post_id (str): The post ID (e.g., '114359040827344338')
    Returns:
        dict: The post data if found, else None.
    """
    api = Api()
    user_info = api.lookup(username)
    if not user_info:
        raise ValueError(f"User '{username}' not found.")
    post = api._get(f"/v1/statuses/{post_id}")
    if not post or (post.get('account', {}).get('username', '').lower() != username.lower()):
        raise ValueError(f"Post ID {post_id} not found for user @{username}.")
    return post

if __name__ == "__main__":
    username = "realDonaldTrump"
    post_id = "114360632714487285"
    post = get_post_by_username_and_id(username, post_id)
    print(json.dumps(post, indent=2))
