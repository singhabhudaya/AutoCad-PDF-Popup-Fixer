# AutoCAD PDF Hyperlink Remover

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

_A lightweight set of Python tools (CLI + GUI) that remove both standard hyperlink annotations and hidden hover‐popup actions from AutoCAD‐exported PDFs._

---

## 🎯 Why This Exists

When you export drawings from AutoCAD as PDF, you often get unwanted blue “clickable” or hover‐triggered popups (`/Annots`, `/OpenAction`, `/AA`). Those can be a nuisance if you import the PDF back into another CAD program or send it to clients. This repository provides two complementary solutions:

1. **Command‐Line Tool** (`remove_pdf_links.py`):  
   Uses [pikepdf](https://github.com/pikepdf/pikepdf) to strip out `/Annots`, `/OpenAction`, and `/AA` entries from one PDF or all PDFs in a folder. Perfect for batch processing on CI/CD, build scripts, or quick terminal commands.

2. **Windows GUI Tool** (`gui_remove_pdf_links.py`):  
   A small Tkinter application that gives you three buttons:  
   - **Remove Links** (only `/Annots`) → output `<filename>_noLinks.pdf`  
   - **Remove Popups** (only `/OpenAction` & `/AA`) → output `<filename>_noPopups.pdf`  
   - **Remove All** (both) → output `<filename>_cleaned.pdf`  

   You can bundle the GUI into a single EXE via PyInstaller so colleagues can double‐click to clean PDFs without installing Python.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**  
- **pip** (Python package manager)  
- (Optional for EXE) **PyInstaller**

### 1. Clone the Repo

```bash
git clone https://github.com/singhabhudaya/autocad-pdf-hyperlink-remover.git
cd autocad-pdf-hyperlink-remover
