#!/usr/bin/env python

"""
Runner for visual tests with optional Xvfb bootstrap on Linux.
"""

import os
import shutil
import subprocess
import sys


def _has_reachable_x11_display():
    display = os.environ.get("DISPLAY")
    if not display:
        return False

    if not display.startswith(":"):
        return True

    display_number = display[1:].split(".", 1)[0]
    if not display_number.isdigit():
        return True

    socket_path = "/tmp/.X11-unix/X{0}".format(display_number)
    return os.path.exists(socket_path)


def main():
    test_cmd = [sys.executable, "tests/visual_tests.py"]

    if (
        sys.platform.startswith("linux")
        and not _has_reachable_x11_display()
        and os.environ.get("PIVY_VISUALTESTS_IN_XVFB") != "1"
    ):
        xvfb_run = shutil.which("xvfb-run")
        if xvfb_run:
            env = os.environ.copy()
            env["PIVY_VISUALTESTS_IN_XVFB"] = "1"
            return subprocess.call(
                [
                    xvfb_run,
                    "-a",
                    "-s",
                    "-screen 0 1280x1024x24",
                    sys.executable,
                    "tests/visual_tests.py",
                ],
                env=env,
            )

    return subprocess.call(test_cmd)


if __name__ == "__main__":
    raise SystemExit(main())
