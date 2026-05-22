import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image

# Setup theme and appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class OmniConvertApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("OmniConvert v1.2 - Personal Batch Converter")
        self.geometry("850x750")
        # PERBAIKAN: Menggunakan fungsi minsize() yang benar bawaan Tkinter
        self.minsize(700, 600) 
        self.resizable(True, True)
        
        # State variables
        self.input_folder = ""
        self.output_folder = ""
        self.files_by_category = {
            "Gambar": [],
            "Dokumen": [],
            "Presentasi": [],
            "Script": []
        }
        
        # Supported Extensions
        self.ext_map = {
            "Gambar": [".jpg", ".jpeg", ".png", ".webp", ".bmp"],
            "Dokumen": [".docx", ".pdf", ".txt"],
            "Presentasi": [".ppt", ".pptx"],
            "Script": [".py"]
        }
        
        self.init_ui()
        
    def init_ui(self):
        # --- TOP SECTION: Folder Selection ---
        self.top_frame = ctk.CTkFrame(self, corner_radius=15)
        self.top_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        self.btn_select_folder = ctk.CTkButton(
            self.top_frame, text="Pilih Folder Sumber", font=("Urbanist", 14, "bold"),
            command=self.browse_input_folder, width=180
        )
        self.btn_select_folder.pack(side="left", padx=15, pady=15)
        
        self.lbl_folder_path = ctk.CTkLabel(
            self.top_frame, text="Belum ada folder yang dipilih...", 
            font=("Urbanist", 12), text_color="#aaaaaa", anchor="w"
        )
        self.lbl_folder_path.pack(side="left", fill="x", expand=True, padx=10)
        
        # --- MIDDLE SECTION: Dynamic Category Controls ---
        self.mid_frame = ctk.CTkFrame(self, corner_radius=15)
        self.mid_frame.pack(fill="x", padx=20, pady=10)
        
        self.lbl_cat_title = ctk.CTkLabel(
            self.mid_frame, text="Pengaturan Konversi Per Kategori (Pendekatan A)", 
            font=("Urbanist", 14, "bold"), text_color="#deff9a"
        )
        self.lbl_cat_title.pack(anchor="w", padx=15, pady=10)
        
        # Container for rows
        self.rows_container = ctk.CTkFrame(self.mid_frame, fg_color="transparent")
        self.rows_container.pack(fill="x", padx=15, pady=5)
        
        # Dictionary to hold UI elements for each category
        self.category_ui = {}
        categories = [
            ("Gambar", ["PNG", "JPG", "WEBP", "PDF"]),
            ("Dokumen", ["PDF", "DOCX", "TXT"]),
            ("Presentasi", ["PDF"]),
            ("Script", ["PDF", "TXT"])
        ]
        
        for cat_name, targets in categories:
            row = ctk.CTkFrame(self.rows_container, fg_color="transparent")
            row.pack(fill="x", pady=6)
            
            # Checkbox to enable/disable category
            chk_var = ctk.BooleanVar(value=False)
            chk = ctk.CTkCheckBox(
                row, text=f"{cat_name} (0 file ditemukan)", font=("Urbanist", 13),
                variable=chk_var, state="disabled", command=self.update_convert_button_state
            )
            chk.pack(side="left", padx=5)
            
            # Label arrow
            lbl_to = ctk.CTkLabel(row, text="ubah ke ➔", font=("Urbanist", 12), text_color="#888888")
            lbl_to.pack(side="left", padx=15)
            
            # Dropdown target
            combo = ctk.CTkComboBox(row, values=targets, width=120, state="disabled")
            combo.pack(side="left", padx=5)
            
            self.category_ui[cat_name] = {
                "checkbox": chk,
                "chk_var": chk_var,
                "combo": combo
            }
            
        # --- BOTTOM SECTION: Output, Logs & Progress (Responsive Area) ---
        self.bottom_frame = ctk.CTkFrame(self, corner_radius=15)
        self.bottom_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Output directory row
        out_row = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        out_row.pack(fill="x", padx=15, pady=10)
        
        self.btn_out_folder = ctk.CTkButton(
            out_row, text="Folder Output", font=("Urbanist", 12),
            width=120, fg_color="#333333", hover_color="#444444", command=self.browse_output_folder
        )
        self.btn_out_folder.pack(side="left")
        
        self.lbl_out_path = ctk.CTkLabel(
            out_row, text="Sama dengan folder sumber (_converted)", 
            font=("Urbanist", 12), text_color="#888888", anchor="w"
        )
        self.lbl_out_path.pack(side="left", fill="x", expand=True, padx=10)
        
        # Log terminal
        self.txt_log = ctk.CTkTextbox(self.bottom_frame, font=("Consolas", 11), fg_color="#111111", text_color="#daffde")
        self.txt_log.pack(fill="both", expand=True, padx=15, pady=5)
        self.log("Sistem OmniConvert Siap. Silakan pilih folder untuk memulai.")
        
        # Progress Bar
        self.progress = ctk.CTkProgressBar(self.bottom_frame, progress_color="#deff9a")
        self.progress.pack(fill="x", padx=15, pady=10)
        self.progress.set(0)
        
        # Action Button
        self.btn_convert = ctk.CTkButton(
            self.bottom_frame, text="KONVERSI SEKARANG", font=("Urbanist", 16, "bold"),
            fg_color="#a3cf45", hover_color="#deff9a", text_color="#000000",
            height=45, state="disabled", command=self.start_conversion_thread
        )
        self.btn_convert.pack(fill="x", padx=15, pady=(5, 15))

    def log(self, message):
        self.txt_log.insert(tk.END, message + "\n")
        self.txt_log.see(tk.END)

    def browse_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder = os.path.normpath(folder)
            self.lbl_folder_path.configure(text=self.input_folder, text_color="#deff9a")
            self.output_folder = os.path.join(self.input_folder, "_converted")
            self.lbl_out_path.configure(text=self.output_folder)
            self.scan_folder()
            
    def browse_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = os.path.normpath(folder)
            self.lbl_out_path.configure(text=self.output_folder)

    def scan_folder(self):
        for cat in self.files_by_category:
            self.files_by_category[cat] = []
            
        self.log(f"\nMemindai folder: {self.input_folder}...")
        
        try:
            all_files = os.listdir(self.input_folder)
            for f in all_files:
                full_path = os.path.join(self.input_folder, f)
                if os.path.isfile(full_path):
                    _, ext = os.path.splitext(f.lower())
                    for cat_name, extensions in self.ext_map.items():
                        if ext in extensions:
                            self.files_by_category[cat_name].append(full_path)
                            break
                            
            for cat_name, ui in self.category_ui.items():
                count = len(self.files_by_category[cat_name])
                ui["checkbox"].configure(text=f"{cat_name} ({count} file ditemukan)")
                
                if count > 0:
                    ui["checkbox"].configure(state="normal")
                    ui["chk_var"].set(True)
                    ui["combo"].configure(state="readonly")
                else:
                    ui["checkbox"].configure(state="disabled")
                    ui["chk_var"].set(False)
                    ui["combo"].configure(state="disabled")
                    
            self.log("Pemindaian selesai.")
            self.update_convert_button_state()
            
        except Exception as e:
            self.log(f"Gagal memindai folder: {str(e)}")
            messagebox.showerror("Error", f"Gagal memindai folder: {str(e)}")

    def update_convert_button_state(self):
        any_active = False
        for cat_name, ui in self.category_ui.items():
            if ui["chk_var"].get() and len(self.files_by_category[cat_name]) > 0:
                any_active = True
                break
        
        if any_active:
            self.btn_convert.configure(state="normal")
        else:
            self.btn_convert.configure(state="disabled")

    def start_conversion_thread(self):
        self.btn_convert.configure(state="disabled")
        self.btn_select_folder.configure(state="disabled")
        threading.Thread(target=self.execute_conversion, daemon=True).start()

    def execute_conversion(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            
        tasks = []
        for cat_name, ui in self.category_ui.items():
            if ui["chk_var"].get():
                target_fmt = ui["combo"].get().lower()
                for file_path in self.files_by_category[cat_name]:
                    tasks.append((file_path, cat_name, target_fmt))
                    
        total_tasks = len(tasks)
        if total_tasks == 0:
            return
            
        self.log(f"\nMemulai konversi masal untuk {total_tasks} file...")
        
        success_count = 0
        for index, (file_path, cat, target_fmt) in enumerate(tasks):
            base_name = os.path.basename(file_path)
            name_without_ext, _ = os.path.splitext(base_name)
            self.log(f"[{index+1}/{total_tasks}] Mengonversi {base_name}...")
            
            try:
                # 1. LOGIC FOR IMAGES
                if cat == "Gambar":
                    out_name = f"{name_without_ext}.{target_fmt}"
                    out_path = os.path.join(self.output_folder, out_name)
                    img = Image.open(file_path)
                    if target_fmt == "jpg" or target_fmt == "jpeg":
                        if img.mode in ("RGBA", "LA"):
                            background = Image.new("RGB", img.size, (255, 255, 255))
                            background.paste(img, mask=img.split()[3])
                            img = background
                        else:
                            img = img.convert("RGB")
                    img.save(out_path)
                    success_count += 1
                
                # 2. LOGIC FOR DOCUMENTS
                elif cat == "Dokumen":
                    _, origin_ext = os.path.splitext(base_name.lower())
                    if origin_ext == ".docx" and target_fmt == "pdf":
                        import win32com.client
                        word = win32com.client.Dispatch("Word.Application")
                        doc = word.Documents.Open(file_path, Visible=False)
                        out_path = os.path.join(self.output_folder, f"{name_without_ext}.pdf")
                        doc.SaveAs(out_path, 17)
                        doc.Close()
                        word.Quit()
                        success_count += 1
                        
                    elif origin_ext == ".pdf" and target_fmt == "docx":
                        from pdf2docx import Converter
                        out_path = os.path.join(self.output_folder, f"{name_without_ext}.docx")
                        cv = Converter(file_path)
                        cv.convert(out_path, start=0, end=None)
                        cv.close()
                        success_count += 1
                        
                    elif origin_ext == ".pdf" and target_fmt == "txt":
                        import pypdf
                        out_path = os.path.join(self.output_folder, f"{name_without_ext}.txt")
                        reader = pypdf.PdfReader(file_path)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text() + "\n"
                        with open(out_path, "w", encoding="utf-8") as f:
                            f.write(text)
                        success_count += 1
                
                # 3. LOGIC FOR PRESENTATIONS
                elif cat == "Presentasi":
                    if target_fmt == "pdf":
                        import win32com.client
                        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
                        deck = powerpoint.Presentations.Open(file_path, WithWindow=False)
                        out_path = os.path.join(self.output_folder, f"{name_without_ext}.pdf")
                        deck.SaveAs(out_path, 32)
                        deck.Close()
                        powerpoint.Quit()
                        success_count += 1
                
                # 4. LOGIC FOR CODE SCRIPTS
                elif cat == "Script":
                    if target_fmt == "pdf":
                        from fpdf import FPDF
                        out_path = os.path.join(self.output_folder, f"{name_without_ext}.pdf")
                        with open(file_path, "r", encoding="utf-8") as f:
                            code_lines = f.readlines()
                        
                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_font("Courier", size=10)
                        for line in code_lines:
                            clean_line = line.replace("\t", "    ").rstrip()
                            pdf.cell(0, 5, txt=clean_line, ln=True)
                        pdf.output(out_path)
                        success_count += 1
                        
                    elif target_fmt == "txt":
                        import shutil
                        out_path = os.path.join(self.output_folder, f"{name_without_ext}.txt")
                        shutil.copy(file_path, out_path)
                        success_count += 1
                        
            except Exception as e:
                self.log(f"❌ Gagal mengonversi {base_name}: {str(e)}")
                
            self.progress.set((index + 1) / total_tasks)
            
        self.log(f"\nProses Selesai! Berhasil mengonversi {success_count} dari {total_tasks} file.")
        messagebox.showinfo("Selesai", f"Proses selesai!\nBerhasil mengonversi {success_count}/{total_tasks} file.")
        
        self.btn_convert.configure(state="normal")
        self.btn_select_folder.configure(state="normal")
        self.progress.set(0)

if __name__ == "__main__":
    app = OmniConvertApp()
    app.mainloop()