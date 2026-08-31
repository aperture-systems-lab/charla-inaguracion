import numpy as np
from manim import (
    ORIGIN,
    PI,
    RIGHT,
    TAU,
    UP,
    Arc,
    Circle,
    Create,
    Dot,
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

from componentes import (
    ajustar_ancho,
    aro_iris,
    imagen,
    imagen_recortada,
    resplandor,
    texto,
)
from estilo import BLANCO, CLARO, FONT_TITULO, PRIMARIO, SECUNDARIO

CENTRO_QR = np.array([3.5, -0.35, 0.0])
CENTRO_ORBITA = np.array([-3.5, -0.5, 0.0])

ARO_RADIO = 1.72
ARO_GROSOR = 0.36
LADO_PAPEL = 2.05
MARGEN_QR = 0.14
ANCHO_RESPLANDOR = 3.4

HOLGURA_VISOR = 0.10
BRAZO_VISOR = 0.30
FOCO = 0.08

ANCHO_OJO = 1.35
ANCHO_HALO_OJO = 2.7
RADIOS_ORBITA = (0.95, 1.5, 2.05)
VUELTAS_ORBITA = (2, -1, 1)
FASES_ORBITA = (0.35, 2.2, 3.9)
RADIO_SATELITE = 0.085
ESTELA = ((0.0, 0.26, 0.60), (0.26, 0.58, 0.30), (0.58, 0.95, 0.13))

Y_GRACIAS = 3.0
Y_FIRMA = 2.4
Y_ROTULO = -3.35
RAYA_ROTULO = 0.55
ANCHO_COLUMNA = 4.7

VUELTA = 3.6
LATIDO_BASE = 0.5
LATIDO_SUBIDA = 0.5
LATIDO_OJO_BASE = 0.5
LATIDO_OJO_SUBIDA = 0.35


def _papel_qr():
    papel = RoundedRectangle(
        width=LADO_PAPEL, height=LADO_PAPEL, corner_radius=0.13,
        stroke_width=0,
    ).set_fill(BLANCO, opacity=1.0)
    papel.move_to(CENTRO_QR)
    codigo = imagen("qr_formulario.png")
    codigo.scale_to_fit_width(LADO_PAPEL - MARGEN_QR * 2)
    codigo.move_to(CENTRO_QR)
    return Group(papel, codigo)


def _visor(apertura):
    esquinas = VGroup()
    for signo_x in (-1, 1):
        for signo_y in (-1, 1):
            vertice = CENTRO_QR + np.array([
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
        CENTRO_QR + radio * np.array([np.cos(a), np.sin(a), 0.0])
        for a in [TAU * i / 6 - media for i in range(6)]
    ]
    return Polygon(*vertices, stroke_width=0)


def _rotulo():
    palabra = texto("ASISTENCIA", 18, color=PRIMARIO, font=FONT_TITULO)
    rayas = [
        Line(ORIGIN, RIGHT * RAYA_ROTULO, color=SECUNDARIO, stroke_width=2)
        .set_stroke(opacity=0.6)
        for _ in range(2)
    ]
    grupo = VGroup(rayas[0], palabra, rayas[1]).arrange(RIGHT, buff=0.3)
    ajustar_ancho(grupo, ANCHO_COLUMNA)
    return grupo.move_to(CENTRO_QR[0] * RIGHT + Y_ROTULO * UP)


def _orbitas():
    return VGroup(*[
        Circle(radius=radio, color=PRIMARIO, stroke_width=1.6)
        .set_stroke(opacity=0.3)
        .move_to(CENTRO_ORBITA)
        for radio in RADIOS_ORBITA
    ])


def _satelites(avance):
    grupo = VGroup()
    for radio, vueltas, fase in zip(RADIOS_ORBITA, VUELTAS_ORBITA, FASES_ORBITA):
        signo = np.sign(vueltas)
        angulo = fase + TAU * vueltas * avance
        for desde, hasta, opacidad in ESTELA:
            grupo.add(
                Arc(
                    radius=radio, arc_center=CENTRO_ORBITA,
                    start_angle=angulo - signo * hasta,
                    angle=signo * (hasta - desde),
                    color=PRIMARIO, stroke_width=3.2,
                ).set_stroke(opacity=opacidad)
            )
        grupo.add(Dot(
            CENTRO_ORBITA + radio * np.array([
                np.cos(angulo), np.sin(angulo), 0.0,
            ]),
            radius=RADIO_SATELITE, color=CLARO,
        ))
    return grupo


def construir(scene):
    gracias = texto("MUCHAS GRACIAS", 38, color=PRIMARIO, font=FONT_TITULO)
    gracias.move_to([0, Y_GRACIAS, 0])
    firma = texto("Aperture · Semillero de Data Science e IA", 17,
                  color=SECUNDARIO).move_to([0, Y_FIRMA, 0])

    halo_ojo = resplandor(ANCHO_HALO_OJO, fuerza=0.32).move_to(CENTRO_ORBITA)
    ojo = imagen_recortada("aperture-eye-cyan", ANCHO_OJO)
    ojo.move_to(CENTRO_ORBITA)
    orbitas = _orbitas()
    satelites = _satelites(0.0)

    halo = resplandor(ANCHO_RESPLANDOR, fuerza=0.4).move_to(CENTRO_QR)
    aro = aro_iris(0.0, ARO_GROSOR).move_to(CENTRO_QR)
    tarjeta_qr = _papel_qr()
    reposo_visor = LADO_PAPEL / 2 + HOLGURA_VISOR
    visor = _visor(reposo_visor)
    rotulo = _rotulo()

    scene.play(FadeIn(gracias, shift=UP * 0.18), run_time=0.7)
    scene.play(FadeIn(firma, shift=UP * 0.1), run_time=0.5)

    scene.add(halo_ojo)
    scene.play(FadeIn(ojo, scale=0.7), run_time=0.6)
    scene.play(
        LaggedStart(*[Create(o) for o in orbitas], lag_ratio=0.2),
        run_time=0.9,
    )
    scene.play(FadeIn(satelites, scale=0.6), run_time=0.5)

    abertura = ValueTracker(0.0)
    aro.add_updater(
        lambda m: m.become(
            aro_iris(abertura.get_value(), ARO_GROSOR).move_to(CENTRO_QR)
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
        FadeIn(rotulo[1], shift=UP * 0.1),
        Create(rotulo[0]),
        Create(rotulo[2]),
        run_time=0.6,
    )

    reloj = ValueTracker(0.0)
    halo.add_updater(lambda m: m.set_opacity(
        LATIDO_BASE + LATIDO_SUBIDA * np.sin(PI * reloj.get_value())
    ))
    halo_ojo.add_updater(lambda m: m.set_opacity(
        LATIDO_OJO_BASE + LATIDO_OJO_SUBIDA * np.sin(TAU * reloj.get_value())
    ))
    visor.add_updater(lambda m: m.become(
        _visor(reposo_visor + FOCO * np.sin(PI * reloj.get_value()))
    ))
    satelites.add_updater(lambda m: m.become(_satelites(reloj.get_value())))
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
    halo_ojo.clear_updaters()
    visor.clear_updaters()
    satelites.clear_updaters()
