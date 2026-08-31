# Inauguración del Semillero Aperture

Presentación animada de la sesión inaugural del **Semillero de Data Science e
IA — Aperture**, hecha con [Manim Slides](https://manim-slides.eertmans.be/).

## Requisitos

- Python ≥ 3.13 (ver [.python-version](.python-version))
- [uv](https://docs.astral.sh/uv/) para gestionar el entorno y las dependencias

## Uso

```bash
# Instalación de librerías
uv sync

# Renderizar la presentación 
uv run python -m manim_slides render main.py presentation

# Renderizar rápido
uv run python -m manim_slides render -ql main.py presentation

# Presentar
uv run python -m manim_slides present presentation
```

