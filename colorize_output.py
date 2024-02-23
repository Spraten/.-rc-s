colorize_output.py 
import subprocess
import sys
import re

class Color:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'

def apply_color_rules(line):
    if "error" in line.lower():
        return f"{Color.RED}{line}{Color.RESET}"
    elif "warning" in line.lower():
        return f"{Color.YELLOW}{line}{Color.RESET}"
    elif re.search(r'\b\d{3}\b', line):  # Highlight 3-digit numbers
        return re.sub(r'(\b\d{3}\b)', f"{Color.GREEN}\\1{Color.RESET}", line)
    else:
        return line

def run_and_color_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    stdout, stderr = process.communicate()

    colored_stdout = "\n".join(apply_color_rules(line) for line in stdout.split('\n'))
    colored_stderr = "\n".join(apply_color_rules(line) for line in stderr.split('\n'))

    print(colored_stdout)
    if stderr:
        print(colored_stderr, file=sys.stderr)

def main():
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])
        run_and_color_command(command)
    else:
        print("Usage: python3 colorize_output.py '<command>'")

if __name__ == "__main__":
    main()
