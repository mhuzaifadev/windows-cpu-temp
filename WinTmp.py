import os
import sys
import clr
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('temp_monitor.log'),
        logging.StreamHandler()
    ]
)

def get_dll_path():
    """Get the path to the LibreHardwareMonitorLib.dll."""
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent
    
    return str(base_path / 'WinTmp' / 'LibreHardwareMonitorLib.dll')

# Initialize the hardware monitor
try:
    dll_path = get_dll_path()
    logging.info(f"Loading DLL from: {dll_path}")
    
    if not os.path.exists(dll_path):
        raise FileNotFoundError(f"LibreHardwareMonitorLib.dll not found at {dll_path}")
    
    clr.AddReference(dll_path)
    from LibreHardwareMonitor import Hardware
    
    # Create computer instance
    computer = Hardware.Computer()
    computer.IsCpuEnabled = True
    computer.IsGpuEnabled = True
    computer.Open()
    
    logging.info("Hardware monitor initialized successfully")
except Exception as e:
    logging.error(f"Failed to initialize hardware monitor: {str(e)}")
    raise

def update_sensors():
    """Update all sensor readings."""
    try:
        computer.Update()
    except Exception as e:
        logging.error(f"Error updating sensors: {str(e)}")
        raise

def get_cpu_temperature():
    """Get the CPU temperature."""
    try:
        update_sensors()
        for hardware in computer.Hardware:
            if hardware.HardwareType == Hardware.HardwareType.Cpu:
                for sensor in hardware.Sensors:
                    if sensor.SensorType == Hardware.SensorType.Temperature:
                        return sensor.Value
        return None
    except Exception as e:
        logging.error(f"Error getting CPU temperature: {str(e)}")
        return None

def get_gpu_temperature():
    """Get the GPU temperature."""
    try:
        update_sensors()
        for hardware in computer.Hardware:
            if hardware.HardwareType == Hardware.HardwareType.GpuNvidia or \
               hardware.HardwareType == Hardware.HardwareType.GpuAmd or \
               hardware.HardwareType == Hardware.HardwareType.GpuIntel:
                for sensor in hardware.Sensors:
                    if sensor.SensorType == Hardware.SensorType.Temperature:
                        return sensor.Value
        return None
    except Exception as e:
        logging.error(f"Error getting GPU temperature: {str(e)}")
        return None

def get_cpu_temperatures():
    """Get temperatures for all CPU cores."""
    try:
        update_sensors()
        temps = []
        for hardware in computer.Hardware:
            if hardware.HardwareType == Hardware.HardwareType.Cpu:
                for sensor in hardware.Sensors:
                    if sensor.SensorType == Hardware.SensorType.Temperature:
                        temps.append(sensor.Value)
        return temps
    except Exception as e:
        logging.error(f"Error getting CPU temperatures: {str(e)}")
        return []

def get_gpu_temperatures():
    """Get temperatures for all GPUs."""
    try:
        update_sensors()
        temps = []
        for hardware in computer.Hardware:
            if hardware.HardwareType in [Hardware.HardwareType.GpuNvidia,
                                       Hardware.HardwareType.GpuAmd,
                                       Hardware.HardwareType.GpuIntel]:
                for sensor in hardware.Sensors:
                    if sensor.SensorType == Hardware.SensorType.Temperature:
                        temps.append(sensor.Value)
        return temps
    except Exception as e:
        logging.error(f"Error getting GPU temperatures: {str(e)}")
        return []

# Export the functions
CPU_Temp = get_cpu_temperature
GPU_Temp = get_gpu_temperature
CPU_Temps = get_cpu_temperatures
GPU_Temps = get_gpu_temperatures 