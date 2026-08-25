from manim import UP, FadeIn, FadeOut

from componentes import logo_esquina, red_decorativa

from . import (
    cierre,
    lineas,
    porque_aperture,
    portada,
    pronto_iniciamos,
    proyecto,
    reuniones,
)


class SlideBase:
    def indicador(self):
        if getattr(self, "_indicador", None) is None:
            self._indicador = logo_esquina()
        return self._indicador

    def next_slide(self, *args, indicador=True, **kwargs):
        if not indicador:
            super().next_slide(*args, **kwargs)
            return
        logo = self.indicador()
        self.play(FadeIn(logo, shift=UP * 0.1), run_time=0.3)
        super().next_slide(*args, **kwargs)
        self.remove(logo)

    def iniciar_slide(self):
        self._slide_actual = getattr(self, "_slide_actual", 0) + 1
        marco = getattr(self, "marco", None)
        fondo_viejo = getattr(self, "_fondo", None)
        resto = [m for m in self.mobjects if m is not marco and m is not fondo_viejo]
        for m in resto:
            m.clear_updaters()

        self._fondo = red_decorativa(self._slide_actual - 1)
        salidas = [FadeOut(m) for m in resto]
        if fondo_viejo is not None:
            salidas.append(FadeOut(fondo_viejo))
        self.play(*salidas, FadeIn(self._fondo))
        if marco is not None:
            self.add(marco)


def _slide(construir):
    def metodo(self):
        self.iniciar_slide()
        construir(self)

    return metodo


class SlidesInicio:
    slide_pronto_iniciamos = _slide(pronto_iniciamos.construir)
    slide_portada = _slide(portada.construir)


class SlidesCuerpo:
    slide_porque_aperture = _slide(porque_aperture.construir)
    slide_lineas = _slide(lineas.construir)
    slide_reuniones = _slide(reuniones.construir)
    slide_proyecto = _slide(proyecto.construir)


class SlidesFinal:
    slide_cierre = _slide(cierre.construir)
