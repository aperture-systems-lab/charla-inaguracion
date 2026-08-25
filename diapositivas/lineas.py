import numpy as np
from manim import (
    BOLD,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circle,
    Create,
    Dot,
    FadeIn,
    Line,
    Polygon,
    Rectangle,
    RoundedRectangle,
    VGroup,
)

from componentes import ajustar_ancho, panel, texto
from componentes import titulo as hacer_titulo
from estilo import (
    AMBAR,
    CLARO,
    MORADO,
    PRIMARIO,
    SECUNDARIO,
    SUPERFICIE,
)

ANCHO_LINEA = 4.3
ALTO_LINEA = 4.4
Y_LINEA = -0.6
X_LINEAS = (-4.55, 0.0, 4.55)

MARGEN_TEXTO = 0.5
ALTO_EMBLEMA = 2.2
DY_EMBLEMA = 0.85
DY_NOMBRE = -1.25


LINEAS = (
    (("Data Science", "y Machine Learning"), PRIMARIO, "datos"),
    (("IA y Sistemas", "Inteligentes"), AMBAR, "red"),
    (("High Performance", "Computing"), MORADO, "chip"),
)


IZQ, DER, ABAJO, ARRIBA = -1.0, 1.0, -0.76, 0.76


PENDIENTE, CORTE = 0.6, 0.0


def _ajuste(x):
    return PENDIENTE * x + CORTE


def _emblema_datos(color):
    guias = VGroup(*[
        Line(np.array([IZQ, y, 0]), np.array([DER, y, 0]),
             color=SECUNDARIO, stroke_width=1.2, stroke_opacity=0.14)
        for y in np.linspace(ABAJO, ARRIBA, 5)[1:-1]
    ])
    ejes = VGroup(
        Line(np.array([IZQ, ABAJO, 0]), np.array([IZQ, ARRIBA, 0]),
             color=SECUNDARIO, stroke_width=2.5, stroke_opacity=0.5),
        Line(np.array([IZQ, ABAJO, 0]), np.array([DER, ABAJO, 0]),
             color=SECUNDARIO, stroke_width=2.5, stroke_opacity=0.5),
    )

    borde_x = np.linspace(-0.92, 0.96, 9)
    ancho = 0.08 + 0.08 * (np.abs(borde_x) / 0.96) ** 2
    banda = Polygon(
        *[np.array([x, _ajuste(x) + a, 0]) for x, a in zip(borde_x, ancho)],
        *[np.array([x, _ajuste(x) - a, 0])
          for x, a in zip(borde_x[::-1], ancho[::-1])],
        stroke_width=0,
    ).set_fill(color, opacity=0.16)

    recta = Line(
        np.array([-0.92, _ajuste(-0.92), 0]),
        np.array([0.96, _ajuste(0.96), 0]),
        color=CLARO, stroke_width=4,
    )

    desvios = np.random.default_rng(11).uniform(-0.13, 0.13, 8)
    nube = VGroup(*[
        Dot(np.array([x, _ajuste(x) + d, 0]), radius=0.077, color=color)
        for x, d in zip(np.linspace(-0.8, 0.88, 8), desvios)
    ])
    return VGroup(guias, ejes, banda, recta, nube)


def _emblema_red(color):
    capas = (2, 4, 4, 2)
    columnas = np.linspace(-0.95, 0.95, len(capas))

    paso = 0.42
    centros = [
        [
            np.array([x, (i - (cuantos - 1) / 2) * paso, 0])
            for i in range(cuantos)
        ]
        for x, cuantos in zip(columnas, capas)
    ]
    aristas = VGroup(*[
        Line(origen, destino, color=color,
             stroke_width=1.3, stroke_opacity=0.22)
        for izquierda, derecha in zip(centros, centros[1:])
        for origen in izquierda for destino in derecha
    ])
    nodos = VGroup(*[
        Circle(radius=0.16, color=color, stroke_width=3.5)
        .set_fill(SUPERFICIE, opacity=1.0).move_to(centro)
        for capa in centros for centro in capa
    ])
    return VGroup(aristas, nodos)


def _emblema_chip(color):
    lado = 1.5
    cuerpo = RoundedRectangle(
        width=lado, height=lado, corner_radius=0.12,
        stroke_color=color, stroke_width=3,
    ).set_fill(color, opacity=0.08)

    patillas = VGroup()
    for direccion in (UP, DOWN, LEFT, RIGHT):
        a_lo_largo = np.array([direccion[1], direccion[0], 0.0])
        for paso in np.linspace(-0.42, 0.42, 4):
            arranque = direccion * (lado / 2) + a_lo_largo * paso
            patillas.add(Line(
                arranque, arranque + direccion * 0.16,
                color=color, stroke_width=2.5,
            ))

    oblea = RoundedRectangle(
        width=lado * 0.72, height=lado * 0.72, corner_radius=0.05,
        stroke_color=color, stroke_width=2, stroke_opacity=0.7,
    ).set_fill(color, opacity=0.08)

    hueco = lado * 0.72 / 3.4
    nucleos = VGroup(*[
        RoundedRectangle(
            width=hueco * 0.72, height=hueco * 0.72, corner_radius=0.03,
            stroke_width=0,
        )
        .set_fill(color, opacity=0.82 if (fila, col) == (1, 1) else 0.34)
        .move_to(np.array([(col - 1) * hueco, (fila - 1) * hueco, 0]))
        for fila in range(3) for col in range(3)
    ])
    return VGroup(patillas, cuerpo, oblea, nucleos)


_EMBLEMAS = {
    "datos": _emblema_datos,
    "red": _emblema_red,
    "chip": _emblema_chip,
}


def _rotulo(nombre, color, ancho):
    lineas = VGroup(*[
        ajustar_ancho(texto(linea, 20, color=color, weight=BOLD), ancho - 0.5)
        for linea in nombre
    ]).arrange(DOWN, buff=0.13)
    fondo = RoundedRectangle(
        corner_radius=0.1, width=ancho, height=lineas.height + 0.5,
        stroke_width=0,
    ).set_fill(color, opacity=0.2)
    barra = Rectangle(width=ancho, height=0.075, stroke_width=0)
    barra.set_fill(color, opacity=1.0)
    barra.next_to(fondo, UP, buff=0.12)
    return VGroup(barra, fondo, lineas.move_to(fondo.get_center()))


def _columna(nombre, color, clase, x):
    centro = np.array([x, Y_LINEA, 0.0])
    util = ANCHO_LINEA - MARGEN_TEXTO * 2

    caja = panel(ANCHO_LINEA, ALTO_LINEA, color=color, opacidad=0.05)
    caja.move_to(centro)

    emblema = _EMBLEMAS[clase](color)
    emblema.scale_to_fit_height(ALTO_EMBLEMA)
    ajustar_ancho(emblema, util)
    emblema.move_to(centro + UP * DY_EMBLEMA)

    titular = _rotulo(nombre, color, util)
    titular.move_to(centro + UP * DY_NOMBRE)

    return caja, emblema, titular


def construir(scene):
    encabezado = hacer_titulo("LINEAS DE ESTUDIO")
    entradilla = texto("Las tres áreas de trabajo que tendremos", 19,
                       color=SECUNDARIO).move_to([0, 2.4, 0])

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(entradilla, shift=UP * 0.12), run_time=0.5)
    scene.next_slide()

    for (nombre, color, clase), x in zip(LINEAS, X_LINEAS):
        caja, emblema, titular = _columna(nombre, color, clase, x)
        scene.play(FadeIn(caja, scale=0.92), run_time=0.45)
        scene.play(Create(emblema), run_time=1.1)
        scene.play(FadeIn(titular, scale=0.9), run_time=0.5)
        scene.next_slide()
