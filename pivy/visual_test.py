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


if hasattr(Image, "Resampling"):
    _RESAMPLE_LANCZOS = Image.Resampling.LANCZOS
else:
    _RESAMPLE_LANCZOS = Image.LANCZOS if Image is not None else None


def _require_pillow():
    if Image is None:
        raise RuntimeError(
            "Pillow ist nicht installiert. Bitte zuerst installieren: pip install pillow"
        )


def _load_scene(scene_path):
    so_input = SoInput()
    if not so_input.openFile(scene_path):
        raise RuntimeError("Konnte Scene-Datei nicht oeffnen: {0}".format(scene_path))

    root = SoDB.readAll(so_input)
    if root is None:
        raise RuntimeError("Konnte Scene-Datei nicht lesen: {0}".format(scene_path))
    return root


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


def compare_images(rendered_image, reference_image):
    rendered_rgb = rendered_image.convert("RGB")
    reference_rgb = reference_image.convert("RGB")

    hash_similarity = _hamming_similarity(
        _dhash_bits(rendered_rgb), _dhash_bits(reference_rgb)
    )
    color_similarity = _bhattacharyya_similarity(
        _histogram_hsv(rendered_rgb), _histogram_hsv(reference_rgb)
    )

    # Combined perceptual score (not pixel-by-pixel matching).
    score = (0.7 * hash_similarity) + (0.3 * color_similarity)
    score = max(0.0, min(1.0, score))
    return score * 100.0


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
        scene_root = _load_scene(args.scene)
        image_buffer, components = _render_scene(
            scene_root, args.width, args.height, tuple(args.background)
        )
        rendered_image = _buffer_to_image(
            image_buffer, args.width, args.height, components
        )

        if args.output:
            output_dir = os.path.dirname(os.path.abspath(args.output))
            if output_dir and not os.path.isdir(output_dir):
                os.makedirs(output_dir)
            rendered_image.save(args.output)
            print("Render gespeichert: {0}".format(args.output))

        similarity = None
        if args.reference:
            _require_pillow()
            with Image.open(args.reference) as baseline:
                similarity = compare_images(rendered_image, baseline)
            print("Aehnlichkeit: {0:.2f}%".format(similarity))

        if similarity is not None and args.threshold is not None and similarity < args.threshold:
            print(
                "Aehnlichkeit unter Threshold ({0:.2f}% < {1:.2f}%)".format(
                    similarity, args.threshold
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
