Visual reference baselines for `tests/visual_tests.py`.

To regenerate these PNG files:

```bash
# if no display is available, run under Xvfb
xvfb-run -a pixi run visualrefs
```

The generator uses deterministic scene setup (camera, light, material, size) so
images stay stable across runs in the same rendering environment.
