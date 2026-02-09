import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark App")
        self.root.geometry("520x450")
        self.root.resizable(False, False)

        self.image_path = None
        self.logo_path = None
        self.result_image = None  # store final image

        self.create_ui()

    def create_ui(self):
        title = tk.Label(
            self.root,
            text="Image Watermark App",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        self.image_status = tk.Label(
            frame, text="No image selected", fg="gray"
        )
        tk.Button(
            frame, text="Select Image",
            width=25, command=self.select_image
        ).pack(pady=5)
        self.image_status.pack(pady=(0, 10))

        self.logo_status = tk.Label(
            frame, text="No logo selected", fg="gray"
        )
        tk.Button(
            frame, text="Select Logo (PNG)",
            width=25, command=self.select_logo
        ).pack(pady=5)
        self.logo_status.pack(pady=(0, 15))

        tk.Button(
            self.root,
            text="Preview Watermarked Image",
            bg="#4CAF50", fg="white",
            width=30, command=self.show_watermark
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Save Watermarked Image",
            bg="#2196F3", fg="white",
            width=30, command=self.save_image
        ).pack(pady=5)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg")]
        )
        if self.image_path:
            self.image_status.config(text="Image selected ✓", fg="green")

    def select_logo(self):
        self.logo_path = filedialog.askopenfilename(
            filetypes=[("PNG files", "*.png")]
        )
        if self.logo_path:
            self.logo_status.config(text="Logo selected ✓", fg="green")

    def show_watermark(self):
        if not self.image_path or not self.logo_path:
            messagebox.showerror("Error", "Select both image and logo.")
            return

        background = Image.open(self.image_path).convert("RGBA")
        logo = Image.open(self.logo_path).convert("RGBA")

        bg_w, bg_h = background.size

        # Resize logo (25% max width)
        max_w = bg_w // 4
        scale = min(max_w / logo.width, 1)
        logo = logo.resize(
            (int(logo.width * scale), int(logo.height * scale)),
            Image.LANCZOS
        )

        padding = 20
        position = (bg_w - logo.width - padding,
                    bg_h - logo.height - padding)

        result = Image.new("RGBA", background.size)
        result.paste(background, (0, 0))
        result.paste(logo, position, logo)

        self.result_image = result
        self.show_image(result)

    def show_image(self, image):
        window = tk.Toplevel(self.root)
        window.title("Preview")

        # Scale image to fit screen
        max_size = 900
        w, h = image.size
        scale = min(max_size / w, max_size / h, 1)
        preview = image.resize(
            (int(w * scale), int(h * scale)),
            Image.LANCZOS
        )

        photo = ImageTk.PhotoImage(preview)
        label = tk.Label(window, image=photo)
        label.image = photo
        label.pack(padx=10, pady=10)

    def save_image(self):
        if self.result_image is None:
            messagebox.showerror("Error", "No watermarked image to save.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg")
            ]
        )

        if path:
            # Convert RGBA → RGB if saving JPG
            if path.lower().endswith((".jpg", ".jpeg")):
                self.result_image.convert("RGB").save(path, quality=95)
            else:
                self.result_image.save(path)

            messagebox.showinfo("Saved", "Image saved successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
