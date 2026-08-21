# Hand Gesture Effects App

A real-time computer vision app: make hand gestures in front of your webcam, and text/visual effects appear on screen.

## Stack

- **Language:** Python
- **Hand tracking:** OpenCV + MediaPipe Hands (21 landmarks per hand, per-hand handedness labels)
- **Rendering:** OpenCV (`cv2.putText`) and/or PIL for text/overlay effects

## Architecture

1. **Hand tracking layer** — MediaPipe Hands processes webcam frames, returns landmark coordinates and handedness ("Left"/"Right") per detected hand.
2. **Gesture classifier** — Rule-based geometry checks on landmark positions to start (finger extended/curled, fingertip proximity, etc.). Can swap in an ML classifier later for custom/nuanced gestures.
3. **Effects/overlay layer** — Renders text and visual effects (particles, glow, banners, etc.) onto the frame based on the active gesture.
4. **State/trigger management** — Debouncing (gesture must hold for several consecutive frames) and cooldowns to prevent spam-triggering.

## Gesture Set

### Single-hand gestures (starter set)

| Gesture | Effect |
|---|---|
| 👍 Thumbs up | "Nice!" text + confetti burst |
| ✌️ Peace sign | Sparkle trail following hand |
| ✊ Fist | Screen shake / impact effect |
| 🖐️ Open palm | Text banner slides in |
| 👉 Point | Particle trail from fingertip |

Detection approach: compute finger states (extended vs. curled) from landmark positions using geometry — e.g., is a fingertip farther from the wrist than the knuckle below it.

### Two-hand gesture: Heart

Both hands come together to form a heart shape; triggers text on screen (e.g., "❤️ Love it!").

**Detection logic:**
1. Confirm exactly two hands are detected in the frame.
2. Use MediaPipe's handedness labels to identify which landmark set is "Left" vs. "Right" (don't assume order).
3. Check proximity between:
   - Left thumb tip (landmark 4) and right thumb tip (landmark 4)
   - Left index tip (landmark 8) and right index tip (landmark 8)
4. If both distances are below a tuned threshold → heart gesture detected.
5. Text anchor point: midpoint between the two hands (average of wrist or palm-center landmarks).

## File Structure

```
hand-gesture-effects/
├── README.md
├── requirements.txt
├── main.py                     # Entry point: webcam loop, ties everything together
│
├── gestures/
│   ├── __init__.py
│   ├── base.py                 # Gesture base class / shared helpers (e.g. distance())
│   ├── single_hand.py          # Thumbs up, peace, fist, open palm, point detectors
│   └── heart.py                # Two-hand heart gesture detector
│
├── effects/
│   ├── __init__.py
│   ├── text_overlay.py         # Text rendering (banners, fade-in, pulse)
│   └── particles.py            # Particle system (confetti, sparkle trail, impact)
│
├── core/
│   ├── __init__.py
│   ├── hand_tracker.py         # Wraps MediaPipe Hands setup + frame processing
│   ├── state_manager.py        # Debouncing, cooldowns, active-gesture tracking
│   └── config.py                # Thresholds, cooldown durations, camera settings
│
└── assets/
    └── fonts/                  # Custom fonts for text overlays (optional)
```

**Why this layout:**
- `gestures/` and `effects/` are separate so a gesture detector never has to know how its effect is drawn — `main.py` just maps detected gesture → effect call.
- `core/state_manager.py` centralizes debounce/cooldown logic so every gesture (single- or two-hand) uses the same triggering rules instead of reimplementing it.
- `core/config.py` holds tunable values (like the heart gesture's `threshold=0.05`) in one place so you're not hunting through detector files to tweak sensitivity.

## Requirements

```
opencv-python
mediapipe
```
(add `numpy`, `Pillow` as needed once particle/text rendering is built out)

## Next Steps

1. Scaffold the files above and get `core/hand_tracker.py` + `main.py` running a basic webcam loop with landmark drawing.
2. Implement `gestures/single_hand.py` with rule-based detection for the starter set.
3. Implement `gestures/heart.py` using the two-hand proximity logic above.
4. Build out `effects/text_overlay.py` and `effects/particles.py`.
5. Wire debouncing/cooldowns in `core/state_manager.py` so gestures trigger cleanly.