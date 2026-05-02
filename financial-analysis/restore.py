import re
import sys

def main():
    lines = sys.stdin.readlines()
    with open('frontend/streamlit_app.py', 'w') as f:
        for line in lines:
            # Match `<line_number>: <original_line>`
            m = re.match(r'^\d+:\s(.*)$', line)
            if m:
                f.write(m.group(1) + '\n')
            elif re.match(r'^\d+:$', line):
                f.write('\n')

if __name__ == "__main__":
    main()
