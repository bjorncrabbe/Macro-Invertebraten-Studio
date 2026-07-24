import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

from backend.camera import Camera
from backend.ai_engine import AIEngine
from backend.determination import DeterminationEngine
from backend.count_manager import ObservationLogger


class MacroStudio:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("🔬 Macro-Invertebraten Studio v4.0")

        self.root.geometry("1400x850")

        self.root.configure(bg="#f2f2f2")

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        # Engines

        self.camera = Camera()

        self.ai = AIEngine()

        self.key = DeterminationEngine()

        self.logger = ObservationLogger()

        # Bouw GUI

        self.build_ui()

    # Camera starten
    if not self.camera.connect():
        messagebox.showwarning(
        "Camera",
        "Geen camera gevonden."
    )

    # Start de videoloop
    self.update_video()
    def build_ui(self):

        # =======================
        # Bovenbalk
        # =======================

        top = tk.Frame(
            self.root,
            bg="#1f4e79",
            height=60
        )

        top.pack(fill="x")

        tk.Label(
            top,
            text="🔬 Macro-Invertebraten Studio v4.0",
            bg="#1f4e79",
            fg="white",
            font=("Segoe UI",18,"bold")
        ).pack(
            side="left",
            padx=20,
            pady=10
        )

        # =======================
        # Midden
        # =======================

        body = tk.Frame(
            self.root,
            bg="#f2f2f2"
        )

        body.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Camera

        self.left = tk.Frame(
            body,
            bg="black"
        )

        self.left.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.video = tk.Label(
            self.left,
            bg="black"
        )

        self.video.pack(
            fill="both",
            expand=True
        )

        # Rechterpaneel

        self.right = tk.Frame(
            body,
            bg="white",
            width=420
        )

        self.right.pack(
            side="right",
            fill="y"
        )

        self.right.pack_propagate(False)

        # AI

        tk.Label(
            self.right,
            text="AI Familie",
            bg="white",
            font=("Segoe UI",14,"bold")
        ).pack(
            pady=(20,5)
        )

        self.lbl_family = tk.Label(
            self.right,
            text="-",
            bg="white",
            fg="blue",
            font=("Segoe UI",18,"bold")
        )

        self.lbl_family.pack()

        self.lbl_confidence = tk.Label(
            self.right,
            text="0 %",
            bg="white",
            font=("Segoe UI",12)
        )

        self.lbl_confidence.pack()

        # Sleutel

        tk.Label(
            self.right,
            text="Determinatiesleutel",
            bg="white",
            font=("Segoe UI",14,"bold")
        ).pack(
            pady=(30,10)
        )

        self.btnA = tk.Button(
            self.right,
            text="A",
            width=40,
            height=4
        )

        self.btnA.pack(pady=5)

        self.btnB = tk.Button(
            self.right,
            text="B",
            width=40,
            height=4
        )

        self.btnB.pack(pady=5)

        self.lbl_result = tk.Label(
            self.right,
            text="Nog geen resultaat",
            bg="white",
            fg="green",
            wraplength=350
        )

        self.lbl_result.pack(
            pady=20
        )

        self.btn_save = tk.Button(
            self.right,
            text="Waarneming opslaan"
        )

        self.btn_save.pack(
            pady=10
        )

    def update_video(self):

        frame = self.camera.read()

        if frame is not None:
            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            image = Image.fromarray(frame)

            image.thumbnail((900, 700))

            photo = ImageTk.PhotoImage(image)

            self.video.configure(image=photo)

            self.video.image = photo

        self.root.after(
            30,
            self.update_video
        )
    def run(self):

        self.root.mainloop()

    def close(self):

        self.camera.disconnect()

        self.root.destroy()