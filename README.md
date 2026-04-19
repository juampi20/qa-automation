# QA Automation - Sauce Demo

Framework de automatización de pruebas usando **Playwright** y **pytest** para la aplicación [SauceDemo](https://www.saucedemo.com).

## Características

- 🎭 **Playwright** - Automatización de navegador multi-navegador
- 🧪 **pytest** - Framework de testing
- 📊 **Allure** - Reportes de pruebas
- 📄 **Page Object Model** - Patrón de diseño escalable
- 🐍 **Python 3.12+** - Última versión de Python

## Requisitos

- [Python](https://www.python.org/) 3.12+
- [uv](https://docs.astral.sh/uv/) - Package manager

## Instalación

```bash
# Clonar el repositorio
git clone <repo-url>
cd qa-automation

# Instalar dependencias
uv sync
```

## Estructura del Proyecto

```
qa-automation/
├── src/
│   ├── pages/           # Page Object Model
│   │   ├── base_page.py
│   │   ├── ...
│   └── tests/           # Test cases
│       ├── test_login.py
│       └── ...
├── conftest.py          # Configuración de pytest
├── pyproject.toml       # Dependencias del proyecto
└── README.md
```

## Ejecución de Pruebas

### Ejecutar todos los tests
```bash
uv run pytest
```

### Ejecutar un archivo específico
```bash
uv run pytest ./src/tests/test_login.py -v
```

### Ejecutar un test específico
```bash
uv run pytest ./src/tests/test_login.py -k "test_login_valid" -v
```

### Ejecutar con ralentización (slowmo)
```bash
uv run pytest -v --headed --slowmo=1500
```

## Tests Disponibles

### Login Tests
- `test_login_valid` - Login exitoso con credenciales válidas
- `test_login_invalid_credentials` - Login fallido con credenciales inválidas
- `test_login_empty_fields` - Validación de campos vacíos

### Inventory Tests
- `test_add_one_item_to_cart` - Agregar un item al carrito
- `test_add_second_item_to_cart` - Agregar segundo item al carrito

## Credenciales de Prueba

| Usuario | Password | Estado |
|---------|----------|--------|
| standard_user | secret_sauce | ✅ Válido |
| locked_out_user | secret_sauce | 🔒 Bloqueado |
| problem_user | secret_sauce | ⚠️ Problemas |
| performance_glitch_user | secret_sauce | 🐢 Lento |

## Configuración

- **Timeout default**: 10.000ms
- **Viewport**: 1600x900
- **Navegador**: Chromium
- **Scope fixtures**: Function (test aislado)

## Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto es de código abierto bajo licencia MIT.

---

**Última actualización**: Abril 2026
**Desarrollado con ❤️ usando Playwright y pytest**
