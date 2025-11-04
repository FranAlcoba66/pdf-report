# fastapi-pdf-report

Este proyecto genera reportes PDF usando FastAPI y WeasyPrint.

## Usar Poetry (recomendado)

1) Instalar Poetry (si no lo tienes):

```bash
curl -sSL https://install.python-poetry.org | python3 -
# o sigue la guía oficial en https://python-poetry.org/docs/
```

2) Opcional: configurar el entorno virtual dentro del proyecto (recomendado):

```bash
poetry config virtualenvs.in-project true
```

3) Instalar dependencias del sistema (necesarias para WeasyPrint). En Debian/Ubuntu ejecuta:

```bash
sudo apt update
sudo apt install -y \
  libcairo2 \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libgdk-pixbuf2.0-0 \
  libffi-dev \
  shared-mime-info \
  libjpeg-dev \
  zlib1g-dev
```

WeasyPrint requiere bibliotecas nativas (C) como Cairo y Pango; si estás en otra distro o en macOS, consulta la doc oficial: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html

4) Instalar dependencias Python con Poetry:

```bash
poetry install
```

5) Ejecutar la aplicación:

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Notas

- `weasyprint` trae dependencias nativas; si `poetry install` falla, revisa el error y asegúrate de tener las librerías del sistema instaladas (lista anterior).
- Para producción, crea la `poetry.lock` en tu CI/localhost y usa `poetry export -f requirements.txt --without-hashes > requirements.txt` si tu despliegue necesita `pip`.

## Estructura

- `app/` contiene la aplicación FastAPI.
- `pyproject.toml` describe el proyecto y dependencias (Poetry).

