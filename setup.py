import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path

def download_file(url, filename):
    """Download a file from a URL."""
    print(f"Downloading {filename}...")
    urllib.request.urlretrieve(url, filename)
    print("Download complete!")

def extract_zip(zip_path, extract_to):
    """Extract a zip file to a directory."""
    print(f"Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("Extraction complete!")

def setup_librehardwaremonitor():
    """Set up LibreHardwareMonitorLib and its dependencies."""
    # Create WinTmp directory if it doesn't exist
    wintmp_dir = Path("WinTmp")
    wintmp_dir.mkdir(exist_ok=True)

    # Download LibreHardwareMonitor from NuGet
    nuget_url = "https://www.nuget.org/api/v2/package/LibreHardwareMonitorLib/0.9.3"
    zip_path = "LibreHardwareMonitorLib.zip"
    
    try:
        # Download and extract LibreHardwareMonitorLib
        download_file(nuget_url, zip_path)
        extract_zip(zip_path, "temp_extract")
        
        # Copy the DLL and its dependencies
        dll_path = Path("temp_extract/lib/netstandard2.0/LibreHardwareMonitorLib.dll")
        if dll_path.exists():
            shutil.copy2(dll_path, wintmp_dir / "LibreHardwareMonitorLib.dll")
            print("DLL copied successfully!")
        else:
            print("Error: DLL not found in extracted files")
            return False

        # Download and copy required .NET dependencies
        dependencies = {
            "System.IO.FileSystem.AccessControl": "5.0.0",
            "System.Security.Principal.Windows": "5.0.0",
            "System.Security.AccessControl": "5.0.0",
            "Microsoft.Win32.Registry": "5.0.0"
        }

        for dep_name, dep_version in dependencies.items():
            dep_url = f"https://www.nuget.org/api/v2/package/{dep_name}/{dep_version}"
            dep_zip = f"{dep_name}.zip"
            
            try:
                download_file(dep_url, dep_zip)
                extract_zip(dep_zip, f"temp_{dep_name}")
                
                # Copy the DLL from the extracted package
                dep_dll = Path(f"temp_{dep_name}/lib/netstandard2.0/{dep_name}.dll")
                if dep_dll.exists():
                    shutil.copy2(dep_dll, wintmp_dir / f"{dep_name}.dll")
                    print(f"{dep_name} DLL copied successfully!")
                else:
                    print(f"Error: {dep_name} DLL not found in extracted files")
                
                # Clean up
                os.remove(dep_zip)
                shutil.rmtree(f"temp_{dep_name}")
            except Exception as e:
                print(f"Error processing {dep_name}: {str(e)}")
                continue
            
        # Clean up
        os.remove(zip_path)
        shutil.rmtree("temp_extract")
        return True
        
    except Exception as e:
        print(f"Error during setup: {str(e)}")
        return False

if __name__ == "__main__":
    print("Setting up LibreHardwareMonitor...")
    if setup_librehardwaremonitor():
        print("Setup completed successfully!")
    else:
        print("Setup failed!")
        sys.exit(1) 