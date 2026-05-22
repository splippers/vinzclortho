# VinzClortho

*"Yes, have some!"*

The Keymaster. Central credential manager and API client hub for the Splipperverse.

Run the setup wizard to register your accounts and generate your local `.env` files:

```bash
python3 setup.py
```

---

## Shoulders / store.splippers.com (`stripe_shoulders.py`)

UK statutory register management SaaS. Manages Stripe credentials and pre-wires the live product/price.

### What the wizard does for you
- Writes `../splippers.com/.env` with all required vars
- Generates a `TOKEN_ENCRYPTION_KEY` (Fernet — save it, it encrypts OAuth tokens at rest)
- Pre-fills `STRIPE_PRICE_ID=price_1TZpG40hSs6KrAknRm8sqJEH` (£19/month, live, created 2026-05-22)

### What you need to provide

| What | Where to get it |
|------|-----------------|
| `STRIPE_SECRET_KEY` | Stripe Dashboard → Developers → API keys → Secret key |
| `STRIPE_WEBHOOK_SECRET` | After registering webhook URL in Stripe (see below) |
| Cloud storage OAuth app credentials | Google Console / Dropbox App Console / Azure App Registration |

### Registering the Stripe webhook (after deploy)

1. Go to Stripe Dashboard → Developers → Webhooks → Add endpoint
2. URL: `https://store.splippers.com/billing/webhook`
3. Events: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`
4. Copy the signing secret (`whsec_...`) and re-run `python3 setup.py` or add to `.env` manually

### Environment variables

| Variable | Purpose |
|----------|---------|
| `STRIPE_SECRET_KEY` | Stripe live secret key |
| `STRIPE_WEBHOOK_SECRET` | Webhook signing secret |
| `STRIPE_PRICE_ID` | Pre-filled — £19/month recurring |
| `TOKEN_ENCRYPTION_KEY` | Fernet key for encrypting OAuth tokens at rest |
| `APP_BASE_URL` | Public URL of the deployed service |
| `OAUTH_REDIRECT_URI` | OAuth callback (auto-set from APP_BASE_URL) |
| `GOOGLE_CLIENT_ID/SECRET` | Google Drive OAuth app |
| `DROPBOX_APP_KEY/SECRET` | Dropbox OAuth app |
| `ONEDRIVE_CLIENT_ID/SECRET` | Microsoft OneDrive OAuth app |

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
