import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    LaggedStart,
    Line,
    Polygon,
    RoundedRectangle,
    Star,
    VGroup,
    VMobject,
)

from componentes import ajustar_ancho, aspa, panel, texto
from componentes import titulo as hacer_titulo
from estilo import (
    AMBAR,
    CLARO,
    COLOR_JERONIMO,
    COLOR_JOSE,
    COLOR_VALENTINA,
    FONT_TITULO,
    MORADO,
    PRIMARIO,
    ROJO,
    SECUNDARIO,
    VERDE,
)


ALTO_ICONO = 1.9
ANCHO_PROBLEMA = 4.3
ALTO_PROBLEMA = 3.7
X_PROBLEMAS = (-4.6, 0.0, 4.6)
Y_PROBLEMA = 0.1
DY_ICONO = 0.52
DY_ROTULO = -1.25
Y_REMATE = -2.5


PROBLEMAS = (
    ("Solo teoría", "examen", AMBAR),
    ("Sin dónde probar", "matraz", MORADO),
    ("Cada uno por su lado", "sueltos", VERDE),
)


FUNDADORES = (
    ("Valentina Muñoz", "Ingeniería Administrativa",
     COLOR_VALENTINA, "estrella"),
    ("Jose Miguel García", "Estadística", COLOR_JOSE, "curva"),
    ("Jerónimo Hoyos", "Ingeniería de Sistemas", COLOR_JERONIMO, "latido"),
)


PROFESORES = (
    ("María Constanza", "Torres Madroñero"),
    ("Francisco Javier", "Moreno Arboleda"),
    ("Jaime Alberto", "Guzmán Luna"),
)

ANCHO_FICHA = 4.3
ALTO_FICHA = 2.0
X_FICHAS = (-4.55, 0.0, 4.55)
Y_FICHAS = 1.85
RADIO_ARO = 0.4
DY_ARO = 0.42
DY_ETIQUETAS = -0.42


ALTO_FICHA_PROF = 1.5
Y_FICHAS_PROF = -0.75


def _dibujo_examen(color):
    hoja = RoundedRectangle(
        width=1.15, height=1.5, corner_radius=0.08,
        stroke_color=color, stroke_width=3.5,
    ).set_fill(color, opacity=0.06)
    renglones = VGroup(*[
        Line(LEFT * largo / 2, RIGHT * largo / 2, color=color,
             stroke_width=2.5, stroke_opacity=0.7).move_to([0, y, 0])
        for y, largo in (
            (0.46, 0.72), (0.23, 0.72), (0.0, 0.72),
            (-0.23, 0.72), (-0.46, 0.38),
        )
    ])
    tachon = aspa(ROJO, tam=0.24, grosor=6).move_to([0.6, -0.62, 0])
    return VGroup(hoja, renglones, tachon)


def _dibujo_matraz(color):
    silueta = VMobject(color=color, stroke_width=3.5)
    silueta.set_points_as_corners([
        np.array([-0.17, 0.86, 0]), np.array([-0.17, 0.34, 0]),
        np.array([-0.66, -0.7, 0]), np.array([0.66, -0.7, 0]),
        np.array([0.17, 0.34, 0]), np.array([0.17, 0.86, 0]),
    ])
    boca = Line(np.array([-0.25, 0.86, 0]), np.array([0.25, 0.86, 0]),
                color=color, stroke_width=3.5)
    caldo = Polygon(
        np.array([-0.45, -0.29, 0]), np.array([0.45, -0.29, 0]),
        np.array([0.66, -0.7, 0]), np.array([-0.66, -0.7, 0]),
        stroke_width=0,
    ).set_fill(color, opacity=0.22)
    burbujas = VGroup(
        Dot(np.array([-0.16, -0.05, 0]), radius=0.05, color=color),
        Dot(np.array([0.14, 0.13, 0]), radius=0.037, color=color),
    )
    tachon = aspa(ROJO, tam=0.24, grosor=6).move_to([0.64, 0.56, 0])
    return VGroup(silueta, boca, caldo, burbujas, tachon)


def _dibujo_sueltos(color):
    vertices = [
        np.array([0.0, 0.78, 0]),
        np.array([-0.76, -0.56, 0]),
        np.array([0.76, -0.56, 0]),
    ]
    trozos = VGroup()
    for i in range(3):
        for desde, hasta in ((i, (i + 1) % 3), ((i + 1) % 3, i)):
            recta = vertices[hasta] - vertices[desde]
            unidad = recta / np.linalg.norm(recta)
            trozos.add(Line(
                vertices[desde] + unidad * 0.22,
                vertices[desde] + unidad * 0.48,
                color=color, stroke_width=3, stroke_opacity=0.5,
            ))
    nodos = VGroup(*[Dot(v, radius=0.11, color=color) for v in vertices])
    return VGroup(trozos, nodos)


_DIBUJOS = {
    "examen": _dibujo_examen,
    "matraz": _dibujo_matraz,
    "sueltos": _dibujo_sueltos,
}


def _pizarra(color):
    tablero = RoundedRectangle(
        width=2.3, height=1.7, corner_radius=0.1,
        stroke_color=color, stroke_width=3.5,
    ).set_fill(color, opacity=0.05)
    formula = texto("f(x)", 34, color=color).move_to([0, 0.28, 0])
    tiza = VGroup(*[
        Line(LEFT * largo / 2, RIGHT * largo / 2, color=color,
             stroke_width=2.5, stroke_opacity=0.55).move_to([0, y, 0])
        for y, largo in ((-0.28, 1.3), (-0.55, 0.85))
    ])
    return VGroup(tablero, formula, tiza)


def _cubo(color):
    arriba = Polygon(
        np.array([0, 0.68, 0]), np.array([0.72, 0.32, 0]),
        np.array([0, -0.04, 0]), np.array([-0.72, 0.32, 0]),
        color=color, stroke_width=3,
    ).set_fill(color, opacity=0.28)
    izquierda = Polygon(
        np.array([-0.72, 0.32, 0]), np.array([0, -0.04, 0]),
        np.array([0, -0.78, 0]), np.array([-0.72, -0.42, 0]),
        color=color, stroke_width=3,
    ).set_fill(color, opacity=0.1)
    derecha = Polygon(
        np.array([0.72, 0.32, 0]), np.array([0, -0.04, 0]),
        np.array([0, -0.78, 0]), np.array([0.72, -0.42, 0]),
        color=color, stroke_width=3,
    ).set_fill(color, opacity=0.18)
    return VGroup(izquierda, derecha, arriba)


def _cifra_cien():
    cifra = texto("100%", 40, color=PRIMARIO, font=FONT_TITULO)
    barra = Line(UP * 0.34, DOWN * 0.34, color=PRIMARIO, stroke_width=4)
    glosa = texto("proyectos prácticos", 21, color=CLARO)
    dentro = VGroup(cifra, barra, glosa).arrange(RIGHT, buff=0.45)
    caja = panel(dentro.width + 1.0, dentro.height + 0.7)
    caja.move_to(dentro.get_center())
    return VGroup(caja, dentro)


def _emblema(clase, color):
    if clase == "estrella":
        return Star(n=5, outer_radius=0.24, inner_radius=0.103,
                    color=color, stroke_width=3.5)
    if clase == "curva":
        subida = VMobject(color=color, stroke_width=3.5)
        subida.set_points_as_corners([
            np.array([-0.29, -0.17, 0]), np.array([-0.07, 0.04, 0]),
            np.array([0.07, -0.07, 0]), np.array([0.29, 0.22, 0]),
        ])
        punta = VGroup(
            Line(np.array([0.29, 0.22, 0]), np.array([0.1, 0.22, 0]),
                 color=color, stroke_width=3.5),
            Line(np.array([0.29, 0.22, 0]), np.array([0.29, 0.03, 0]),
                 color=color, stroke_width=3.5),
        )
        return VGroup(subida, punta)
    latido = VMobject(color=color, stroke_width=3.5)
    latido.set_points_as_corners([
        np.array([-0.31, 0.0, 0]), np.array([-0.13, 0.0, 0]),
        np.array([-0.05, 0.24, 0]), np.array([0.04, -0.24, 0]),
        np.array([0.12, 0.0, 0]), np.array([0.31, 0.0, 0]),
    ])
    return latido


def _birrete(color):
    tabla = Polygon(
        np.array([0, 0.17, 0]), np.array([0.36, 0.01, 0]),
        np.array([0, -0.15, 0]), np.array([-0.36, 0.01, 0]),
        color=color, stroke_width=2.5,
    ).set_fill(color, opacity=0.25)
    casquete = VMobject(color=color, stroke_width=2.5)
    casquete.set_points_as_corners([
        np.array([-0.19, -0.06, 0]), np.array([-0.16, -0.26, 0]),
        np.array([0.16, -0.26, 0]), np.array([0.19, -0.06, 0]),
    ])
    borla = VGroup(
        Line(np.array([0.36, 0.01, 0]), np.array([0.36, -0.2, 0]),
             color=color, stroke_width=2.5),
        Dot(np.array([0.36, -0.24, 0]), radius=0.05, color=color),
    )
    return VGroup(tabla, casquete, borla)


def _ficha_profesor(lineas, x):
    centro = np.array([x, Y_FICHAS_PROF, 0.0])
    caja = panel(ANCHO_FICHA, ALTO_FICHA_PROF, color=SECUNDARIO,
                 opacidad=0.04, grosor=2)
    caja.move_to(centro)

    birrete = _birrete(PRIMARIO)
    birrete.scale_to_fit_height(0.62)
    birrete.move_to(centro + LEFT * (ANCHO_FICHA / 2 - 0.68))

    nombre = VGroup(*[
        texto(linea, 17, color=CLARO) for linea in lineas
    ]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    nombre.next_to(birrete, RIGHT, buff=0.34)

    return VGroup(caja, birrete, nombre)


def _rotulo_partido(contenido, largo=1.5):
    raya_izq = Line(LEFT * largo, RIGHT * 0, color=SECUNDARIO, stroke_width=2)
    raya_der = Line(LEFT * 0, RIGHT * largo, color=SECUNDARIO, stroke_width=2)
    for raya in (raya_izq, raya_der):
        raya.set_stroke(opacity=0.45)
    return VGroup(
        raya_izq, texto(contenido, 17, color=SECUNDARIO), raya_der,
    ).arrange(RIGHT, buff=0.35)


def _ficha_persona(nombre, carrera, color, clase, x):
    centro = np.array([x, Y_FICHAS, 0.0])
    util = ANCHO_FICHA - 0.7
    caja = panel(ANCHO_FICHA, ALTO_FICHA, color=color, opacidad=0.06)
    caja.move_to(centro)

    aro = Circle(radius=RADIO_ARO, color=color, stroke_width=3)
    aro.move_to(centro + UP * DY_ARO)
    emblema = _emblema(clase, color).move_to(aro.get_center())

    etiquetas = VGroup(
        ajustar_ancho(texto(nombre, 20, color=CLARO), util),
        ajustar_ancho(texto(carrera, 14, color=SECUNDARIO), util),
    ).arrange(DOWN, buff=0.13)
    etiquetas.move_to(centro + UP * DY_ETIQUETAS)

    return VGroup(caja, aro, emblema, etiquetas)


def construir(scene):
    encabezado = hacer_titulo("POR QUE CREAMOS EL SEMILLERO")
    entrada = texto("Aprender IA y datos en la carrera no siempre es fácil",
                    20, color=SECUNDARIO).move_to([0, 2.4, 0])

    cajas, dibujos, rotulos = VGroup(), VGroup(), VGroup()
    util = ANCHO_PROBLEMA - 0.5
    for (rotulo, clase, color), x in zip(PROBLEMAS, X_PROBLEMAS):
        centro = np.array([x, Y_PROBLEMA, 0.0])
        cajas.add(
            panel(ANCHO_PROBLEMA, ALTO_PROBLEMA, color=color, opacidad=0.05)
            .move_to(centro)
        )
        figura = _DIBUJOS[clase](color)
        figura.scale_to_fit_height(ALTO_ICONO)
        figura.move_to(centro + UP * DY_ICONO)
        dibujos.add(figura)
        rotulos.add(
            ajustar_ancho(texto(rotulo, 21, color=color), util)
            .move_to(centro + UP * DY_ROTULO)
        )

    remate = texto("Por eso creamos Aperture.", 26, color=PRIMARIO)
    remate.move_to([0, Y_REMATE, 0])

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(entrada, shift=UP * 0.12), run_time=0.5)
    for caja, figura, rotulo in zip(cajas, dibujos, rotulos):
        scene.play(FadeIn(caja, scale=0.92), run_time=0.4)
        scene.play(Create(figura), run_time=0.8)
        scene.play(FadeIn(rotulo, shift=UP * 0.1), run_time=0.35)
    scene.play(FadeIn(remate, shift=UP * 0.15), run_time=0.7)
    scene.next_slide()

    encabezado_meta = hacer_titulo("NUESTRA META")

    pizarra = _pizarra(SECUNDARIO)
    pizarra.scale_to_fit_height(2.0).move_to([-2.6, 0.85, 0])
    cubo = _cubo(PRIMARIO)
    cubo.scale_to_fit_height(2.0).move_to([2.6, 0.85, 0])
    flecha = Arrow(
        np.array([-1.15, 0.85, 0]), np.array([1.15, 0.85, 0]),
        color=PRIMARIO, stroke_width=5, buff=0.0,
        max_tip_length_to_length_ratio=0.22,
    )
    pie_pizarra = texto("teoría", 17, color=SECUNDARIO)
    pie_pizarra.move_to([-2.6, -0.55, 0])
    pie_cubo = texto("algo que funciona", 17, color=PRIMARIO)
    pie_cubo.move_to([2.6, -0.55, 0])

    meta = texto("Aprender construyendo.", 30, color=CLARO)
    meta.move_to([0, -1.65, 0])
    cien = _cifra_cien().move_to([0, -2.85, 0])

    scene.play(
        FadeOut(cajas), FadeOut(dibujos), FadeOut(rotulos),
        FadeOut(entrada), FadeOut(remate),
        FadeOut(encabezado), FadeIn(encabezado_meta, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(Create(pizarra), FadeIn(pie_pizarra), run_time=0.8)
    scene.play(Create(flecha), run_time=0.5)
    scene.play(Create(cubo), FadeIn(pie_cubo), run_time=0.9)
    scene.play(FadeIn(meta, shift=UP * 0.12), run_time=0.6)
    scene.play(FadeIn(cien, shift=UP * 0.12), run_time=0.6)
    scene.next_slide()

    encabezado_equipo = hacer_titulo("QUIENES ARRANCAMOS ESTO")
    fichas = VGroup(*[
        _ficha_persona(nombre, carrera, color, clase, x)
        for (nombre, carrera, color, clase), x in zip(FUNDADORES, X_FICHAS)
    ])

    rotulo_prof = _rotulo_partido("Nos acompañan").move_to([0, 0.35, 0])
    fichas_prof = VGroup(*[
        _ficha_profesor(lineas, x)
        for lineas, x in zip(PROFESORES, X_FICHAS)
    ])

    grupo_dentro = VGroup(
        texto("Grupo de investigación", 14, color=SECUNDARIO),
        texto("SINTELWEB · Sistemas Inteligentes Web", 19, color=PRIMARIO),
    ).arrange(DOWN, buff=0.14)
    grupo_caja = panel(grupo_dentro.width + 0.9, grupo_dentro.height + 0.55)
    grupo_caja.move_to(grupo_dentro.get_center())
    sintelweb = VGroup(grupo_caja, grupo_dentro).move_to([0, -2.55, 0])

    scene.play(
        FadeOut(VGroup(pizarra, flecha, cubo, pie_pizarra, pie_cubo,
                       meta, cien)),
        FadeOut(encabezado_meta),
        FadeIn(encabezado_equipo, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(
        LaggedStart(*[FadeIn(f, shift=UP * 0.18) for f in fichas],
                    lag_ratio=0.35),
        run_time=1.6,
    )
    scene.play(FadeIn(rotulo_prof), run_time=0.4)
    scene.play(
        LaggedStart(*[FadeIn(f, shift=UP * 0.14) for f in fichas_prof],
                    lag_ratio=0.3),
        run_time=1.3,
    )
    scene.play(FadeIn(sintelweb, shift=UP * 0.12), run_time=0.6)
    scene.wait(0.4)

    scene.next_slide()
