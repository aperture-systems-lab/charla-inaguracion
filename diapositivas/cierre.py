import numpy as np
from manim import (
    PI,
    TAU,
    UP,
    Create,
    FadeIn,
    Group,
    LaggedStart,
    Line,
    Polygon,
    RoundedRectangle,
    ShowPassingFlash,
    ValueTracker,
    VGroup,
    rate_functions,
)

from componentes import aro_iris, imagen, resplandor, texto
from estilo import BLANCO, CLARO, FONT_TITULO, PRIMARIO, SECUNDARIO

CENTRO = np.array([0.0, -0.35, 0.0])


ARO_RADIO = 1.62
ARO_GROSOR = 0.34
LADO_PAPEL = 1.9
MARGEN_QR = 0.13
ANCHO_RESPLANDOR = 3.1

HOLGURA_VISOR = 0.09
BRAZO_VISOR = 0.28
FOCO = 0.07

Y_GRACIAS = 3.0
Y_FIRMA = 2.4
Y_ROTULO = -2.95
Y_DETALLE = -3.42

VUELTA = 3.6
LATIDO_BASE = 0.5
LATIDO_SUBIDA = 0.5


def _papel_qr():
    papel = RoundedRectangle(
        width=LADO_PAPEL, height=LADO_PAPEL, corner_radius=0.13,
        stroke_width=0,
    ).set_fill(BLANCO, opacity=1.0)
    papel.move_to(CENTRO)
    codigo = imagen("qr_links.png")
    codigo.scale_to_fit_width(LADO_PAPEL - MARGEN_QR * 2)
    codigo.move_to(CENTRO)
    return Group(papel, codigo)


def _visor(apertura):
    esquinas = VGroup()
    for signo_x in (-1, 1):
        for signo_y in (-1, 1):
            vertice = CENTRO + np.array([
                signo_x * apertura, signo_y * apertura, 0.0,
            ])
            esquinas.add(
                Line(vertice, vertice + np.array([-signo_x * BRAZO_VISOR, 0, 0]),
                     color=PRIMARIO, stroke_width=4),
                Line(vertice, vertice + np.array([0, -signo_y * BRAZO_VISOR, 0]),
                     color=PRIMARIO, stroke_width=4),
            )
    return esquinas


def _contorno():
    media = TAU / 12
    radio = (ARO_RADIO + ARO_GROSOR) / np.cos(media)
    vertices = [
        CENTRO + radio * np.array([np.cos(a), np.sin(a), 0.0])
        for a in [TAU * i / 6 - media for i in range(6)]
    ]
    return Polygon(*vertices, stroke_width=0)


def construir(scene):
    gracias = texto("MUCHAS GRACIAS", 38, color=PRIMARIO, font=FONT_TITULO)
    gracias.move_to([0, Y_GRACIAS, 0])
    firma = texto("Aperture · Semillero de Data Science e IA", 17,
                  color=SECUNDARIO).move_to([0, Y_FIRMA, 0])

    halo = resplandor(ANCHO_RESPLANDOR, fuerza=0.4).move_to(CENTRO)
    aro = aro_iris(0.0, ARO_GROSOR).move_to(CENTRO)
    tarjeta_qr = _papel_qr()
    reposo_visor = LADO_PAPEL / 2 + HOLGURA_VISOR
    visor = _visor(reposo_visor)

    rotulo = texto("Todos los enlaces del semillero", 20, color=CLARO)
    rotulo.move_to([0, Y_ROTULO, 0])
    detalle = texto("web · GitHub · Instagram · correo", 15, color=SECUNDARIO)
    detalle.move_to([0, Y_DETALLE, 0])

    scene.play(FadeIn(gracias, shift=UP * 0.18), run_time=0.7)
    scene.play(FadeIn(firma, shift=UP * 0.1), run_time=0.5)

    abertura = ValueTracker(0.0)
    aro.add_updater(
        lambda m: m.become(
            aro_iris(abertura.get_value(), ARO_GROSOR).move_to(CENTRO)
        )
    )
    scene.add(halo, aro)
    scene.play(
        abertura.animate.set_value(ARO_RADIO),
        run_time=1.0,
        rate_func=rate_functions.ease_out_cubic,
    )
    aro.clear_updaters()

    scene.play(FadeIn(tarjeta_qr, scale=0.85), run_time=0.6)

    scene.play(
        LaggedStart(*[Create(brazo) for brazo in visor], lag_ratio=0.08),
        run_time=0.7,
    )
    scene.play(
        FadeIn(rotulo, shift=UP * 0.1),
        FadeIn(detalle, shift=UP * 0.08),
        run_time=0.6,
    )

    reloj = ValueTracker(0.0)
    halo.add_updater(lambda m: m.set_opacity(
        LATIDO_BASE + LATIDO_SUBIDA * np.sin(PI * reloj.get_value())
    ))
    visor.add_updater(lambda m: m.become(
        _visor(reposo_visor + FOCO * np.sin(PI * reloj.get_value()))
    ))
    if hasattr(scene, "_base_slide_config"):
        scene._base_slide_config.auto_next = True
    scene.next_slide(loop=True, indicador=False)

    scene.play(
        reloj.animate.set_value(1.0),
        ShowPassingFlash(
            _contorno().set_stroke(CLARO, width=6, opacity=1.0),
            time_width=0.22,
        ),
        run_time=VUELTA,
        rate_func=rate_functions.linear,
    )

    scene.next_slide(indicador=False)
    halo.clear_updaters()
    visor.clear_updaters()
