import subprocess
import importlib

def check_package(package):
    try:
        importlib.import_module(package)
        return True
    except ImportError:
        return False

def install_packages(packages):
    for package in packages:
        subprocess.call(['pip', 'install', package])

def run_streamlit():
    command = 'streamlit run frontend.py'
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    required_packages = ['streamlit', 'pandas']

    missing_packages = [package for package in required_packages if not check_package(package)]

    if missing_packages:
        print("The following packages are missing: {}".format(', '.join(missing_packages)))
        install_packages(missing_packages)
        print("Packages installed successfully.")

    run_streamlit()