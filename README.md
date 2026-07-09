# QA Automation — SauceDemo

Playwright + pytest test suite for [SauceDemo](https://www.saucedemo.com).

## Setup

```bash
uv sync
uv run playwright install chromium
```

## Run

```bash
# Full suite (headless)
uv run pytest

# Slow motion (debug)
uv run pytest --headed --slowmo=1000

# Single file
uv run pytest src/tests/test_login.py -v
```

## Allure Reporting

Genera un reporte HTML interactivo con features, stories, severidad, pasos y screenshots automáticos en fallos.

```bash
# Generar resultados
uv run pytest --alluredir=allure-results

# Generar y abrir reporte HTML
uv run allure generate allure-results --clean -o allure-report
uv run allure open allure-report
```

## Playwright Tracing

Genera una grabación completa del test (clicks, navigations, requests, console logs, DOM paso a paso) que se guarda automáticamente cuando un test falla. Se abre como timeline interactiva.

```bash
# Los traces se guardan solos en traces/ al fallar un test
uv run pytest

# Ver un trace
npx playwright show-trace traces/<nombre-del-test>.zip
```

## Test areas

Los tests siguen el patrón Page Object y están organizados por feature en `src/tests/`:

- `test_<feature>.py` — un archivo por funcionalidad (login, inventory, cart, checkout, etc.)
- Cada archivo contiene tests parametrizados para cubrir los diferentes casos
- Los tests nuevos se agregan en el archivo correspondiente sin necesidad de registrar nada

```bash
# Ver todos los tests disponibles (siempre actualizado)
uv run pytest --collect-only --quiet
```

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
