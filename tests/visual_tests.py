#!/usr/bin/env python

"""
Visual regression tests for pivy.visual_test.

The suite keeps references as generated image files and verifies perceptual
similarity scores. This is intentionally not pixel-by-pixel matching.
"""

import os
import tempfile
import unittest

from pivy import coin
from pivy.visual_test import VisualTester

try:
    from PIL import Image  # noqa: F401
    _HAS_PILLOW = True
except ImportError:
    _HAS_PILLOW = False


@unittest.skipUnless(_HAS_PILLOW, "Pillow is required for visual tests")
class VisualRegressionTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory(prefix="pivy-visual-tests-")
        self.tester = VisualTester(
            width=320,
            height=240,
            background=(1.0, 1.0, 1.0),
        )

    def tearDown(self):
        self.tmpdir.cleanup()

    def _path(self, name):
        return os.path.join(self.tmpdir.name, name)

    def _make_scene(self, shape="cube", color=(0.8, 0.2, 0.2), x_shift=0.0):
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

    def _write_reference(self, scene, filename="reference.png"):
        reference_path = self._path(filename)
        self.tester.run(scene=scene, output_path=reference_path)
        self.assertTrue(os.path.isfile(reference_path))
        return reference_path

    def test_01_render_scene_object_writes_png(self):
        output_path = self._path("render.png")
        result = self.tester.run(scene=self._make_scene(), output_path=output_path)

        self.assertTrue(os.path.isfile(output_path))
        self.assertEqual(result.output_path, output_path)
        self.assertIsNone(result.similarity_percent)

    def test_02_identical_scene_has_high_similarity(self):
        reference_path = self._write_reference(self._make_scene(), "same_reference.png")
        result = self.tester.run(scene=self._make_scene(), reference=reference_path)

        self.assertGreaterEqual(result.similarity_percent, 99.0)
        self.assertGreaterEqual(result.hash_similarity_percent, 99.0)

    def test_03_shifted_scene_has_lower_similarity(self):
        reference_path = self._write_reference(self._make_scene(), "shift_reference.png")
        shifted_scene = self._make_scene(x_shift=2.6)
        result = self.tester.run(scene=shifted_scene, reference=reference_path)

        self.assertLess(result.similarity_percent, 97.0)

    def test_04_different_shape_has_lower_similarity(self):
        reference_path = self._write_reference(self._make_scene(shape="cube"), "shape_ref.png")
        result = self.tester.run(
            scene=self._make_scene(shape="cone"),
            reference=reference_path,
        )

        self.assertLess(result.similarity_percent, 97.0)

    def test_05_scene_path_input_is_supported(self):
        iv_path = self._path("scene.iv")
        with open(iv_path, "w", encoding="utf-8") as handle:
            handle.write(
                "#Inventor V2.1 ascii\n"
                "Separator {\n"
                "  OrthographicCamera {\n"
                "    position 0 0 5\n"
                "    nearDistance 0.5\n"
                "    farDistance 20\n"
                "    height 4\n"
                "  }\n"
                "  DirectionalLight { }\n"
                "  Material {\n"
                "    diffuseColor 0.8 0.2 0.2\n"
                "    specularColor 0.05 0.05 0.05\n"
                "    shininess 0.1\n"
                "  }\n"
                "  Cube { width 2 height 2 depth 2 }\n"
                "}\n"
            )

        reference_path = self._write_reference(self._make_scene(shape="cube"), "path_ref.png")
        result = self.tester.run(scene_path=iv_path, reference=reference_path)

        self.assertGreaterEqual(result.similarity_percent, 99.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
