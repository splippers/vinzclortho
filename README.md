# VinzClortho

*"Yes, have some!"*

The Keymaster. Central credential manager and API client hub for the Splipperverse.

Run the setup wizard to register your accounts and generate your local `.env`:

```bash
python3 setup.py
```

---

## X.com (`x.py`)

Read operations use a shared Bearer Token. Write operations (posting, DMs) use per-account OAuth 1.0a.

### Environment variables

| Variable | Purpose |
|----------|---------|
| `X_BEARER_TOKEN` | Read-only access — profile lookups, latest tweets |
| `X_{ACCOUNT}_API_KEY` | Per-account OAuth 1.0a |
| `X_{ACCOUNT}_API_SECRET` | Per-account OAuth 1.0a |
| `X_{ACCOUNT}_ACCESS_TOKEN` | Per-account OAuth 1.0a |
| `X_{ACCOUNT}_ACCESS_TOKEN_SECRET` | Per-account OAuth 1.0a |

`{ACCOUNT}` is the uppercased nickname you choose during setup (e.g. `MYACCOUNT`).

### Usage

```python
from vinzclortho.x import get_latest_tweet, post_tweet, send_dm

# Check when someone last posted
tweet = get_latest_tweet("someusername")
print(tweet["created_at"], tweet["text"])

# Post from a named account
post_tweet("myaccount", "Hello from VinzClortho.")

# DM someone
send_dm("myaccount", "<their_user_id>", "Hi there.")
```

### Getting API keys

1. Go to [developer.x.com](https://developer.x.com)
2. Create a project and app for each account
3. Generate OAuth 1.0a keys (API Key, API Secret, Access Token, Access Token Secret)
4. Get your Bearer Token from the app dashboard
5. Run `python3 setup.py` and paste them in when prompted

## Dependencies

```
requests
requests-oauthlib
```
