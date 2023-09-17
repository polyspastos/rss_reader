import os
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import feedparser
import datetime
import re
import html
import threading

# Load RSS feeds from a separate file
def load_rss_feeds():
    rss_feeds = []
    try:
        with open("feeds.txt", "r") as file:
            rss_feeds = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        pass

    return rss_feeds

# Function to filter and load run folders
def load_run_folders():
    run_folders = [folder for folder in os.listdir() if folder[0].isdigit()]
    run_combobox['values'] = run_folders
    latest_run = max(run_folders, key=os.path.getctime, default="")
    run_combobox.set(latest_run)

def load_run_content():
    selected_run = run_combobox.get()
    run_folder = os.path.join(selected_run)

    content_text.delete(1.0, tk.END)

    for filename in os.listdir(run_folder):
        file_path = os.path.join(run_folder, filename)
        if os.path.isfile(file_path) and filename.endswith(".txt"):
            file_listbox.insert(tk.END, os.path.splitext(filename)[0])

def load_file_content(event):
    selected_file = file_listbox.get(tk.ACTIVE)
    selected_run = run_combobox.get()
    file_path = os.path.join(selected_run, selected_file + ".txt")

    with open(file_path, 'r', encoding='utf-8') as file:
        content_text.delete(1.0, tk.END)
        content_text.insert(tk.END, file.read())

def fetch_new_runs():
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    folder_path = os.path.join(timestamp)

    os.makedirs(folder_path, exist_ok=True)

    for rss_url in rss_feeds:
        feed = feedparser.parse(rss_url)

        website_name = re.sub(r'[^a-zA-Z0-9]', '_', rss_url)

        filename = f"{website_name}.txt"
        filename = re.sub(r'[^a-zA-Z0-9_\.]', '_', filename)
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'w', encoding='utf-8') as file:
            for entry in feed.entries:
                news_title = entry.title
                news_summary = entry.summary

                content = ""
                for key in entry.keys():
                    if "content" in key.lower():
                        content += f"{key}: {html.unescape(entry[key])}\n"

                file.write(f"\nTitle: {news_title}\n\n")
                file.write(f"Summary: {news_summary}\n\n")
                file.write(f"Content:\n{content}\n--")

    run_combobox.set(timestamp)
    load_run_content()
    new_run_button.config(state="normal", text="New Run")

def initiate_new_run():
    new_run_button.config(state="disabled", text="Fetching new run...")

    new_run_thread = threading.Thread(target=fetch_new_runs)
    new_run_thread.start()

def refresh_runs():
    load_run_folders()

# Load RSS feeds from the file
rss_feeds = load_rss_feeds()

window = tk.Tk()
window.title("RSS Feed Reader")
window.state("zoomed")

window.configure(bg="#333333")

control_frame = ttk.Frame(window)
control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

run_label = ttk.Label(control_frame, text="Select Run:", background="#444444", foreground="white")
run_label.grid(row=0, column=0, sticky="w")

run_combobox = ttk.Combobox(control_frame, values=[], state="readonly")
run_combobox.grid(row=0, column=1, sticky="ew")

load_button = ttk.Button(control_frame, text="Load Run Content", command=load_run_content)
load_button.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

new_run_label = ttk.Label(control_frame, text="", background="#444444", foreground="white")
new_run_label.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

new_run_button = ttk.Button(control_frame, text="New Run", command=initiate_new_run)
new_run_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

refresh_button = ttk.Button(control_frame, text="Refresh Runs", command=refresh_runs)
refresh_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

content_frame = ttk.Frame(window)
content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

file_listbox = tk.Listbox(content_frame, selectmode=tk.SINGLE, width=40, background="#555555", foreground="white")
file_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
file_listbox.bind("<ButtonRelease-1>", load_file_content)

content_text = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, width=80, background="#333333", foreground="white")
content_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)
control_frame.columnconfigure(1, weight=1)
content_frame.columnconfigure(0, weight=1)
content_frame.columnconfigure(1, weight=1)
content_frame.rowconfigure(0, weight=1)

load_run_folders()  # Load run folders initially

window.mainloop()
