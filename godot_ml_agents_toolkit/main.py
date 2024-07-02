import sys
import runpy


def main():
    if len(sys.argv) < 2:
        print("Usage: mypackage <script.py>")
        sys.exit(1)

    script_file = sys.argv[1]

    # Execute the provided Python script
    try:
        runpy.run_path(script_file, run_name="__main__")
    except Exception as e:
        print(f"Error running script {script_file}: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()