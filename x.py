"""
VinzClortho — X.com credential manager and API client
Supports multiple named accounts (splippers, hubbins_saint, marsha_m_bland, etc.)

Read ops  : Bearer Token (X_BEARER_TOKEN)
Write ops : OAuth 1.0a per account (X_{ACCOUNT}_API_KEY, X_{ACCOUNT}_API_SECRET,
            X_{ACCOUNT}_ACCESS_TOKEN, X_{ACCOUNT}_ACCESS_TOKEN_SECRET)
"""

import os
import requests
from requests_oauthlib import OAuth1

X_API = "https://api.x.com/2"
BEARER  = os.environ.get("X_BEARER_TOKEN", "")


def _bearer_headers():
    return {"Authorization": f"Bearer {BEARER}"}


def _oauth(account: str) -> OAuth1:
    account = account.upper()
    return OAuth1(
        os.environ[f"X_{account}_API_KEY"],
        os.environ[f"X_{account}_API_SECRET"],
        os.environ[f"X_{account}_ACCESS_TOKEN"],
        os.environ[f"X_{account}_ACCESS_TOKEN_SECRET"],
    )


# --------------------------------------------------------------------------- #
#  Read                                                                         #
# --------------------------------------------------------------------------- #

def get_user(username: str) -> dict:
    """Resolve a username to user object (id, name, username, public_metrics)."""
    r = requests.get(
        f"{X_API}/users/by/username/{username}",
        params={"user.fields": "public_metrics,description,created_at"},
        headers=_bearer_headers(), timeout=10,
    )
    r.raise_for_status()
    return r.json().get("data", {})


def get_latest_tweet(username: str) -> dict:
    """Return the most recent tweet from a user, including created_at."""
    user = get_user(username)
    user_id = user["id"]
    r = requests.get(
        f"{X_API}/users/{user_id}/tweets",
        params={
            "max_results": 5,
            "tweet.fields": "created_at,text",
            "exclude": "retweets,replies",
        },
        headers=_bearer_headers(), timeout=10,
    )
    r.raise_for_status()
    tweets = r.json().get("data", [])
    return tweets[0] if tweets else {}


# --------------------------------------------------------------------------- #
#  Write                                                                        #
# --------------------------------------------------------------------------- #

def post_tweet(account: str, text: str, reply_to: str = None) -> dict:
    """Post a tweet from a named account. account = 'splippers', 'hubbins_saint', etc."""
    payload = {"text": text[:280]}
    if reply_to:
        payload["reply"] = {"in_reply_to_tweet_id": reply_to}
    r = requests.post(
        f"{X_API}/tweets",
        json=payload,
        auth=_oauth(account), timeout=10,
    )
    r.raise_for_status()
    return r.json().get("data", {})


def delete_tweet(account: str, tweet_id: str) -> bool:
    r = requests.delete(
        f"{X_API}/tweets/{tweet_id}",
        auth=_oauth(account), timeout=10,
    )
    r.raise_for_status()
    return r.json().get("data", {}).get("deleted", False)


# --------------------------------------------------------------------------- #
#  DM                                                                           #
# --------------------------------------------------------------------------- #

def send_dm(account: str, participant_id: str, text: str) -> dict:
    r = requests.post(
        f"{X_API}/dm_conversations/with/{participant_id}/messages",
        json={"text": text},
        auth=_oauth(account), timeout=10,
    )
    r.raise_for_status()
    return r.json().get("data", {})
