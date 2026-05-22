"""
VinzClortho — Stripe credential helper for Shoulders (splippers.com store)

Reads credentials from environment and exposes thin wrappers used by the
setup wizard and any admin scripts.
"""
from __future__ import annotations

import os
import stripe as _stripe


# Live product/price IDs — created 2026-05-22
PRODUCT_ID = "prod_UYwXjCqEUJPboN"
PRICE_ID    = "price_1TZpG40hSs6KrAknRm8sqJEH"  # £19/month


def _configure() -> None:
    key = os.environ.get("STRIPE_SECRET_KEY")
    if not key:
        raise RuntimeError("STRIPE_SECRET_KEY not set")
    _stripe.api_key = key


def get_product() -> dict:
    _configure()
    return _stripe.Product.retrieve(PRODUCT_ID)


def get_price() -> dict:
    _configure()
    return _stripe.Price.retrieve(PRICE_ID)


def list_subscriptions(limit: int = 20) -> list[dict]:
    _configure()
    return _stripe.Subscription.list(limit=limit).data


def get_customer(customer_id: str) -> dict:
    _configure()
    return _stripe.Customer.retrieve(customer_id)
