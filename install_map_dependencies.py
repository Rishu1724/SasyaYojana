"""
Script to install dependencies for map visualization in Sasya-Mitra.
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a Python package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}: {e}")
        return False
    return True

def main():
    """Main function to install map visualization dependencies."""
    print("Installing dependencies for map visualization...")
    
    # Change to the map visualization directory
    map_dir = os.path.join("models", "map_visualization")
    if os.path.exists(map_dir):
        os.chdir(map_dir)
        print(f"Changed to directory: {os.getcwd()}")
    else:
        print(f"Directory {map_dir} not found. Installing from current directory.")
    
    # Read requirements from file
    requirements_file = "requirements.txt"
    if os.path.exists(requirements_file):
        try:
            with open(requirements_file, 'r') as f:
                packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            print(f"Found {len(packages)} packages to install:")
            for package in packages:
                print(f"  - {package}")
            
            # Install each package
            failed_packages = []
            for package in packages:
                if not install_package(package):
                    failed_packages.append(package)
            
            if failed_packages:
                print(f"\nFailed to install the following packages:")
                for package in failed_packages:
                    print(f"  - {package}")
                print("\nPlease install these packages manually.")
            else:
                print("\nAll map visualization dependencies installed successfully!")
                
        except Exception as e:
            print(f"Error reading requirements file: {e}")
    else:
        print(f"Requirements file {requirements_file} not found.")
        print("Installing default packages...")
        
        # Default packages if requirements file is missing
        default_packages = [
            "folium>=0.12.0",
            "geopandas>=0.9.0",
            "shapely>=1.7.0"
        ]
        
        failed_packages = []
        for package in default_packages:
            if not install_package(package):
                failed_packages.append(package)
        
        if failed_packages:
            print(f"\nFailed to install the following packages:")
            for package in failed_packages:
                print(f"  - {package}")
        else:
            print("\nDefault map visualization dependencies installed successfully!")

if __name__ == "__main__":
    main()