import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageCombiner:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Combiner")
        
        self.images = []
        self.padding = 0
        
        self.create_widgets()
        
    def create_widgets(self):
        self.add_button = tk.Button(self.root, text="Add Images", command=self.add_images)
        self.add_button.pack(pady=10)
        
        self.padding_label = tk.Label(self.root, text="Padding (px):")
        self.padding_label.pack()
        
        self.padding_entry = tk.Entry(self.root)
        self.padding_entry.pack(pady=5)
        
        self.orientation_var = tk.StringVar(value="horizontal")
        self.horizontal_radio = tk.Radiobutton(self.root, text="Horizontal", variable=self.orientation_var, value="horizontal")
        self.horizontal_radio.pack()
        
        self.vertical_radio = tk.Radiobutton(self.root, text="Vertical", variable=self.orientation_var, value="vertical")
        self.vertical_radio.pack()
        
        self.preview_button = tk.Button(self.root, text="Preview", command=self.preview)
        self.preview_button.pack(pady=10)
        
        self.save_button = tk.Button(self.root, text="Save", command=self.save_image)
        self.save_button.pack(pady=10)
        
        self.close_button = tk.Button(self.root, text="Close", command=self.root.quit)
        self.close_button.pack(pady=10)
        
        self.preview_label = tk.Label(self.root)
        self.preview_label.pack(pady=10)
        
    def add_images(self):
        file_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        self.images.extend(file_paths)
        messagebox.showinfo("Info", f"{len(file_paths)} images added.")
        
    def preview(self):
        if not self.images:
            messagebox.showwarning("Warning", "No images added.")
            return
        
        try:
            self.padding = int(self.padding_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Padding must be an integer.")
            return
        
        combined_image = self.combine_images()
        if combined_image:
            self.display_image(combined_image)
        
    def combine_images(self):
        images = [Image.open(img) for img in self.images]
        
        if self.orientation_var.get() == "horizontal":
            total_width = sum(img.width for img in images) + self.padding * (len(images) - 1)
            max_height = max(img.height for img in images)
            combined = Image.new('RGB', (total_width, max_height), (255, 255, 255))
            
            x_offset = 0
            for img in images:
                combined.paste(img, (x_offset, 0))
                x_offset += img.width + self.padding
                
        else:  # vertical
            total_height = sum(img.height for img in images) + self.padding * (len(images) - 1)
            max_width = max(img.width for img in images)
            combined = Image.new('RGB', (max_width, total_height), (255, 255, 255))
            
            y_offset = 0
            for img in images:
                combined.paste(img, (0, y_offset))
                y_offset += img.height + self.padding
                
        return combined
    
    def display_image(self, img):
        img.thumbnail((400, 400))  # Resize for preview
        img_tk = ImageTk.PhotoImage(img)
        self.preview_label.config(image=img_tk)
        self.preview_label.image = img_tk  # Keep a reference to avoid garbage collection
    
    def save_image(self):
        if not self.images:
            messagebox.showwarning("Warning", "No images to save.")
            return
        
        combined_image = self.combine_images()
        if combined_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
            if file_path:
                combined_image.save(file_path)
                messagebox.showinfo("Info", "Image saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCombiner(root)
    root.mainloop()