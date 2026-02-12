#!/usr/bin/env python

"""
Generate baseline images for tests/visual_tests.py.
"""

import argparse
import os
import shutil

# Prefer a GLX mode that works reliably with Xvfb in CI.
os.environ.setdefault("COIN_GLXGLUE_NO_PBUFFERS", "1")
os.environ.setdefault("COIN_GLX_PIXMAP_DIRECT_RENDERING", "1")

from pivy import coin
from pivy.visual_test import VisualTester


def make_scene(shape="cube", color=(0.8, 0.2, 0.2), x_shift=0.0):
    root = coin.SoSeparator()

    camera = coin.SoOrthographicCamera()
    camera.position = (0.0, 0.0, 5.0)
    camera.nearDistance = 0.5
    camera.farDistance = 20.0
    camera.height = 4.0
    root.addChild(camera)
    root.addChild(coin.SoDirectionalLight())

    translation = coin.SoTranslation()
    translation.translation = (x_shift, 0.0, 0.0)
    root.addChild(translation)

    material = coin.SoMaterial()
    material.diffuseColor = color
    material.specularColor = (0.05, 0.05, 0.05)
    material.shininess = 0.1
    root.addChild(material)

    if shape == "cube":
        node = coin.SoCube()
        node.width = 2.0
        node.height = 2.0
        node.depth = 2.0
    elif shape == "sphere":
        node = coin.SoSphere()
        node.radius = 1.2
    elif shape == "cone":
        node = coin.SoCone()
        node.bottomRadius = 1.4
        node.height = 2.4
    else:
        raise ValueError("Unknown shape: {0}".format(shape))

    root.addChild(node)
    return root


def main():
    parser = argparse.ArgumentParser(description="Generate visual test baseline images.")
    parser.add_argument(
        "--output-dir",
        default=os.path.join(os.path.dirname(__file__), "visual_references"),
        help="Directory where baseline PNG files are written.",
    )
    args = parser.parse_args()

    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    tester = VisualTester(width=320, height=240, background=(1.0, 1.0, 1.0))

    references = [
        ("cube_scene.png", {"scene": make_scene(shape="cube")}),
        ("shifted_scene.png", {"scene": make_scene(shape="cube", x_shift=2.6)}),
        ("cone_scene.png", {"scene": make_scene(shape="cone")}),
        ("sphere_scene.png", {"scene": make_scene(shape="sphere")}),
    ]

    for filename, payload in references:
        target = os.path.join(output_dir, filename)
        tester.run(output_path=target, **payload)
        print("wrote", target)

    # Keep a dedicated baseline filename for scene_path checks.
    source = os.path.join(output_dir, "cube_scene.png")
    target = os.path.join(output_dir, "path_scene.png")
    shutil.copyfile(source, target)
    print("wrote", target)


if __name__ == "__main__":
    main()
