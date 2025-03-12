import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

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
        
        button_style = {'bg': 'blue', 'fg': 'white', 'width': 12, 'pady': 5}
        
        self.open_button = tk.Button(self.button_frame, text="Open Folder", command=self.open_folder, **button_style)
        self.open_button.pack(pady=2)
        
        self.back_button = tk.Button(self.button_frame, text="Back", command=self.go_back, **button_style)
        self.back_button.pack(pady=2)
        
        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_file, **button_style)
        self.delete_button.pack(pady=2)
        
        self.rename_button = tk.Button(self.button_frame, text="Rename", command=self.rename_file, **button_style)
        self.rename_button.pack(pady=2)
        
        self.copy_button = tk.Button(self.button_frame, text="Copy", command=self.copy_file, **button_style)
        self.copy_button.pack(pady=2)
        
        self.move_button = tk.Button(self.button_frame, text="Move", command=self.move_file, **button_style)
        self.move_button.pack(pady=2)
        
        self.search_entry = tk.Entry(self.right_frame, width=30)
        self.search_entry.pack(pady=5)
        
        self.search_button = tk.Button(self.right_frame, text="Search", command=self.search_file, **button_style)
        self.search_button.pack(pady=5)
        
        # File List
        self.file_list = tk.Listbox(self.right_frame, selectmode=tk.SINGLE)
        self.file_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.file_list.bind("<Double-Button-1>", self.open_file_or_folder)
        
        self.populate_file_list()
    
    def populate_file_list(self):
        self.file_list.delete(0, tk.END)
        path = self.current_path.get()
        print(f"Listing files in: {path}")
        try:
            for item in sorted(os.listdir(path)):
                self.file_list.insert(tk.END, item)
        except PermissionError:
            print("Permission Denied")
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
        selected = self.file_list.get(self.file_list.curselection())
        full_path = os.path.join(self.current_path.get(), selected)
        print(f"Opening: {full_path}")
        if os.path.isdir(full_path):
            self.current_path.set(full_path)
            self.populate_file_list()
        else:
            os.startfile(full_path)
    
    def delete_file(self):
        selected = self.file_list.get(self.file_list.curselection())
        full_path = os.path.join(self.current_path.get(), selected)
        if messagebox.askyesno("Confirm", f"Delete {selected}?"):
            print(f"Deleting: {full_path}")
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            else:
                os.remove(full_path)
            self.populate_file_list()
    
    def rename_file(self):
        selected = self.file_list.get(self.file_list.curselection())
        full_path = os.path.join(self.current_path.get(), selected)
        new_name = simpledialog.askstring("Rename", "Enter new name:")
        if new_name:
            new_path = os.path.join(self.current_path.get(), new_name)
            print(f"Renaming {full_path} to {new_path}")
            os.rename(full_path, new_path)
            self.populate_file_list()
    
    def copy_file(self):
        selected = self.file_list.get(self.file_list.curselection())
        full_path = os.path.join(self.current_path.get(), selected)
        destination = filedialog.askdirectory()
        if destination:
            print(f"Copying {full_path} to {destination}")
            shutil.copy(full_path, os.path.join(destination, selected))
            self.populate_file_list()
    
    def move_file(self):
        selected = self.file_list.get(self.file_list.curselection())
        full_path = os.path.join(self.current_path.get(), selected)
        destination = filedialog.askdirectory()
        if destination:
            print(f"Moving {full_path} to {destination}")
            shutil.move(full_path, os.path.join(destination, selected))
            self.populate_file_list()
    
    def search_file(self):
        query = self.search_entry.get().lower()
        print(f"Searching for: {query}")
        self.file_list.delete(0, tk.END)
        path = self.current_path.get()
        try:
            for item in os.listdir(path):
                if query in item.lower():
                    self.file_list.insert(tk.END, item)
        except PermissionError:
            print("Permission Denied")
            messagebox.showerror("Error", "Permission Denied")

if __name__ == "__main__":
    root = tk.Tk()
    FileManager(root)
    root.mainloop()
