# VinzClortho — Credential Rotation Log

This file tracks security incidents, exposure events, and outstanding rotation requirements.
Actual key values live in Vaultwarden (`vault.marvin`). Never store raw keys here.

---

## ⚠️ IMMEDIATE ROTATION REQUIRED (2026-05-21 audit)

### OpenAI API Key (`sk-proj-...`)
- **Exposure**: Found as raw text in `massdeb8/API.md` (scratch file, since deleted and gitignored)
- **GitHub push**: BLOCKED by GH013 secret scanning — key never reached GitHub
- **Local exposure**: Tool output during security audit session
- **Action**: Revoke at platform.openai.com/api-keys → generate new → store in Vaultwarden
- **Status**: ⬜ PENDING

### Google / Gemini API Key (`AIzaSy...`)
- **Exposure**: Found alongside OpenAI key in `massdeb8/API.md` (deleted)
- **GitHub push**: BLOCKED by GH013 secret scanning
- **Local exposure**: Tool output during security audit session
- **Action**: Revoke at aistudio.google.com/apikey → generate new → store in Vaultwarden
- **Status**: ⬜ PENDING

### hyit.io `OPERATOR_VAULT_KEY` (Fernet)
- **Exposure**: Tracked in git (`hyit.io/.env`) before gitignore was enforced; printed during audit
- **Scope**: hyit.io has no GitHub remote — not pushed — but scrollback contains value
- **Action**: Generate new Fernet key: `python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"` → update hyit.io/.env → store in Vaultwarden
- **Status**: ⬜ PENDING

### hyit.io `SESSION_SECRET`
- **Exposure**: Same as OPERATOR_VAULT_KEY above (same file, same session)
- **Action**: Generate new 64-char hex: `python3 -c "import secrets; print(secrets.token_hex(32))"` → update hyit.io/.env → store in Vaultwarden
- **Status**: ⬜ PENDING

### CEO-Sim `CEOS_JWT_SECRET`
- **Exposure**: Printed during security audit (cat ceos.env). File is now gitignored.
- **Action**: Generate new 64-char hex → update ceos.env → store in Vaultwarden
- **Status**: ⬜ PENDING

### Anthropic API Key
- **Exposure**: Previous session (2026-05-20) — appeared in tool output
- **Action**: Revoke at console.anthropic.com → generate new → store in Vaultwarden → update all service .env files
- **Status**: ⬜ PENDING (user notified 2026-05-20)

---

## ⚠️ SNMP Community Strings (fleet-wide)

- **Exposure**: `craic/INFRA.md` was publicly served via The Den (passwordless `/gemini/` endpoint) until 2026-05-20 lockdown. Den now replaced with honeypot.
- **Affected strings**: EDDIE RO, LAVE/VROOMFONDEL RO, trap community `ALBATROSS`
- **Action**: Rotate via `/etc/snmp/snmpd.conf` on each node → restart `snmpd.service` → update INFRA.md
- **Status**: ⬜ PENDING

---

## ✅ COMPLETED ROTATIONS

### CraicKen API Token
- **Rotation date**: 2026-05-20
- **Reason**: Token appeared in tool output during session
- **New token**: Stored in Vaultwarden (see `craicken/.env`)

### Gemini API Key (craicken/.env)
- **Rotation date**: 2026-05-20
- **Reason**: Exposed in tool output
- **Status**: Revoked — `REVOKED_REPLACE_ME` placeholder in file. New key not yet generated.

---

## Rotation Protocol

1. Revoke the old credential at the issuing service
2. Generate new credential
3. Store in Vaultwarden at `vault.marvin` (HTTPS, self-signed cert)
4. Update the relevant `.env` file on each affected node
5. Restart the affected service
6. Update this log: mark ⬜ → ✅ with rotation date

**Do NOT store raw credentials in this file, in git, or in chat.**
