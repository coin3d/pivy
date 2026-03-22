#!/usr/bin/env python

"""
Visual regression tests for pivy.visual_test.

The suite keeps references as generated image files and verifies perceptual
similarity scores. This is intentionally not pixel-by-pixel matching.
"""

import os
import sys
import tempfile
import unittest

coin = None
VisualTester = None
BASELINE_DIR = os.path.join(os.path.dirname(__file__), "visual_references")
BASELINES = {
    "cube": "cube_scene.png",
    "shifted": "shifted_scene.png",
    "cone": "cone_scene.png",
    "sphere": "sphere_scene.png",
    "path": "path_scene.png",
}

try:
    from PIL import Image  # noqa: F401
    _HAS_PILLOW = True
except ImportError:
    _HAS_PILLOW = False


class VisualRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not _HAS_PILLOW:
            raise unittest.SkipTest("Pillow is required for visual tests")

        # GLX options for when a display is present (e.g. Xvfb); no DISPLAY required.
        os.environ.setdefault("COIN_GLXGLUE_NO_PBUFFERS", "1")
        os.environ.setdefault("COIN_GLX_PIXMAP_DIRECT_RENDERING", "1")

        global coin, VisualTester
        from pivy import coin as coin_module
        from pivy.visual_test import VisualTester as visual_tester_class

        coin = coin_module
        VisualTester = visual_tester_class

        available, reason = cls._probe_offscreen_renderer()
        if not available:
            raise unittest.SkipTest(
                "Offscreen renderer not available in this environment: {0}".format(reason)
            )

        missing = [
            filename
            for filename in BASELINES.values()
            if not os.path.isfile(os.path.join(BASELINE_DIR, filename))
        ]
        if missing:
            raise RuntimeError(
                "Missing visual reference images: {0}. "
                "Run tests/generate_visual_references.py".format(", ".join(missing))
            )

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

    def _reference_path(self, key):
        return os.path.join(BASELINE_DIR, BASELINES[key])

    @staticmethod
    def _make_scene(shape="cube", color=(0.8, 0.2, 0.2), x_shift=0.0):
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

    @classmethod
    def _probe_offscreen_renderer(cls):
        tester = VisualTester(width=64, height=64, background=(1.0, 1.0, 1.0))
        try:
            tester.run(scene=cls._make_scene())
        except Exception as exc:
            return False, str(exc)
        return True, ""

    def test_01_render_scene_object_writes_png(self):
        output_path = self._path("render.png")
        result = self.tester.run(
            scene=self._make_scene(),
            output_path=output_path,
            reference=self._reference_path("cube"),
        )

        self.assertTrue(os.path.isfile(output_path))
        self.assertEqual(result.output_path, output_path)
        self.assertGreaterEqual(result.similarity_percent, 98.0)

    def test_02_identical_scene_has_high_similarity(self):
        result = self.tester.run(
            scene=self._make_scene(),
            reference=self._reference_path("cube"),
        )

        self.assertGreaterEqual(result.similarity_percent, 99.0)
        self.assertGreaterEqual(result.hash_similarity_percent, 99.0)

    def test_03_shifted_scene_has_lower_similarity(self):
        shifted_scene = self._make_scene(x_shift=2.6)
        result = self.tester.run(
            scene=shifted_scene,
            reference=self._reference_path("cube"),
        )
        shifted_reference_result = self.tester.run(
            scene=shifted_scene,
            reference=self._reference_path("shifted"),
        )

        self.assertLess(result.similarity_percent, 97.0)
        self.assertGreaterEqual(shifted_reference_result.similarity_percent, 99.0)

    def test_04_different_shape_has_lower_similarity(self):
        result_against_cube = self.tester.run(
            scene=self._make_scene(shape="cone"),
            reference=self._reference_path("cube"),
        )
        result_against_cone = self.tester.run(
            scene=self._make_scene(shape="cone"),
            reference=self._reference_path("cone"),
        )

        self.assertLess(result_against_cube.similarity_percent, 97.0)
        self.assertGreaterEqual(result_against_cone.similarity_percent, 99.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
