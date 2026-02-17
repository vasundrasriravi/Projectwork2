# ================== plot_metrics.py ==================

import pandas as pd
import matplotlib.pyplot as plt

# ---------- GESTURE ACCURACY ----------
GESTURE_MAP = {
    "0": "FIST",
    "8": "INDEX",
    "31": "PALM",
    "33": "V_GEST",
    "34": "TWO_FINGER_CLOSED",
    "35": "PINCH_MAJOR",
    "36": "PINCH_MINOR"
}

try:
    g = pd.read_csv("gesture_metrics.csv")
    if not g.empty:
        gesture_acc = g.groupby("gesture")["success"].mean() * 100

        plt.figure()
        gesture_acc.plot(kind="bar")
        plt.ylabel("Accuracy (%)")
        plt.xlabel("Gesture")
        plt.title("Gesture Recognition Accuracy")
        plt.ylim(0, 100)
        plt.tight_layout()
        plt.show()
    else:
        print("Gesture metrics file is empty.")
except Exception as e:
    print("Gesture plot error:", e)


# ---------- VOICE ACCURACY ----------
try:
    v = pd.read_csv("voice_metrics.csv")
    if not v.empty:
        voice_acc = v.groupby("command")["success"].mean() * 100

        plt.figure()
        voice_acc.plot(kind="bar", color="green")
        plt.ylabel("Accuracy (%)")
        plt.xlabel("Command")
        plt.title("Voice Command Accuracy")
        plt.ylim(0, 100)
        plt.tight_layout()
        plt.show()
    else:
        print("Voice metrics file is empty.")
except Exception as e:
    print("Voice plot error:", e)


# ---------- FPS ----------
try:
    f = pd.read_csv("fps_metrics.csv")
    if not f.empty:
        plt.figure()
        plt.plot(f["fps"])
        plt.ylabel("FPS")
        plt.xlabel("Frame Index")
        plt.title("System Frame Rate")
        plt.tight_layout()
        plt.show()
    else:
        print("FPS metrics file is empty.")
except Exception as e:
    print("FPS plot error:", e)
