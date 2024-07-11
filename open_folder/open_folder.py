from flask import Flask, request, jsonify
import os
import subprocess
import logging
import tkinter as tk
from tkinter import filedialog

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    folder_selected = filedialog.askdirectory()
    return folder_selected

def check_path_file():
    home_dir = os.path.expanduser("~")
    path_file = os.path.join(home_dir, "path.txt")
    
    if os.path.exists(path_file):
        with open(path_file, 'r') as f:
            path = f.readline().strip()
        print(f"Path read from path.txt: {path}")
    else:
        print("Path.txt not found. Select a folder to save path.txt:")
        selected_folder = select_folder()
        if selected_folder:
            with open(path_file, 'w') as f:
                f.write(selected_folder)
            print(f"Created path.txt with path: {selected_folder}")

def get_path_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            path = file.readline().strip()
            return path
    except Exception as e:
        app.logger.error(f"Error reading file {file_name}: {e}")
        return None


@app.route('/open_folder', methods=['POST'])
def open_folder():
    data = request.get_json()
    unix_file_path = data.get('file_path')

    # Convert Unix path to Windows path
    windows_home = get_path_from_file('C:/Users/Alien/path.txt')
    windows_file_path = unix_file_path.replace('/root/orders', os.path.join(windows_home, 'orders')).replace('/', '\\')
    
    # Log paths
    app.logger.debug(f"Received Unix file path: {unix_file_path}")
    app.logger.debug(f"Converted Windows file path: {windows_file_path}")

    if os.path.exists(windows_file_path):
        subprocess.run(['explorer', windows_file_path])
        return jsonify({"status": "success"}), 200
    else:
        app.logger.error(f"File path does not exist -> {windows_file_path}")
        return jsonify({"error": f"File path does not exist -> {windows_file_path}"}), 404

if __name__ == '__main__':
    check_path_file()
    app.run(host='0.0.0.0', port=5000)
