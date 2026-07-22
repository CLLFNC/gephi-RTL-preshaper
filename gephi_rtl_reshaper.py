#!/usr/bin/env python3
"""
Gephi RTL Reshaper
------------------
GUI application to prepare Arabic/Persian (or other RTL script) labels
before importing them into Gephi, which does not natively support RTL
rendering.

The user selects ONE text column (e.g. "Name"); the app creates a new
column called "Label" containing the reshaped and visually reordered
text for correct display in Gephi.

Supports Italian, English, Arabic, and Farsi interface languages via the
selector at the top of the window. Default language: English.

Usage: double-click the executable (or "python gephi_rtl_reshaper.py").
"""

import os
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
except ImportError:
    arabic_reshaper = None
    get_display = None


def reshape_value(text):
    """Apply reshaping + bidi reordering to a single cell."""
    if pd.isna(text):
        return text
    text = str(text)
    if text.strip() == "":
        return text
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


# ---------------------------------------------------------------------------
# Translations
# ---------------------------------------------------------------------------
LANG_NAMES = {
    "en": "English",
    "it": "Italiano",
    "ar": "العربية",
    "fa": "فارسی",
}

TEXTS = {
    "en": {
        "window_title": "Gephi RTL Reshaper",
        "language_label": "Language:",
        "step1_frame": "1. Select the CSV file",
        "browse_button": "Browse...",
        "step2_frame": "2. Select the column to convert for Gephi (e.g. Name)",
        "placeholder": "Load a CSV file to see the available columns.",
        "step3_frame": "3. Generate the file for Gephi",
        "process_button": "Process and save",
        "status_loaded": "Loaded {n} rows, {m} columns.",
        "status_done": "Done! File saved to: {path}",
        "dialog_open_title": "Select the CSV with nodes or edges",
        "filetype_csv": "CSV files",
        "filetype_all": "All files",
        "err_read_title": "Read error",
        "err_read_msg": "Could not read the file:\n{e}",
        "err_missing_libs_title": "Missing libraries",
        "err_missing_libs_msg": (
            "The 'arabic_reshaper' and 'python-bidi' libraries are not installed.\n\n"
            "If you are running the Python script, install them with:\n"
            "pip install arabic_reshaper python-bidi\n\n"
            "If you are using the executable and see this message, contact whoever built it."
        ),
        "err_missing_libs_msg_short": "The required libraries are not installed. Cannot proceed.",
        "warn_no_file_title": "No file",
        "warn_no_file_msg": "Please select a CSV file first.",
        "warn_no_col_title": "No column selected",
        "warn_no_col_msg": "Select the column to convert.",
        "err_process_title": "Processing error",
        "err_process_msg": "An error occurred:\n{e}\n\n{tb}",
        "done_title": "Done",
        "done_msg": (
            "File created successfully:\n{path}\n\n"
            "The 'Label' column was added (from '{col}').\n\n"
            "Use this column as Label in Gephi."
        ),
    },
    "it": {
        "window_title": "Gephi RTL Reshaper",
        "language_label": "Lingua:",
        "step1_frame": "1. Seleziona il file CSV",
        "browse_button": "Sfoglia...",
        "step2_frame": "2. Seleziona la colonna da convertire per Gephi (es. Name)",
        "placeholder": "Carica un file CSV per vedere le colonne disponibili.",
        "step3_frame": "3. Genera il file per Gephi",
        "process_button": "Elabora e salva",
        "status_loaded": "Caricate {n} righe, {m} colonne.",
        "status_done": "Fatto! File salvato in: {path}",
        "dialog_open_title": "Seleziona il CSV con i nodi o gli archi",
        "filetype_csv": "File CSV",
        "filetype_all": "Tutti i file",
        "err_read_title": "Errore di lettura",
        "err_read_msg": "Impossibile leggere il file:\n{e}",
        "err_missing_libs_title": "Librerie mancanti",
        "err_missing_libs_msg": (
            "Le librerie 'arabic_reshaper' e 'python-bidi' non sono installate.\n\n"
            "Se stai eseguendo lo script Python, installale con:\n"
            "pip install arabic_reshaper python-bidi\n\n"
            "Se stai usando l'eseguibile e vedi questo messaggio, contatta chi lo ha creato."
        ),
        "err_missing_libs_msg_short": "Le librerie necessarie non sono installate. Impossibile procedere.",
        "warn_no_file_title": "Nessun file",
        "warn_no_file_msg": "Seleziona prima un file CSV.",
        "warn_no_col_title": "Nessuna colonna selezionata",
        "warn_no_col_msg": "Seleziona la colonna da convertire.",
        "err_process_title": "Errore durante l'elaborazione",
        "err_process_msg": "Si è verificato un errore:\n{e}\n\n{tb}",
        "done_title": "Completato",
        "done_msg": (
            "File creato con successo:\n{path}\n\n"
            "È stata aggiunta la colonna 'Label' (da '{col}').\n\n"
            "Usa questa colonna come Label in Gephi."
        ),
    },
    "ar": {
        "window_title": "Gephi RTL Reshaper",
        "language_label": ":اللغة",
        "step1_frame": "١. اختر ملف CSV",
        "browse_button": "استعراض...",
        "step2_frame": "٢. اختر العمود المراد تحويله لـ Gephi (مثال: Name)",
        "placeholder": "قم بتحميل ملف CSV لعرض الأعمدة المتاحة.",
        "step3_frame": "٣. إنشاء الملف الخاص بـ Gephi",
        "process_button": "معالجة وحفظ",
        "status_loaded": "تم تحميل {n} صف و {m} عمود.",
        "status_done": "تم! تم حفظ الملف في: {path}",
        "dialog_open_title": "اختر ملف CSV الخاص بالعقد أو الروابط",
        "filetype_csv": "ملفات CSV",
        "filetype_all": "جميع الملفات",
        "err_read_title": "خطأ في القراءة",
        "err_read_msg": ":تعذر قراءة الملف\n{e}",
        "err_missing_libs_title": "مكتبات مفقودة",
        "err_missing_libs_msg": (
            ".المكتبتان 'arabic_reshaper' و 'python-bidi' غير مثبتتين\n\n"
            ":إذا كنت تشغّل سكربت Python، ثبّتهما باستخدام\n"
            "pip install arabic_reshaper python-bidi\n\n"
            ".إذا كنت تستخدم الملف التنفيذي وظهرت لك هذه الرسالة، تواصل مع من أنشأه"
        ),
        "err_missing_libs_msg_short": ".المكتبات المطلوبة غير مثبتة. لا يمكن المتابعة",
        "warn_no_file_title": "لا يوجد ملف",
        "warn_no_file_msg": ".الرجاء اختيار ملف CSV أولاً",
        "warn_no_col_title": "لم يتم اختيار عمود",
        "warn_no_col_msg": ".اختر العمود المراد تحويله",
        "err_process_title": "خطأ أثناء المعالجة",
        "err_process_msg": ":حدث خطأ\n{e}\n\n{tb}",
        "done_title": "تم بنجاح",
        "done_msg": (
            ":تم إنشاء الملف بنجاح\n{path}\n\n"
            ".('{col}' تمت إضافة العمود 'Label' (من\n\n"
            ".استخدم هذا العمود كـ Label في Gephi"
        ),
    },
    "fa": {
        "window_title": "Gephi RTL Reshaper",
        "language_label": ":زبان",
        "step1_frame": "۱. فایل CSV را انتخاب کنید",
        "browse_button": "انتخاب فایل...",
        "step2_frame": "۲. ستونی که باید برای Gephi تبدیل شود را انتخاب کنید (مثلاً Name)",
        "placeholder": "برای مشاهده ستون‌های موجود، یک فایل CSV بارگذاری کنید.",
        "step3_frame": "۳. ساخت فایل برای Gephi",
        "process_button": "پردازش و ذخیره",
        "status_loaded": "{n} ردیف و {m} ستون بارگذاری شد.",
        "status_done": ":انجام شد! فایل ذخیره شد در\n{path}",
        "dialog_open_title": "فایل CSV گره‌ها یا یال‌ها را انتخاب کنید",
        "filetype_csv": "فایل‌های CSV",
        "filetype_all": "همه فایل‌ها",
        "err_read_title": "خطا در خواندن",
        "err_read_msg": ":امکان خواندن فایل وجود ندارد\n{e}",
        "err_missing_libs_title": "کتابخانه‌های موجود نیست",
        "err_missing_libs_msg": (
            ".کتابخانه‌های 'arabic_reshaper' و 'python-bidi' نصب نشده‌اند\n\n"
            ":اگر اسکریپت پایتون را اجرا می‌کنید، آن‌ها را با این دستور نصب کنید\n"
            "pip install arabic_reshaper python-bidi\n\n"
            ".اگر از فایل اجرایی استفاده می‌کنید و این پیام را می‌بینید، با سازنده آن تماس بگیرید"
        ),
        "err_missing_libs_msg_short": ".کتابخانه‌های لازم نصب نشده‌اند. ادامه ممکن نیست",
        "warn_no_file_title": "فایلی انتخاب نشده",
        "warn_no_file_msg": ".لطفاً ابتدا یک فایل CSV انتخاب کنید",
        "warn_no_col_title": "ستونی انتخاب نشده",
        "warn_no_col_msg": ".ستونی که باید تبدیل شود را انتخاب کنید",
        "err_process_title": "خطا در پردازش",
        "err_process_msg": ":خطایی رخ داد\n{e}\n\n{tb}",
        "done_title": "انجام شد",
        "done_msg": (
            ":فایل با موفقیت ساخته شد\n{path}\n\n"
            ".(ستون 'Label' اضافه شد (از '{col}'\n\n"
            ".از این ستون به‌عنوان Label در Gephi استفاده کنید"
        ),
    },
}

DEFAULT_LANG = "en"


class ReshaperApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.current_lang = DEFAULT_LANG

        self.geometry("560x520")
        self.resizable(False, False)

        self.input_path = tk.StringVar()
        self.df = None
        self.selected_column = tk.StringVar(value="")  # single-column selection

        self._build_ui()
        self._apply_language()

        if arabic_reshaper is None or get_display is None:
            t = TEXTS[self.current_lang]
            messagebox.showerror(t["err_missing_libs_title"], t["err_missing_libs_msg"])

    # -- UI construction ---------------------------------------------------

    def _build_ui(self):
        pad = {"padx": 12, "pady": 8}

        # --- Language selector ---
        lang_frame = ttk.Frame(self)
        lang_frame.pack(fill="x", padx=12, pady=(10, 0))

        self.lang_label = ttk.Label(lang_frame, text="")
        self.lang_label.pack(side="left", padx=(0, 8))

        self.lang_combo = ttk.Combobox(
            lang_frame,
            state="readonly",
            values=[LANG_NAMES[code] for code in ("en", "it", "ar", "fa")],
            width=12,
        )
        self.lang_combo.pack(side="left")
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_language_change)

        # --- Step 1: file selection ---
        self.frame1 = ttk.LabelFrame(self, text="")
        self.frame1.pack(fill="x", **pad)

        entry = ttk.Entry(self.frame1, textvariable=self.input_path, state="readonly")
        entry.pack(side="left", fill="x", expand=True, padx=(8, 4), pady=8)

        self.browse_btn = ttk.Button(self.frame1, text="", command=self.browse_file)
        self.browse_btn.pack(side="left", padx=(0, 8), pady=8)

        # --- Step 2: column selection ---
        self.frame2 = ttk.LabelFrame(self, text="")
        self.frame2.pack(fill="both", expand=True, **pad)

        self.columns_frame = ttk.Frame(self.frame2)
        self.columns_frame.pack(fill="both", expand=True, padx=8, pady=8)

        self.placeholder_label = ttk.Label(self.columns_frame, text="")
        self.placeholder_label.pack(anchor="w")

        # --- Step 3: run ---
        self.frame3 = ttk.LabelFrame(self, text="")
        self.frame3.pack(fill="x", **pad)

        self.process_btn = ttk.Button(self.frame3, text="", command=self.process)
        self.process_btn.pack(pady=10)

        self.status_var = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.status_var, foreground="#444").pack(
            anchor="w", padx=16, pady=(0, 8)
        )

    # -- Language handling ---------------------------------------------------

    def _on_language_change(self, event=None):
        selected_name = self.lang_combo.get()
        for code, name in LANG_NAMES.items():
            if name == selected_name:
                self.current_lang = code
                break
        self._apply_language()

    def _apply_language(self):
        t = TEXTS[self.current_lang]

        self.title(t["window_title"])
        self.lang_label.config(text=t["language_label"])
        self.lang_combo.set(LANG_NAMES[self.current_lang])

        self.frame1.config(text=t["step1_frame"])
        self.browse_btn.config(text=t["browse_button"])

        self.frame2.config(text=t["step2_frame"])
        self.frame3.config(text=t["step3_frame"])
        self.process_btn.config(text=t["process_button"])

        # Only show the placeholder text if no columns are currently listed
        if self.df is None:
            self.placeholder_label.config(text=t["placeholder"])

    # -- Core logic ----------------------------------------------------------

    def browse_file(self):
        t = TEXTS[self.current_lang]
        path = filedialog.askopenfilename(
            title=t["dialog_open_title"],
            filetypes=[(t["filetype_csv"], "*.csv"), (t["filetype_all"], "*.*")],
        )
        if not path:
            return

        try:
            df = pd.read_csv(path)
        except Exception as e:
            messagebox.showerror(t["err_read_title"], t["err_read_msg"].format(e=e))
            return

        self.input_path.set(path)
        self.df = df
        self._populate_columns(df.columns.tolist())
        self.status_var.set(t["status_loaded"].format(n=len(df), m=len(df.columns)))

    def _populate_columns(self, columns):
        for widget in self.columns_frame.winfo_children():
            widget.destroy()

        self.selected_column.set("")

        # Priority order for the pre-selected default column
        priority = ["name", "label", "edge label", "edge_label"]
        default_col = None
        for cand in priority:
            for col in columns:
                if col.strip().lower() == cand:
                    default_col = col
                    break
            if default_col:
                break

        for col in columns:
            ttk.Radiobutton(
                self.columns_frame, text=col, value=col, variable=self.selected_column
            ).pack(anchor="w", pady=2)

        if default_col:
            self.selected_column.set(default_col)

    def process(self):
        t = TEXTS[self.current_lang]

        if self.df is None:
            messagebox.showwarning(t["warn_no_file_title"], t["warn_no_file_msg"])
            return

        if arabic_reshaper is None or get_display is None:
            messagebox.showerror(t["err_missing_libs_title"], t["err_missing_libs_msg_short"])
            return

        selected_col = self.selected_column.get()
        if not selected_col:
            messagebox.showwarning(t["warn_no_col_title"], t["warn_no_col_msg"])
            return

        try:
            df_out = self.df.copy()
            df_out["Label"] = df_out[selected_col].apply(reshape_value)

            in_path = self.input_path.get()
            base, ext = os.path.splitext(in_path)
            out_path = f"{base}_reshaped.csv"

            df_out.to_csv(out_path, index=False)

        except Exception as e:
            messagebox.showerror(
                t["err_process_title"],
                t["err_process_msg"].format(e=e, tb=traceback.format_exc()),
            )
            return

        self.status_var.set(t["status_done"].format(path=out_path))
        messagebox.showinfo(
            t["done_title"],
            t["done_msg"].format(path=out_path, col=selected_col),
        )


def main():
    app = ReshaperApp()
    app.mainloop()


if __name__ == "__main__":
    main()