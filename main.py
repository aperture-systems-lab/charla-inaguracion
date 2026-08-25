from manim import ManimColor
from manim_slides import Slide

from componentes import marco
from diapositivas import (
    SlideBase,
    SlidesCuerpo,
    SlidesFinal,
    SlidesInicio,
)
from estilo import FONDO


class presentation(
    SlidesInicio,
    SlidesCuerpo,
    SlidesFinal,
    SlideBase,
    Slide,
):
    skip_reversing = True

    def construct(self):
        self._slide_actual = 0
        self.camera.background_color = ManimColor(FONDO)
        self.marco = marco()
        self.add(self.marco)

        self.slide_pronto_iniciamos()
        self.slide_portada()
        self.slide_porque_aperture()
        self.slide_lineas()
        self.slide_reuniones()
        self.slide_proyecto()
        self.slide_cierre()
