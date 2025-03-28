import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from PIL import Image, ImageTk  # Install using: pip install pillow

class FileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple File Manager")
        self.root.geometry("800x500")

        self.current_path = tk.StringVar()
        self.current_path.set(os.getcwd())

        print(f"Starting File Manager at: {self.current_path.get()}")

        # Main layout frames
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Entry to display current directory
        self.path_entry = tk.Entry(self.right_frame, textvariable=self.current_path, width=60)
        self.path_entry.pack(pady=5)

        # Buttons for navigation
        self.button_frame = tk.Frame(self.left_frame)
        self.button_frame.pack()

        # Load all icons
        self.load_all_icons()

        # Button style configuration
        button_style = {
            'bg': '#4a7a8c',  # Blue-gray color
            'fg': 'white',
            'compound': tk.LEFT,
            'padx': 10,
            'pady': 5,
            'activebackground': '#3a6a7c',
            'font': ('Arial', 10)
        }

        # Create buttons with icons
        self.open_button = tk.Button(
            self.button_frame, 
            text="  Open Folder", 
            command=self.open_folder, 
            image=self.open_icon, 
            **button_style
        )
        self.open_button.pack(pady=2, fill=tk.X)

        self.back_button = tk.Button(
            self.button_frame, 
            text="  Back", 
            command=self.go_back, 
            image=self.back_icon, 
            **button_style
        )
        self.back_button.pack(pady=2, fill=tk.X)

        self.delete_button = tk.Button(
            self.button_frame, 
            text="  Delete", 
            command=self.delete_file, 
            image=self.delete_icon, 
            **button_style
        )
        self.delete_button.pack(pady=2, fill=tk.X)

        self.rename_button = tk.Button(
            self.button_frame, 
            text="  Rename", 
            command=self.rename_file, 
            image=self.rename_icon, 
            **button_style
        )
        self.rename_button.pack(pady=2, fill=tk.X)

        self.copy_button = tk.Button(
            self.button_frame, 
            text="  Copy", 
            command=self.copy_file, 
            image=self.save_icon,  # Using save icon for copy
            **button_style
        )
        self.copy_button.pack(pady=2, fill=tk.X)

        self.move_button = tk.Button(
            self.button_frame, 
            text="  Move", 
            command=self.move_file, 
            image=self.move_icon, 
            **button_style
        )
        self.move_button.pack(pady=2, fill=tk.X)

        # Search components
        search_frame = tk.Frame(self.right_frame)
        search_frame.pack(pady=5, fill=tk.X)
        
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5))

        self.search_button = tk.Button(
            search_frame, 
            text="  Search", 
            command=self.search_file, 
            image=self.search_icon, 
            **button_style
        )
        self.search_button.pack(side=tk.LEFT)

        # File list with images using Treeview
        self.file_frame = tk.Frame(self.right_frame)
        self.file_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.file_list = ttk.Treeview(self.file_frame, columns=("Name"), show="tree")
        self.file_list.pack(fill=tk.BOTH, expand=True)

        self.file_list.bind("<Double-Button-1>", self.open_file_or_folder)

        self.populate_file_list()

    def load_all_icons(self):
        """Load all icons from the icons folder"""
        script_dir = os.path.dirname(__file__)
        icons_dir = os.path.join(script_dir, "icons")

        # Load button icons
        try:
            # File list icons
            folder_icon_path = os.path.join(icons_dir, "folder.png")
            file_icon_path = os.path.join(icons_dir, "file.png")
            
            self.list_folder_icon = ImageTk.PhotoImage(Image.open(folder_icon_path).resize((16, 16)))
            self.list_file_icon = ImageTk.PhotoImage(Image.open(file_icon_path).resize((16, 16)))

            # Button icons
            back_icon_path = os.path.join(icons_dir, "back.jpg")
            save_icon_path = os.path.join(icons_dir, "save.png")
            search_icon_path = os.path.join(icons_dir, "search.png")
            rename_icon_path = os.path.join(icons_dir, "rename.png")
            move_icon_path = os.path.join(icons_dir, "move.png")
            open_icon_path = os.path.join(icons_dir, "open.png")
            delete_icon_path = os.path.join(icons_dir, "delete.png")

            # Resize button icons to appropriate size (24x24)
            self.back_icon = ImageTk.PhotoImage(Image.open(back_icon_path).resize((24, 24)))
            self.save_icon = ImageTk.PhotoImage(Image.open(save_icon_path).resize((24, 24)))
            self.search_icon = ImageTk.PhotoImage(Image.open(search_icon_path).resize((24, 24)))
            self.rename_icon = ImageTk.PhotoImage(Image.open(rename_icon_path).resize((24, 24)))
            self.move_icon = ImageTk.PhotoImage(Image.open(move_icon_path).resize((24, 24)))
            self.open_icon = ImageTk.PhotoImage(Image.open(open_icon_path).resize((24, 24)))
            self.delete_icon = ImageTk.PhotoImage(Image.open(delete_icon_path).resize((24, 24)))

        except Exception as e:
            print(f"Error loading icons: {e}")
            # Fallback to empty images if icons not found
            self.list_folder_icon = None
            self.list_file_icon = None
            self.back_icon = tk.PhotoImage()
            self.save_icon = tk.PhotoImage()
            self.search_icon = tk.PhotoImage()
            self.rename_icon = tk.PhotoImage()
            self.move_icon = tk.PhotoImage()
            self.open_icon = tk.PhotoImage()
            self.delete_icon = tk.PhotoImage()

    def populate_file_list(self):
        """Populates the file list with directories and files"""
        self.file_list.delete(*self.file_list.get_children())  # Clear existing items
        path = self.current_path.get()
        
        try:
            for item in sorted(os.listdir(path)):
                full_path = os.path.join(path, item)
                
                if os.path.isdir(full_path):
                    self.file_list.insert("", tk.END, text=item, image=self.list_folder_icon if self.list_folder_icon else "")
                else:
                    self.file_list.insert("", tk.END, text=item, image=self.list_file_icon if self.list_file_icon else "")

        except PermissionError:
            messagebox.showerror("Error", "Permission Denied")

    def open_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            print(f"Opening folder: {folder}")
            self.current_path.set(folder)
            self.populate_file_list()

    def go_back(self):
        parent_dir = os.path.dirname(self.current_path.get())
        print(f"Going back to: {parent_dir}")
        self.current_path.set(parent_dir)
        self.populate_file_list()

    def open_file_or_folder(self, event):
        selected = self.file_list.item(self.file_list.focus())["text"]
        full_path = os.path.join(self.current_path.get(), selected)
        print(f"Opening: {full_path}")
        if os.path.isdir(full_path):
            self.current_path.set(full_path)
            self.populate_file_list()
        else:
            os.startfile(full_path)

    def delete_file(self):
        selected = self.file_list.item(self.file_list.focus())["text"]
        full_path = os.path.join(self.current_path.get(), selected)
        if messagebox.askyesno("Confirm", f"Delete {selected}?"):
            print(f"Deleting: {full_path}")
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            else:
                os.remove(full_path)
            self.populate_file_list()

    def rename_file(self):
        selected = self.file_list.item(self.file_list.focus())["text"]
        full_path = os.path.join(self.current_path.get(), selected)
        new_name = simpledialog.askstring("Rename", "Enter new name:")
        if new_name:
            new_path = os.path.join(self.current_path.get(), new_name)
            print(f"Renaming {full_path} to {new_path}")
            os.rename(full_path, new_path)
            self.populate_file_list()

    def copy_file(self):
        selected = self.file_list.item(self.file_list.focus())["text"]
        full_path = os.path.join(self.current_path.get(), selected)
        destination = filedialog.askdirectory()
        if destination:
            print(f"Copying {full_path} to {destination}")
            if os.path.isdir(full_path):
                shutil.copytree(full_path, os.path.join(destination, selected))
            else:
                shutil.copy(full_path, os.path.join(destination, selected))
            self.populate_file_list()

    def move_file(self):
        selected = self.file_list.item(self.file_list.focus())["text"]
        full_path = os.path.join(self.current_path.get(), selected)
        destination = filedialog.askdirectory()
        if destination:
            print(f"Moving {full_path} to {destination}")
            shutil.move(full_path, os.path.join(destination, selected))
            self.populate_file_list()
    
    def search_file(self):
        """Search for a file or folder by name"""
        query = self.search_entry.get().lower()
        print(f"Searching for: {query}")
        self.file_list.delete(*self.file_list.get_children())  # Clear existing items
        path = self.current_path.get()
        
        try:
            for item in sorted(os.listdir(path)):
                if query in item.lower():
                    full_path = os.path.join(path, item)
                    
                    # Add matching item back to the list
                    if os.path.isdir(full_path):
                        self.file_list.insert("", tk.END, text=item, image=self.list_folder_icon if self.list_folder_icon else "")
                    else:
                        self.file_list.insert("", tk.END, text=item, image=self.list_file_icon if self.list_file_icon else "")
        
        except PermissionError:
            print("Permission Denied")
            messagebox.showerror("Error", "Permission Denied")


if __name__ == "__main__":
    root = tk.Tk()
    FileManager(root)
    root.mainloop()
