import numpy as np
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    TAU,
    UP,
    Arc,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Flash,
    LaggedStart,
    Line,
    ValueTracker,
    VGroup,
    rate_functions,
)

from componentes import separador, texto, vinetas
from componentes import titulo as hacer_titulo
from estilo import CLARO, FONT_TITULO, PRIMARIO, SECUNDARIO

CENTRO_RELOJ = np.array([3.75, 0.75, 0.0])
RADIO = 1.6
RADIO_ARCO = 1.42
LARGO_AGUJA = 1.24

X_IZQ = -6.4
Y_PIPS = -1.85
DIAS = 7
DIA_ENCENDIDO = 3

CLAVES = (
    "Charlas de cada área.",
    "Invitados especiales.",
    "Charlas prácticas.",
)


def _esfera():
    aro = Circle(radius=RADIO, color=PRIMARIO, stroke_width=4)
    aro.move_to(CENTRO_RELOJ)
    marcas = VGroup()
    for i in range(12):
        angulo = PI / 2 - i * TAU / 12
        u = np.array([np.cos(angulo), np.sin(angulo), 0.0])
        cardinal = i % 3 == 0
        marcas.add(Line(
            CENTRO_RELOJ + u * (RADIO - (0.26 if cardinal else 0.15)),
            CENTRO_RELOJ + u * (RADIO - 0.04),
            color=PRIMARIO if cardinal else SECUNDARIO,
            stroke_width=4 if cardinal else 2,
            stroke_opacity=1.0 if cardinal else 0.6,
        ))
    return VGroup(aro, marcas)


def _aguja(fraccion):
    angulo = PI / 2 - fraccion * TAU
    punta = CENTRO_RELOJ + LARGO_AGUJA * np.array([
        np.cos(angulo), np.sin(angulo), 0.0,
    ])
    return Line(CENTRO_RELOJ, punta, color=CLARO, stroke_width=5)


def _arco(fraccion):
    return Arc(
        radius=RADIO_ARCO,
        start_angle=PI / 2,
        angle=-max(fraccion, 1e-3) * TAU,
        arc_center=CENTRO_RELOJ,
        color=PRIMARIO,
        stroke_width=7,
    )


def _semana():
    puntos = VGroup()
    for i in range(DIAS):
        encendido = i == DIA_ENCENDIDO
        puntos.add(Dot(
            radius=0.13 if encendido else 0.085,
            color=PRIMARIO if encendido else SECUNDARIO,
            fill_opacity=1.0 if encendido else 0.35,
        ))
    puntos.arrange(RIGHT, buff=0.34)
    puntos.move_to(CENTRO_RELOJ + DOWN * (CENTRO_RELOJ[1] - Y_PIPS))
    return puntos


def construir(scene):
    encabezado = hacer_titulo("REUNIONES SEMANALES")

    cifra = texto("1 SESION", 40, color=PRIMARIO, font=FONT_TITULO)
    cifra.move_to([X_IZQ, 1.35, 0], aligned_edge=LEFT)
    apellido = texto("a la semana", 24, color=CLARO)
    apellido.move_to([X_IZQ + 0.1, 0.62, 0], aligned_edge=LEFT)
    raya = separador(largo=1.5, grosor=3)
    raya.move_to([X_IZQ, 0.15, 0], aligned_edge=LEFT)
    claves = vinetas(CLAVES, tam=17, buff=0.45)
    claves.move_to([X_IZQ, -1.25, 0], aligned_edge=LEFT)

    esfera = _esfera()
    aguja = _aguja(0.0)
    arco = _arco(0.0).set_stroke(opacity=0.0)
    eje = Dot(CENTRO_RELOJ, radius=0.075, color=PRIMARIO)
    semana = _semana()

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(Create(esfera), run_time=0.9)
    scene.play(FadeIn(eje), Create(aguja), run_time=0.5)
    scene.play(FadeIn(cifra, shift=UP * 0.15), run_time=0.6)
    scene.play(FadeIn(apellido, shift=UP * 0.1), Create(raya), run_time=0.5)
    scene.play(
        LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in claves],
                    lag_ratio=0.35),
        run_time=1.2,
    )
    scene.play(
        LaggedStart(*[FadeIn(p, scale=0.6) for p in semana], lag_ratio=0.12),
        run_time=0.9,
    )

    vuelta = ValueTracker(0.0)
    scene.add(arco)
    aguja.add_updater(lambda m: m.become(_aguja(vuelta.get_value())))
    arco.add_updater(lambda m: m.become(_arco(vuelta.get_value())))

    if hasattr(scene, "_base_slide_config"):
        scene._base_slide_config.auto_next = True
    scene.next_slide(loop=True, indicador=False)

    scene.play(
        vuelta.animate.set_value(1.0),
        run_time=2.6,
        rate_func=rate_functions.linear,
    )
    scene.play(Flash(CENTRO_RELOJ + UP * RADIO_ARCO, color=PRIMARIO,
                     line_length=0.18, num_lines=12, flash_radius=0.3),
               run_time=0.4)

    arco.clear_updaters()
    scene.play(FadeOut(arco), run_time=0.45)

    scene.next_slide(indicador=False)
    aguja.clear_updaters()
