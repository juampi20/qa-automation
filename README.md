# QA Automation — SauceDemo

Playwright + pytest test suite for [SauceDemo](https://www.saucedemo.com).

## Setup

```bash
uv sync
uv run playwright install chromium
```

## Run

```bash
# Full suite
uv run pytest

# Headless (CI default)
HEADLESS=true uv run pytest

# Slow motion (debug)
uv run pytest --headed --slowmo=1000

# Single file
uv run pytest src/tests/test_login.py -v
```

## Test areas

| File | Tests | Scope |
|------|-------|-------|
| `test_login.py` | 3 | Login valid/invalid/empty |
| `test_inventory.py` | 9 | Items, sorting, cart badge |
| `test_cart.py` | 9 | Add/remove, display, edge cases |
| `test_checkout.py` | 11 | Form validation, summary, totals, full flow |
| `test_item_details.py` | 6 | Detail view, add/remove, navigation |
| `test_sidebar.py` | 7 | Menu open/close, links, logout, reset |

**Total: 45 tests**

## Credentials

| User | Password | Notes |
|------|----------|-------|
| `standard_user` | `secret_sauce` | Normal flow |
| `locked_out_user` | `secret_sauce` | Login blocked |
| `problem_user` | `secret_sauce` | Images broken |
| `performance_glitch_user` | `secret_sauce` | Slow responses |

## Config

- Viewport: 1600×900
- Timeout: 10s default
- Browser: Chromium (session-scoped)
- Auth: fresh login per test (SauceDemo is an in-memory SPA)
- Env: `HEADLESS=true`, `SLOW_MO=<ms>`
