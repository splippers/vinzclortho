"""
VinzClortho setup wizard — generates a local .env with your X API credentials.
Run once per machine. The .env is gitignored and never leaves your box.
"""

import os

ENV_FILE = os.path.join(os.path.dirname(__file__), ".env")


def prompt(label, secret=False):
    val = input(f"  {label}: ").strip()
    return val


def main():
    print("\n=== VinzClortho Setup Wizard ===")
    print("Are you the Keymaster? Good. Let's fill the gaps.\n")

    lines = []

    bearer = prompt("X Bearer Token (read-only, shared across all accounts)")
    lines.append(f"X_BEARER_TOKEN={bearer}")
    lines.append("")

    while True:
        nickname = input("\nAccount nickname (e.g. myaccount) — or press Enter to finish: ").strip()
        if not nickname:
            break
        handle = input(f"  X handle for {nickname} (without @): ").strip()
        key = prompt(f"  API Key")
        secret = prompt(f"  API Secret")
        token = prompt(f"  Access Token")
        token_secret = prompt(f"  Access Token Secret")

        slug = nickname.upper().replace("@", "").replace(" ", "_")
        lines.append(f"# @{handle} ({nickname})")
        lines.append(f"X_{slug}_API_KEY={key}")
        lines.append(f"X_{slug}_API_SECRET={secret}")
        lines.append(f"X_{slug}_ACCESS_TOKEN={token}")
        lines.append(f"X_{slug}_ACCESS_TOKEN_SECRET={token_secret}")
        lines.append("")

    with open(ENV_FILE, "w") as f:
        f.write("\n".join(lines))

    print(f"\nSaved to {ENV_FILE}")
    print("Load it with: export $(grep -v '^#' .env | xargs)")
    print("\nDone. VinzClortho is ready.\n")


if __name__ == "__main__":
    main()
