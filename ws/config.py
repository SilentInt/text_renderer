import os
from pathlib import Path

from text_renderer.effect import *
from text_renderer.corpus import *
from text_renderer.config import (
    RenderCfg,
    NormPerspectiveTransformCfg,
    GeneratorCfg,
    FixedTextColorCfg,
    FixedPerspectiveTransformCfg,
    # SimpleTextColorCfg,
)

CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))


def story_data():
    return GeneratorCfg(
        num_image=30000,
        save_dir=CURRENT_DIR / "output",
        render_cfg=RenderCfg(
            bg_dir=CURRENT_DIR / "bg",
            height=100,
            gray=True,
            text_color_cfg=FixedTextColorCfg(),
            perspective_transform=NormPerspectiveTransformCfg(20, 20, 20),
            # perspective_transform=FixedPerspectiveTransformCfg(30, 30, 1.5),
            corpus=WordCorpus(
                WordCorpusCfg(
                    text_paths=[CURRENT_DIR / "corpus" / "text.txt"],
                    font_dir=CURRENT_DIR / "font",
                    font_size=(20, 40),
                    num_word=(1, 1),
                    text_color_cfg=FixedTextColorCfg(),
                ),
            ),
            corpus_effects=Effects([
                # Padding(p=0.5, w_ratio=[0, 2],
                #         h_ratio=[0, 0.3], center=True),
                # Line(0.5, thickness=(1, 1)),
                DropoutRand(p=0.9, dropout_p=(0.0, 0.7)),
            ]),
        ),
    )


configs = [
    story_data()
]
