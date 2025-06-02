#!/usr/bin/env python3
# gui_remove_pdf_links.py

import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pikepdf

class HyperlinkRemoverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoCAD PDF Hyperlink Remover")
        self.geometry("480x240")
        self.resizable(False, False)

        # Label + Entry (read-only) to show selected file path
        tk.Label(self, text="Select a PDF to clean:").pack(pady=(15, 0))
        self.file_path_var = tk.StringVar()
        entry = tk.Entry(self, textvariable=self.file_path_var, state="readonly", width=60)
        entry.pack(pady=(5, 10), padx=10, fill=tk.X)

        # Browse button
        browse_btn = tk.Button(self, text="Browse…", width=12, command=self.browse_file)
        browse_btn.pack(pady=(0, 15))

        # Frame to hold the three action buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=(5, 0))

        # Remove Links button
        self.btn_remove_links = tk.Button(
            btn_frame, text="Remove Links", width=14,
            state="disabled", command=self.remove_links
        )
        self.btn_remove_links.grid(row=0, column=0, padx=5)

        # Remove Popups button
        self.btn_remove_popups = tk.Button(
            btn_frame, text="Remove Popups", width=14,
            state="disabled", command=self.remove_popups
        )
        self.btn_remove_popups.grid(row=0, column=1, padx=5)

        # Remove All button
        self.btn_remove_all = tk.Button(
            btn_frame, text="Remove All", width=14,
            state="disabled", command=self.remove_all
        )
        self.btn_remove_all.grid(row=0, column=2, padx=5)

    def browse_file(self):
        """
        Open a file dialog to let the user pick a PDF.
        After picking, enable the three action buttons.
        """
        chosen = filedialog.askopenfilename(
            title="Choose a PDF…",
            filetypes=[("PDF files", "*.pdf")]
        )
        if chosen:
            self.file_path_var.set(chosen)
            # Enable action buttons
            self.btn_remove_links.config(state="normal")
            self.btn_remove_popups.config(state="normal")
            self.btn_remove_all.config(state="normal")

    def remove_links(self):
        """
        Remove only /Annots from each page and save to *_noLinks.pdf
        """
        input_path = self.file_path_var.get()
        if not input_path.lower().endswith(".pdf"):
            messagebox.showerror("Error", "Please select a valid PDF file.")
            return

        base, fname = os.path.split(input_path)
        name_only, _ = os.path.splitext(fname)
        output_name = f"{name_only}_noLinks.pdf"
        output_path = os.path.join(base, output_name)

        try:
            pdf = pikepdf.Pdf.open(input_path)

            # Remove only /Annots from each page
            for page in pdf.pages:
                obj = page.obj
                if "/Annots" in obj:
                    del obj["/Annots"]

            pdf.save(output_path)
            pdf.close()

            messagebox.showinfo("Success", f"Links removed.\nSaved as:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Failed", f"Could not remove links:\n{e}")

        # Reset UI
        self._reset_ui()

    def remove_popups(self):
        """
        Remove only /OpenAction and /AA entries (hover actions) from pages and catalog.
        Save to *_noPopups.pdf
        """
        input_path = self.file_path_var.get()
        if not input_path.lower().endswith(".pdf"):
            messagebox.showerror("Error", "Please select a valid PDF file.")
            return

        base, fname = os.path.split(input_path)
        name_only, _ = os.path.splitext(fname)
        output_name = f"{name_only}_noPopups.pdf"
        output_path = os.path.join(base, output_name)

        try:
            pdf = pikepdf.Pdf.open(input_path)

            # Remove /OpenAction and /AA only from each page
            for page in pdf.pages:
                obj = page.obj
                if "/OpenAction" in obj:
                    del obj["/OpenAction"]
                if "/AA" in obj:
                    del obj["/AA"]

            # Remove catalog-level actions via trailer
            root = pdf.trailer["/Root"]
            if "/OpenAction" in root:
                del root["/OpenAction"]
            if "/AA" in root:
                del root["/AA"]

            pdf.save(output_path)
            pdf.close()

            messagebox.showinfo("Success", f"Popups removed.\nSaved as:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Failed", f"Could not remove popups:\n{e}")

        # Reset UI
        self._reset_ui()

    def remove_all(self):
        """
        Remove /Annots, /OpenAction, and /AA from pages and catalog.
        Save to *_cleaned.pdf
        """
        input_path = self.file_path_var.get()
        if not input_path.lower().endswith(".pdf"):
            messagebox.showerror("Error", "Please select a valid PDF file.")
            return

        base, fname = os.path.split(input_path)
        name_only, _ = os.path.splitext(fname)
        output_name = f"{name_only}_cleaned.pdf"
        output_path = os.path.join(base, output_name)

        try:
            pdf = pikepdf.Pdf.open(input_path)

            # Remove /Annots, /OpenAction, /AA from each page
            for page in pdf.pages:
                obj = page.obj
                if "/Annots" in obj:
                    del obj["/Annots"]
                if "/OpenAction" in obj:
                    del obj["/OpenAction"]
                if "/AA" in obj:
                    del obj["/AA"]

            # Remove catalog-level actions via trailer
            root = pdf.trailer["/Root"]
            if "/OpenAction" in root:
                del root["/OpenAction"]
            if "/AA" in root:
                del root["/AA"]

            pdf.save(output_path)
            pdf.close()

            messagebox.showinfo("Success", f"All removed.\nSaved as:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Failed", f"Could not remove all:\n{e}")

        # Reset UI
        self._reset_ui()

    def _reset_ui(self):
        """Disable action buttons and clear the selection."""
        self.btn_remove_links.config(state="disabled")
        self.btn_remove_popups.config(state="disabled")
        self.btn_remove_all.config(state="disabled")
        self.file_path_var.set("")


if __name__ == "__main__":
    app = HyperlinkRemoverApp()
    app.mainloop()
