import tkinter as tk
import winshell
from tkinter import messagebox, filedialog, Menu
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import datetime

class RecycleBinApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Papierkorb-Manager")
        self.geometry("850x550") 
        self.config(bg="#f0f0f0")

        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.status_label = tk.Label(main_frame, text="", font=("Arial", 12), bg="#f0f0f0")
        self.status_label.pack(pady=(0, 5))
        
        self.total_size_label = tk.Label(main_frame, text="", font=("Arial", 10), bg="#f0f0f0")
        self.total_size_label.pack(pady=(0, 10))

        search_frame = tk.Frame(main_frame, bg="#f0f0f0")
        search_frame.pack(fill="x", padx=10, pady=(0, 5))
        search_label = tk.Label(search_frame, text="Suchen:", bg="#f0f0f0")
        search_label.pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.search_entry.bind("<KeyRelease>", self.filter_list)
        
        sort_frame = tk.Frame(main_frame, bg="#f0f0f0")
        sort_frame.pack(fill="x", padx=10, pady=(0, 5))
        tk.Label(sort_frame, text="Sortieren nach:", bg="#f0f0f0").pack(side="left", padx=(0, 5))
        tk.Button(sort_frame, text="Name", command=lambda: self.sort_list('name')).pack(side="left")
        tk.Button(sort_frame, text="Größe", command=lambda: self.sort_list('size')).pack(side="left", padx=5)
        tk.Button(sort_frame, text="Datum", command=lambda: self.sort_list('date')).pack(side="left")
        
        listbox_frame = tk.Frame(main_frame)
        listbox_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
        self.listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE, yscrollcommand=scrollbar.set, font=("Courier", 10), bg="#ffffff")
        scrollbar.config(command=self.listbox.yview)
        
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.drop)
        self.listbox.bind("<Button-3>", self.show_context_menu)

        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=10)
        
        self.clear_button = tk.Button(button_frame, text="Papierkorb leeren", command=self.clear_recycle_bin, font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", relief="flat")
        self.clear_button.pack(side="left", padx=5)
        
        self.restore_button = tk.Button(button_frame, text="Element wiederherstellen", command=self.restore_selected_item, font=("Arial", 10, "bold"), bg="#3498db", fg="white", relief="flat")
        self.restore_button.pack(side="left", padx=5)

        self.delete_single_button = tk.Button(button_frame, text="Endgültig löschen", command=self.delete_selected_item_permanently, font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", relief="flat")
        self.delete_single_button.pack(side="left", padx=5)
        
        self.add_file_button = tk.Button(button_frame, text="Dateien in Papierkorb", command=self.add_files_to_bin, font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", relief="flat")
        self.add_file_button.pack(side="left", padx=5)

        self.add_folder_button = tk.Button(button_frame, text="Ordner in Papierkorb", command=self.add_folder_to_bin, font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", relief="flat")
        self.add_folder_button.pack(side="left", padx=5)
        
        self.all_items = []
        self.current_sort_key = None
        self.sort_ascending = True

        self.update_status_and_list()

    def update_status_and_list(self):
        try:
            self.all_items = list(winshell.recycle_bin())
            self.status_label.config(text=f"Der Papierkorb enthält {len(self.all_items)} Elemente.", fg="red" if self.all_items else "green")
            
            total_size_bytes = 0
            for item in self.all_items:
                try:
                    total_size_bytes += item.size()
                except AttributeError:
                    pass
                    
            self.total_size_label.config(text=f"Gesamtgröße: {self.format_size(total_size_bytes)}")
            
            self.filter_list()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Abrufen des Papierkorb-Status: {e}")
        finally:
            self.after(5000, self.update_status_and_list)

    def sort_list(self, sort_key):
        if self.current_sort_key == sort_key:
            self.sort_ascending = not self.sort_ascending
        else:
            self.current_sort_key = sort_key
            self.sort_ascending = True
        
        key_map = {
            'name': lambda item: item.original_filename().lower(),
            'size': lambda item: getattr(item, 'size', lambda: 0)(),
            'date': lambda item: getattr(item, 'deletion_date', lambda: datetime.datetime.min)()
        }
        self.all_items.sort(key=key_map[sort_key], reverse=not self.sort_ascending)
        
        self.filter_list()

    def filter_list(self, event=None):
        search_term = self.search_entry.get().lower()
        self.listbox.delete(0, tk.END)
        self.listbox.filtered_items = []
        
        self.listbox.insert(tk.END, f"{'Dateiname':<50} | {'Größe':<10} | {'Löschdatum':<20}")
        self.listbox.insert(tk.END, "-" * 85)
        
        for item in self.all_items:
            if search_term in item.original_filename().lower():
                try:
                    file_name = item.original_filename()
                    file_size = self.format_size(item.size())
                    deletion_date = item.deletion_date()
                    self.listbox.insert(tk.END, f"{file_name:<50} | {file_size:<10} | {deletion_date.strftime('%d.%m.%Y %H:%M'):<20}")
                except AttributeError:
                    file_name = item.original_filename()
                    self.listbox.insert(tk.END, f"{file_name:<50} | {'N/A':<10} | {'N/A':<20}")
                
                self.listbox.filtered_items.append(item)
        
        self.listbox.item_data = self.listbox.filtered_items

    def format_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = 0
        while size_bytes >= 1024 and i < len(size_name) - 1:
            size_bytes /= 1024
            i += 1
        return f"{size_bytes:.1f}{size_name[i]}"

    def clear_recycle_bin(self):
        if messagebox.askyesno("Papierkorb leeren", "Möchtest du den Papierkorb wirklich leeren?"):
            try:
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
                messagebox.showinfo("Erfolg", "Der Papierkorb wurde geleert.")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Leeren des Papierkorbs: {e}")

    def restore_selected_item(self):
        try:
            selected_index = self.listbox.curselection()
            if not selected_index or selected_index[0] < 2:
                messagebox.showwarning("Keine Auswahl", "Bitte wähle ein Element zum Wiederherstellen aus.")
                return
            
            item_to_restore = self.listbox.item_data[selected_index[0]-2]
            item_to_restore.undelete()
            messagebox.showinfo("Erfolg", f"'{item_to_restore.original_filename()}' wurde wiederhergestellt.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Wiederherstellen des Elements: {e}")
            
    def delete_selected_item_permanently(self):
        try:
            selected_index = self.listbox.curselection()
            if not selected_index or selected_index[0] < 2:
                messagebox.showwarning("Keine Auswahl", "Bitte wähle ein Element zum Löschen aus.")
                return
            
            item_to_delete = self.listbox.item_data[selected_index[0]-2]
            if messagebox.askyesno("Endgültig löschen", f"Möchtest du '{item_to_delete.original_filename()}' wirklich endgültig löschen?"):
                os.remove(item_to_delete.real_path())
                messagebox.showinfo("Erfolg", f"'{item_to_delete.original_filename()}' wurde endgültig gelöscht.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim endgültigen Löschen des Elements: {e}")

    def move_to_recycle_bin(self, path):
        try:
            winshell.delete_file(path)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Verschieben von '{path}' in den Papierkorb: {e}")

    def add_files_to_bin(self):
        files = filedialog.askopenfilenames()
        if files:
            for file in files:
                self.move_to_recycle_bin(file)

    def add_folder_to_bin(self):
        folder = filedialog.askdirectory()
        if folder:
            self.move_to_recycle_bin(folder)

    def drop(self, event):
        files = self.splitlist(event.data)
        for file in files:
            file_path = file.replace("{", "").replace("}", "")
            self.move_to_recycle_bin(file_path)

    def show_context_menu(self, event):
        try:
            self.listbox.selection_clear(0, tk.END)
            index = self.listbox.nearest(event.y)
            
            if index >= 2:
                self.listbox.selection_set(index)
                
                menu = Menu(self, tearoff=0)
                menu.add_command(label="Element wiederherstellen", command=self.restore_selected_item)
                menu.add_command(label="Endgültig löschen", command=self.delete_selected_item_permanently)
                
                menu.post(event.x_root, event.y_root)
        except Exception:
            pass

if __name__ == "__main__":
    app = RecycleBinApp()
    app.mainloop()