import numpy as np
from manim import (
    BOLD,
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Arc,
    Arrow,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Flash,
    LaggedStart,
    Line,
    Polygon,
    RoundedRectangle,
    VGroup,
)

from componentes import ajustar_ancho, panel, tarjeta, texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, PRIMARIO, SECUNDARIO, VERDE

ANCHO_PARADA = 4.0
ALTO_PARADA = 3.4
Y_PARADA = -0.1
X_PARADAS = (-4.6, 0.0, 4.6)

MARGEN_TEXTO = 0.55
DY_EMBLEMA = 0.9
DY_NOMBRE = 0.15
DY_RAYA = -0.12
DY_CUERPO = -0.85


PARADAS = (
    ("El reto", PRIMARIO, "diana", (
        "Un problema de datos",
        "e IA para resolver",
        "durante el semestre.",
    )),
    ("La asesoría", VERDE, "brujula", (
        "Acompañamiento de",
        "los miembros del",
        "semillero.",
    )),
    ("El premio", AMBAR, "copa", (
        "Habrá premio para el",
        "mejor proyecto del",
        "semillero.",
    )),
)


def _emblema_diana(color):
    aros = VGroup(*[
        Circle(radius=r, color=color, stroke_width=3)
        for r in (0.52, 0.34, 0.16)
    ])
    return VGroup(aros, Dot(radius=0.07, color=color))


def _emblema_brujula(color):
    aro = Circle(radius=0.5, color=color, stroke_width=3)
    marcas = VGroup(*[
        Line(
            np.array([np.cos(a), np.sin(a), 0]) * 0.5,
            np.array([np.cos(a), np.sin(a), 0]) * 0.36,
            color=color, stroke_width=2.5, stroke_opacity=0.7,
        )
        for a in (PI / 2, 0.0, -PI / 2, PI)
    ])

    norte = Polygon(
        np.array([0.0, 0.34, 0]), np.array([0.13, 0.0, 0]),
        np.array([-0.13, 0.0, 0]), color=color, stroke_width=2.5,
    ).set_fill(color, opacity=0.8)
    sur = Polygon(
        np.array([0.0, -0.34, 0]), np.array([0.13, 0.0, 0]),
        np.array([-0.13, 0.0, 0]), color=color, stroke_width=2.5,
    ).set_fill(color, opacity=0.1)
    aguja = VGroup(sur, norte).rotate(-0.42)
    return VGroup(aro, marcas, aguja)


def _emblema_copa(color):
    cuenco = Polygon(
        np.array([-0.34, 0.46, 0]), np.array([0.34, 0.46, 0]),
        np.array([0.26, 0.06, 0]), np.array([0.13, -0.10, 0]),
        np.array([-0.13, -0.10, 0]), np.array([-0.26, 0.06, 0]),
        color=color, stroke_width=3,
    ).set_fill(color, opacity=0.18)
    asas = VGroup(
        Arc(radius=0.17, start_angle=PI / 2, angle=-PI,
            arc_center=np.array([0.36, 0.28, 0]),
            color=color, stroke_width=3),
        Arc(radius=0.17, start_angle=PI / 2, angle=PI,
            arc_center=np.array([-0.36, 0.28, 0]),
            color=color, stroke_width=3),
    )
    pie = Line(np.array([0.0, -0.10, 0]), np.array([0.0, -0.32, 0]),
               color=color, stroke_width=4)
    peana = RoundedRectangle(
        width=0.52, height=0.13, corner_radius=0.04,
        stroke_color=color, stroke_width=3,
    ).set_fill(color, opacity=0.18).move_to(np.array([0.0, -0.39, 0]))
    return VGroup(cuenco, asas, pie, peana)


_EMBLEMAS = {
    "diana": _emblema_diana,
    "brujula": _emblema_brujula,
    "copa": _emblema_copa,
}


def _parada(nombre, color, clase, renglones, x):
    centro = np.array([x, Y_PARADA, 0.0])
    util = ANCHO_PARADA - MARGEN_TEXTO * 2

    caja = panel(ANCHO_PARADA, ALTO_PARADA, color=color, opacidad=0.05)
    caja.move_to(centro)

    emblema = _EMBLEMAS[clase](color).move_to(centro + UP * DY_EMBLEMA)

    titular = ajustar_ancho(texto(nombre, 22, color=color), util)
    titular.move_to(centro + UP * DY_NOMBRE)

    raya = Line(LEFT * (util / 2), RIGHT * (util / 2),
                color=color, stroke_width=2).set_stroke(opacity=0.5)
    raya.move_to(centro + UP * DY_RAYA)

    cuerpo = VGroup(*[
        ajustar_ancho(texto(linea, 14, color=CLARO), util)
        for linea in renglones
    ]).arrange(DOWN, buff=0.22)
    cuerpo.move_to(centro + UP * DY_CUERPO)

    return caja, emblema, titular, raya, cuerpo


def _flecha(x_desde, x_hasta):
    return Arrow(
        np.array([x_desde, Y_PARADA, 0.0]),
        np.array([x_hasta, Y_PARADA, 0.0]),
        color=SECUNDARIO, stroke_width=4, buff=0.0,
        max_tip_length_to_length_ratio=0.4,
    )


def _chispas(centro, color):
    posiciones = ((-0.85, 0.55), (0.85, 0.5), (-0.7, -0.45), (0.78, -0.3))
    return VGroup(*[
        Dot(centro + np.array([dx, dy, 0.0]), radius=0.055, color=color)
        for dx, dy in posiciones
    ])


def construir(scene):
    encabezado = hacer_titulo("EL PROYECTO PRACTICO")
    entradilla = texto("Todo el semillero desemboca en construir algo", 19,
                       color=SECUNDARIO).move_to([0, 2.42, 0])

    remate = tarjeta([("Aprender construyendo", 21, BOLD)])
    remate.move_to([0, -2.6, 0])
    coletilla = texto(
        "proyectos reales de IA y datos, en equipo y con impacto social",
        16, color=SECUNDARIO,
    ).move_to([0, -3.35, 0])

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(entradilla, shift=UP * 0.12), run_time=0.5)

    borde = ANCHO_PARADA / 2
    for i, ((nombre, color, clase, renglones), x) in enumerate(
        zip(PARADAS, X_PARADAS)
    ):
        if i:
            scene.play(
                Create(_flecha(X_PARADAS[i - 1] + borde + 0.12, x - borde - 0.12)),
                run_time=0.4,
            )
        caja, emblema, titular, raya, cuerpo = _parada(
            nombre, color, clase, renglones, x
        )
        scene.play(FadeIn(caja, scale=0.92), run_time=0.4)
        scene.play(Create(emblema), run_time=0.7)
        scene.play(FadeIn(titular, shift=UP * 0.1), Create(raya), run_time=0.45)
        scene.play(
            LaggedStart(*[FadeIn(li, shift=RIGHT * 0.12) for li in cuerpo],
                        lag_ratio=0.25),
            run_time=0.8,
        )
        if clase == "copa":
            centro_copa = emblema.get_center()
            chispas = _chispas(centro_copa, color)
            scene.play(
                Flash(centro_copa, color=color, line_length=0.25,
                      num_lines=16, flash_radius=0.8),
                LaggedStart(*[FadeIn(c, scale=0.3) for c in chispas],
                            lag_ratio=0.15),
                run_time=0.7,
            )

            scene.play(
                LaggedStart(*[FadeOut(c, scale=1.8) for c in chispas],
                            lag_ratio=0.12),
                run_time=0.55,
            )

    scene.next_slide()

    scene.play(FadeIn(remate, scale=0.88), run_time=0.6)
    scene.play(FadeIn(coletilla, shift=UP * 0.1), run_time=0.5)
    scene.wait(0.4)

    scene.next_slide()
