
from flask import Flask, request, jsonify
import os
import subprocess
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/open_folder', methods=['POST'])
def open_folder():
    data = request.get_json()
    unix_file_path = data.get('file_path')

    # Convert Unix path to Windows path
    windows_file_path = unix_file_path.replace('/root/orders', 'C:\\Users\\Mans_Alien\\orders').replace('/', '\\')
    
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
    app.run(host='0.0.0.0', port=5000)