#!/usr/bin/env python3

"""
Render Inventor scenes offscreen and run perceptual visual comparisons.

Examples:
  Save render only:
    python3 -m pivy.visual_test scene.iv --output render.png

  Compare with baseline and print similarity in percent:
    python3 -m pivy.visual_test scene.iv --reference baseline.png

  Save render and compare:
    python3 -m pivy.visual_test scene.iv --output render.png --reference baseline.png

Python API:
  from pivy.visual_test import VisualTester
  from pivy.coin import SoSeparator, SoCube

  root = SoSeparator()
  root.addChild(SoCube())

  tester = VisualTester(width=800, height=600, background=(1.0, 1.0, 1.0))
  result = tester.run(scene=root, output_path="render.png")
  print(result.similarity_percent)
"""

import argparse
import math
import os
import sys

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from PIL import Image
except ImportError:
    Image = None

from pivy.coin import (
    SbColor,
    SbViewportRegion,
    SoCamera,
    SoDB,
    SoDirectionalLight,
    SoInput,
    SoLight,
    SoOffscreenRenderer,
    SoPerspectiveCamera,
    SoSearchAction,
    SoSeparator,
)

__all__ = [
    "VisualTestResult",
    "VisualTester",
    "compare_images",
    "compare_images_detailed",
    "load_scene",
    "render_scene",
    "run_visual_test",
]


if hasattr(Image, "Resampling"):
    _RESAMPLE_LANCZOS = Image.Resampling.LANCZOS
else:
    _RESAMPLE_LANCZOS = Image.LANCZOS if Image is not None else None


class VisualTestResult:
    """Result object returned by VisualTester.run()."""

    __slots__ = (
        "output_path",
        "similarity_percent",
        "hash_similarity_percent",
        "color_similarity_percent",
        "threshold",
        "passed",
    )

    def __init__(
        self,
        output_path=None,
        similarity_percent=None,
        hash_similarity_percent=None,
        color_similarity_percent=None,
        threshold=None,
        passed=None,
    ):
        self.output_path = output_path
        self.similarity_percent = similarity_percent
        self.hash_similarity_percent = hash_similarity_percent
        self.color_similarity_percent = color_similarity_percent
        self.threshold = threshold
        self.passed = passed

    def as_dict(self):
        return {
            "output_path": self.output_path,
            "similarity_percent": self.similarity_percent,
            "hash_similarity_percent": self.hash_similarity_percent,
            "color_similarity_percent": self.color_similarity_percent,
            "threshold": self.threshold,
            "passed": self.passed,
        }

    def __repr__(self):
        return (
            "VisualTestResult("
            "output_path={0!r}, "
            "similarity_percent={1!r}, "
            "hash_similarity_percent={2!r}, "
            "color_similarity_percent={3!r}, "
            "threshold={4!r}, "
            "passed={5!r})"
        ).format(
            self.output_path,
            self.similarity_percent,
            self.hash_similarity_percent,
            self.color_similarity_percent,
            self.threshold,
            self.passed,
        )


def _validate_dimensions(width, height):
    if int(width) <= 0 or int(height) <= 0:
        raise ValueError("width und height muessen > 0 sein.")


def _validate_background(background):
    if len(background) != 3:
        raise ValueError("background muss genau 3 Werte enthalten (R, G, B).")

    normalized = []
    for value in background:
        channel = float(value)
        if channel < 0.0 or channel > 1.0:
            raise ValueError("background Werte muessen im Bereich [0..1] liegen.")
        normalized.append(channel)
    return tuple(normalized)


def _normalize_weights(hash_weight, color_weight):
    hash_weight = float(hash_weight)
    color_weight = float(color_weight)
    if hash_weight < 0.0 or color_weight < 0.0:
        raise ValueError("Gewichte muessen >= 0 sein.")

    total = hash_weight + color_weight
    if total <= 0.0:
        raise ValueError("Mindestens eines der Gewichte muss > 0 sein.")
    return hash_weight / total, color_weight / total


def _require_pillow():
    if Image is None:
        raise RuntimeError(
            "Pillow ist nicht installiert. Bitte zuerst installieren: pip install pillow"
        )


def load_scene(scene_path):
    scene_path = os.fspath(scene_path)
    so_input = SoInput()
    if not so_input.openFile(scene_path):
        raise RuntimeError("Konnte Scene-Datei nicht oeffnen: {0}".format(scene_path))

    root = SoDB.readAll(so_input)
    if root is None:
        raise RuntimeError("Konnte Scene-Datei nicht lesen: {0}".format(scene_path))
    return root


def _resolve_scene_input(scene=None, scene_path=None):
    if scene is not None and scene_path is not None:
        raise ValueError("Bitte entweder scene oder scene_path angeben, nicht beides.")
    if scene is None and scene_path is None:
        raise ValueError("Bitte scene oder scene_path angeben.")

    if scene is not None:
        if not hasattr(scene, "isOfType"):
            raise TypeError(
                "scene muss ein Coin-Node Objekt sein (z.B. SoSeparator), "
                "oder scene_path verwenden."
            )
        return scene

    return load_scene(scene_path)


def _scene_has_type(root, type_id):
    search = SoSearchAction()
    search.setInterest(SoSearchAction.FIRST)
    search.setType(type_id)
    search.apply(root)
    return search.getPath() is not None


def _prepare_scene(root, viewport):
    render_root = SoSeparator()
    has_camera = _scene_has_type(root, SoCamera.getClassTypeId())
    has_light = _scene_has_type(root, SoLight.getClassTypeId())

    camera = None
    if not has_camera:
        camera = SoPerspectiveCamera()
        render_root.addChild(camera)

    if not has_light:
        render_root.addChild(SoDirectionalLight())

    render_root.addChild(root)

    if camera is not None:
        camera.viewAll(render_root, viewport)

    return render_root


def _render_scene(scene_root, width, height, background):
    viewport = SbViewportRegion(width, height)
    renderer = SoOffscreenRenderer(viewport)
    renderer.setBackgroundColor(SbColor(*background))

    render_root = _prepare_scene(scene_root, viewport)
    if not renderer.render(render_root):
        raise RuntimeError("Offscreen-Rendering ist fehlgeschlagen")

    image_buffer = bytes(renderer.getBuffer())
    components = int(renderer.getComponents())
    return image_buffer, components


def _buffer_to_image(image_buffer, width, height, components):
    _require_pillow()

    expected = width * height * components
    if len(image_buffer) != expected:
        raise RuntimeError(
            "Unerwartete Buffer-Laenge: erhalten={0}, erwartet={1}".format(
                len(image_buffer), expected
            )
        )

    if components == 1:
        image = Image.frombytes("L", (width, height), image_buffer)
    elif components == 2:
        image = Image.frombytes("LA", (width, height), image_buffer).convert("RGB")
    elif components == 3:
        image = Image.frombytes("RGB", (width, height), image_buffer)
    elif components == 4:
        image = Image.frombytes("RGBA", (width, height), image_buffer)
    else:
        raise RuntimeError("Nicht unterstuetzte Anzahl Komponenten: {0}".format(components))

    # OpenGL buffers are usually bottom-up, image files are top-down.
    return image.transpose(Image.FLIP_TOP_BOTTOM)


def _coerce_to_image(image_or_path):
    _require_pillow()

    if hasattr(image_or_path, "convert"):
        return image_or_path.convert("RGB")

    if isinstance(image_or_path, (str, os.PathLike)):
        with Image.open(image_or_path) as loaded:
            return loaded.convert("RGB")

    raise TypeError(
        "reference muss ein Bildobjekt oder ein Dateipfad sein (str / os.PathLike)."
    )


def _save_image(image, output_path):
    output_path = os.fspath(output_path)
    output_dir = os.path.dirname(os.path.abspath(output_path))
    if output_dir and not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    image.save(output_path)


def _dhash_bits(image, hash_size=16):
    grayscale = image.convert("L").resize((hash_size + 1, hash_size), _RESAMPLE_LANCZOS)
    pixels = list(grayscale.getdata())
    bits = []
    row_stride = hash_size + 1

    for row in range(hash_size):
        base = row * row_stride
        for col in range(hash_size):
            left = pixels[base + col]
            right = pixels[base + col + 1]
            bits.append(1 if left > right else 0)
    return bits


def _histogram_hsv(image, h_bins=12, s_bins=4, v_bins=4):
    hsv = image.convert("HSV")
    histogram = [0] * (h_bins * s_bins * v_bins)

    for h, s, v in hsv.getdata():
        h_idx = min(h_bins - 1, (h * h_bins) // 256)
        s_idx = min(s_bins - 1, (s * s_bins) // 256)
        v_idx = min(v_bins - 1, (v * v_bins) // 256)
        index = (h_idx * s_bins + s_idx) * v_bins + v_idx
        histogram[index] += 1

    total = float(max(1, image.width * image.height))
    return [count / total for count in histogram]


def _hamming_similarity(bits_a, bits_b):
    if len(bits_a) != len(bits_b):
        raise RuntimeError("Interner Fehler: Hash-Laengen stimmen nicht ueberein")
    if not bits_a:
        return 0.0
    distance = sum(1 for a, b in zip(bits_a, bits_b) if a != b)
    return 1.0 - (float(distance) / float(len(bits_a)))


def _bhattacharyya_similarity(hist_a, hist_b):
    if len(hist_a) != len(hist_b):
        raise RuntimeError("Interner Fehler: Histogramm-Laengen stimmen nicht ueberein")
    return sum(math.sqrt(a * b) for a, b in zip(hist_a, hist_b))


def compare_images_detailed(
    rendered_image,
    reference_image,
    hash_weight=0.7,
    color_weight=0.3,
):
    """Return a detailed perceptual comparison as percentages."""
    _require_pillow()
    hash_weight, color_weight = _normalize_weights(hash_weight, color_weight)

    rendered_rgb = rendered_image.convert("RGB")
    reference_rgb = reference_image.convert("RGB")

    hash_similarity = _hamming_similarity(
        _dhash_bits(rendered_rgb), _dhash_bits(reference_rgb)
    )
    color_similarity = _bhattacharyya_similarity(
        _histogram_hsv(rendered_rgb), _histogram_hsv(reference_rgb)
    )

    # Combined perceptual score (not pixel-by-pixel matching).
    score = (hash_weight * hash_similarity) + (color_weight * color_similarity)
    score = max(0.0, min(1.0, score))
    return {
        "similarity_percent": score * 100.0,
        "hash_similarity_percent": hash_similarity * 100.0,
        "color_similarity_percent": color_similarity * 100.0,
    }


def compare_images(rendered_image, reference_image):
    """Backward-compatible: return only combined similarity percent."""
    return compare_images_detailed(rendered_image, reference_image)["similarity_percent"]


class VisualTester:
    """
    High-level API for offscreen rendering and perceptual comparison.

    Example:
        tester = VisualTester(width=1280, height=720)
        result = tester.run(scene=my_scene, reference="baseline.png", output_path="actual.png")
        print(result.similarity_percent)
    """

    def __init__(
        self,
        width=1024,
        height=768,
        background=(0.0, 0.0, 0.0),
        hash_weight=0.7,
        color_weight=0.3,
    ):
        _validate_dimensions(width, height)
        self.width = int(width)
        self.height = int(height)
        self.background = _validate_background(background)
        self.hash_weight, self.color_weight = _normalize_weights(
            hash_weight, color_weight
        )

    def render(self, scene=None, scene_path=None):
        """
        Render a scene to a PIL image.

        Use one of:
          - scene: a Coin scene node (SoNode / SoSeparator / ...)
          - scene_path: path to an Inventor file
        """
        scene_root = _resolve_scene_input(scene=scene, scene_path=scene_path)
        image_buffer, components = _render_scene(
            scene_root, self.width, self.height, self.background
        )
        return _buffer_to_image(image_buffer, self.width, self.height, components)

    def compare(self, rendered_image, reference):
        """
        Compare a rendered image against a reference.

        reference can be:
          - a file path
          - a PIL image object
        """
        reference_image = _coerce_to_image(reference)
        return compare_images_detailed(
            rendered_image,
            reference_image,
            hash_weight=self.hash_weight,
            color_weight=self.color_weight,
        )

    def run(
        self,
        scene=None,
        scene_path=None,
        output_path=None,
        reference=None,
        threshold=None,
    ):
        """
        Render scene, optionally save image, optionally compare against reference.
        """
        if threshold is not None:
            threshold = float(threshold)
            if threshold < 0.0 or threshold > 100.0:
                raise ValueError("threshold muss im Bereich [0..100] liegen.")
            if reference is None:
                raise ValueError("threshold erfordert auch eine reference.")

        rendered_image = self.render(scene=scene, scene_path=scene_path)

        saved_output_path = None
        if output_path:
            saved_output_path = os.fspath(output_path)
            _save_image(rendered_image, saved_output_path)

        similarity_percent = None
        hash_similarity_percent = None
        color_similarity_percent = None
        if reference is not None:
            details = self.compare(rendered_image, reference)
            similarity_percent = details["similarity_percent"]
            hash_similarity_percent = details["hash_similarity_percent"]
            color_similarity_percent = details["color_similarity_percent"]

        passed = None
        if threshold is not None:
            passed = similarity_percent >= threshold

        return VisualTestResult(
            output_path=saved_output_path,
            similarity_percent=similarity_percent,
            hash_similarity_percent=hash_similarity_percent,
            color_similarity_percent=color_similarity_percent,
            threshold=threshold,
            passed=passed,
        )


def render_scene(
    scene=None,
    scene_path=None,
    width=1024,
    height=768,
    background=(0.0, 0.0, 0.0),
):
    """Convenience function returning a rendered PIL image."""
    tester = VisualTester(width=width, height=height, background=background)
    return tester.render(scene=scene, scene_path=scene_path)


def run_visual_test(
    scene=None,
    scene_path=None,
    output_path=None,
    reference=None,
    width=1024,
    height=768,
    background=(0.0, 0.0, 0.0),
    threshold=None,
    hash_weight=0.7,
    color_weight=0.3,
):
    """
    Convenience end-to-end function for rendering and optional comparison.
    """
    tester = VisualTester(
        width=width,
        height=height,
        background=background,
        hash_weight=hash_weight,
        color_weight=color_weight,
    )
    return tester.run(
        scene=scene,
        scene_path=scene_path,
        output_path=output_path,
        reference=reference,
        threshold=threshold,
    )


def _parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Scene offscreen rendern und visuell vergleichen (prozentual)."
    )
    parser.add_argument("scene", help="Pfad zur Scene-Datei (z.B. .iv)")
    parser.add_argument(
        "--output",
        "-o",
        help="Pfad fuer das gerenderte Bild (z.B. render.png)",
    )
    parser.add_argument(
        "--reference",
        "-r",
        help="Pfad zum Referenzbild fuer den Vergleich",
    )
    parser.add_argument("--width", type=int, default=1024, help="Render-Breite")
    parser.add_argument("--height", type=int, default=768, help="Render-Hoehe")
    parser.add_argument(
        "--background",
        nargs=3,
        type=float,
        metavar=("R", "G", "B"),
        default=(0.0, 0.0, 0.0),
        help="Hintergrundfarbe als 3 Floats in [0..1], z.B. --background 1 1 1",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        help="Optionaler Mindestwert in Prozent fuer CI (Exitcode 2 wenn unterschritten)",
    )
    args = parser.parse_args(argv)

    if not args.output and not args.reference:
        parser.error("Bitte mindestens --output oder --reference angeben.")

    if args.width <= 0 or args.height <= 0:
        parser.error("--width und --height muessen > 0 sein.")

    for channel in args.background:
        if channel < 0.0 or channel > 1.0:
            parser.error("--background Werte muessen im Bereich [0..1] liegen.")

    if args.threshold is not None and (args.threshold < 0.0 or args.threshold > 100.0):
        parser.error("--threshold muss im Bereich [0..100] liegen.")

    return args


def main(argv=None):
    args = _parse_args(argv if argv is not None else sys.argv[1:])

    try:
        result = run_visual_test(
            scene_path=args.scene,
            output_path=args.output,
            reference=args.reference,
            width=args.width,
            height=args.height,
            background=tuple(args.background),
            threshold=args.threshold,
        )

        if result.output_path:
            print("Render gespeichert: {0}".format(result.output_path))

        if result.similarity_percent is not None:
            print("Aehnlichkeit: {0:.2f}%".format(result.similarity_percent))

        if result.passed is False:
            print(
                "Aehnlichkeit unter Threshold ({0:.2f}% < {1:.2f}%)".format(
                    result.similarity_percent, result.threshold
                ),
                file=sys.stderr,
            )
            return 2
        return 0
    except Exception as exc:
        print("Fehler: {0}".format(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
