import numpy as np
from manim import (
    DOWN,
    TAU,
    UP,
    Arc,
    Circle,
    Create,
    Dot,
    FadeIn,
    Flash,
    Group,
    LaggedStart,
    ValueTracker,
    VGroup,
    rate_functions,
)

from componentes import (
    IRIS_ABIERTO,
    imagen_recortada,
    iris,
    resplandor,
    separador,
    texto,
)
from estilo import CLARO, FONT_TITULO, PRIMARIO, SECUNDARIO, SUPERFICIE

ANCHO_NOMBRE = 7.4

CENTRO_LOGO = np.array([0.0, 1.75, 0.0])
RADIO_BOLA = 0.9
ANCHO_OJO = 1.18
ANCHO_RESPLANDOR = 3.6


ARO_DENTRO = (1.14, 3, 0.5, 3.5)
ARO_FUERA = (1.38, 2, 0.75, 2.5)

Y_NOMBRE = -0.45
Y_RAYA = -1.12
Y_LINEA_MARCA = -1.7
Y_LEMA = -2.65

GIRO_APERTURA = 0.52
VUELTA = 4.6
ALETEO = 0.13


def _flote(reloj):
    return UP * ALETEO * np.sin(TAU * reloj)


def _aro(radio, tramos, hueco, grosor, giro, color, centro):
    paso = TAU / tramos
    aro = VGroup()
    for i in range(tramos):
        arranque = giro + i * paso + hueco / 2
        aro.add(Arc(
            radius=radio, start_angle=arranque, angle=paso - hueco,
            arc_center=centro, color=color, stroke_width=grosor,
        ))
        aro.add(Dot(
            centro + radio * np.array([
                np.cos(arranque), np.sin(arranque), 0.0,
            ]),
            radius=0.045, color=color,
        ))
    return aro


def construir(scene):
    halo = resplandor(ANCHO_RESPLANDOR, fuerza=0.3).move_to(CENTRO_LOGO)
    bola = Circle(radius=RADIO_BOLA, color=PRIMARIO, stroke_width=4)
    bola.set_fill(SUPERFICIE, opacity=1.0).move_to(CENTRO_LOGO)
    ojo = imagen_recortada("aperture-eye-cyan", ANCHO_OJO)
    ojo.move_to(CENTRO_LOGO)

    nucleo = Group(halo, bola, ojo)

    nombre = texto("APERTURE", 60, color=PRIMARIO, font=FONT_TITULO)
    nombre.scale_to_fit_width(ANCHO_NOMBRE).move_to([0, Y_NOMBRE, 0])

    raya = separador(largo=3.7, grosor=3).move_to([0, Y_RAYA, 0])

    linea_marca = texto("SEMILLERO DE DATA SCIENCE E IA", 22, color=CLARO)
    linea_marca.move_to([0, Y_LINEA_MARCA, 0])

    lema = VGroup(
        texto("No solo estudiamos la IA.", 19, color=SECUNDARIO),
        texto("La construimos y la llevamos a la realidad.", 19, color=SECUNDARIO),
    ).arrange(DOWN, buff=0.18).move_to([0, Y_LEMA, 0])

    revelado = Group(nucleo, nombre, linea_marca)

    hojas = iris(0.0)
    scene.play(FadeIn(hojas), run_time=0.5)

    scene.add(revelado)
    scene.add(hojas)
    scene.wait(0.35)

    abertura = ValueTracker(0.0)
    giro_hojas = ValueTracker(0.0)
    hojas.add_updater(
        lambda m: m.become(iris(abertura.get_value(), giro_hojas.get_value()))
    )
    scene.play(
        abertura.animate.set_value(IRIS_ABIERTO),
        giro_hojas.animate.set_value(GIRO_APERTURA),
        run_time=2.0,
        rate_func=rate_functions.ease_in_out_sine,
    )
    hojas.clear_updaters()
    scene.remove(hojas)

    scene.play(
        Flash(CENTRO_LOGO, color=PRIMARIO, line_length=0.3, num_lines=18,
              flash_radius=RADIO_BOLA + 0.35, run_time=0.6),
    )

    aro_dentro = _aro(*ARO_DENTRO, 0.0, PRIMARIO, CENTRO_LOGO)
    aro_fuera = _aro(*ARO_FUERA, 0.0, SECUNDARIO, CENTRO_LOGO)
    scene.play(
        LaggedStart(Create(aro_dentro), Create(aro_fuera), lag_ratio=0.35),
        run_time=1.1,
    )

    scene.play(Create(raya), run_time=0.5)
    scene.play(FadeIn(lema, shift=UP * 0.12), run_time=0.7)

    reloj = ValueTracker(0.0)
    aro_dentro.add_updater(
        lambda m: m.become(_aro(
            *ARO_DENTRO, reloj.get_value() * TAU / ARO_DENTRO[1], PRIMARIO,
            CENTRO_LOGO + _flote(reloj.get_value()),
        ))
    )
    aro_fuera.add_updater(
        lambda m: m.become(_aro(
            *ARO_FUERA, -reloj.get_value() * TAU / ARO_FUERA[1], SECUNDARIO,
            CENTRO_LOGO + _flote(reloj.get_value()),
        ))
    )

    nucleo.add_updater(
        lambda m: m.move_to(CENTRO_LOGO + _flote(reloj.get_value()))
    )

    if hasattr(scene, "_base_slide_config"):
        scene._base_slide_config.auto_next = True
    scene.next_slide(loop=True, indicador=False)

    scene.play(
        reloj.animate.set_value(1.0),
        run_time=VUELTA,
        rate_func=rate_functions.linear,
    )

    scene.next_slide(indicador=False)
    nucleo.clear_updaters()
    aro_dentro.clear_updaters()
    aro_fuera.clear_updaters()
