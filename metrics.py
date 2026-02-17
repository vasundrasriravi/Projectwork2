# ================== metrics.py ==================

import time
from collections import defaultdict

gesture_counter = defaultdict(int)
voice_counter = defaultdict(lambda: {"success": 0, "total": 0})
fps_values = []
gesture_latencies = []

_last_gesture_time = None


# ---------------- GESTURE ----------------
def log_gesture(gesture_name):
    global _last_gesture_time
    now = time.time()

    if _last_gesture_time is not None:
        gesture_latencies.append((now - _last_gesture_time) * 1000)

    _last_gesture_time = now
    gesture_counter[gesture_name] += 1


# ---------------- VOICE ----------------
def log_voice(command, success=True):
    voice_counter[command]["total"] += 1
    if success:
        voice_counter[command]["success"] += 1


# ---------------- FPS ----------------
def log_fps(fps):
    fps_values.append(fps)


# ---------------- PRINT METRICS ----------------
def print_metrics():
    print("\n====== GESTURE METRICS ======")

    if not gesture_counter:
        print("No gesture data recorded.")
    else:
        total = sum(gesture_counter.values())
        for g, c in gesture_counter.items():
            print(f"{g:<20}: {(c/total)*100:.2f}%")

    if gesture_latencies:
        print(f"\nAverage Gesture Latency : {sum(gesture_latencies)/len(gesture_latencies):.2f} ms")
    else:
        print("\nAverage Gesture Latency : N/A")

    print("\n====== VOICE METRICS ======")
    for cmd, d in voice_counter.items():
        acc = (d["success"]/d["total"])*100 if d["total"] else 0
        print(f"{cmd:<20}: {acc:.2f}%")

    print("\n====== SYSTEM METRICS ======")
    if fps_values:
        print(f"Average Frame Rate : {sum(fps_values)/len(fps_values):.2f} FPS")
    else:
        print("No FPS data recorded.")


# ✅ BACKWARD COMPATIBILITY (IMPORTANT)
def save_and_print_metrics():
    print_metrics()
