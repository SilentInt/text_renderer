import os
from pathlib import Path

from text_renderer.effect import *
from text_renderer.corpus import *
from text_renderer.config import (
    RenderCfg,
    NormPerspectiveTransformCfg,
    GeneratorCfg,
    FixedTextColorCfg,
    # SimpleTextColorCfg,
)

CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))


def story_data():
    return GeneratorCfg(
        num_image=3000,
        save_dir=CURRENT_DIR / "output",
        render_cfg=RenderCfg(
            bg_dir=CURRENT_DIR / "bg",
            height=600,
            gray=False,
            text_color_cfg=FixedTextColorCfg(),
            perspective_transform=NormPerspectiveTransformCfg(20, 20, 1.5),
            corpus=WordCorpus(
                WordCorpusCfg(
                    text_paths=[CURRENT_DIR / "corpus" / "text.txt"],
                    font_dir=CURRENT_DIR / "font",
                    font_size=(100, 210),
                    num_word=(1, 1),
                ),
            ),
            corpus_effects=Effects([
                Padding(p=1, w_ratio=[8, 8],
                        h_ratio=[4, 4], center=False),
                # Line(0.9, thickness=(2, 5)),
                # DropoutRand(p=1, dropout_p=(0.0, 0.2)),
            ]),
            # text_color_cfg=SimpleTextColorCfg(),
        ),
    )


configs = [story_data()]
