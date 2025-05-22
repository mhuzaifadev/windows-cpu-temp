import sys
import os
import logging
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                            QSystemTrayIcon, QMenu, QStyle, QMessageBox)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QIcon, QFont

VERSION = "0.1.0"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('temp_monitor.log'),
        logging.StreamHandler()
    ]
)

def verify_dll():
    """Verify that required DLLs are present."""
    try:
        # Check if running as executable
        if getattr(sys, 'frozen', False):
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).parent

        dll_path = base_path / 'WinTmp' / 'LibreHardwareMonitorLib.dll'
        if not dll_path.exists():
            logging.error(f"Required DLL not found at: {dll_path}")
            return False
        return True
    except Exception as e:
        logging.error(f"Error verifying DLL: {str(e)}")
        return False

class TempWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"CPU & GPU Temperature Monitor v{VERSION}")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        
        # Verify DLL before proceeding
        if not verify_dll():
            QMessageBox.critical(
                self,
                "Error",
                "Required system files are missing. Please reinstall the application."
            )
            sys.exit(1)
            
        try:
            import WinTmp
            self.wintmp = WinTmp
        except Exception as e:
            logging.error(f"Failed to import WinTmp: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                "Failed to initialize temperature monitoring. Please check the log file."
            )
            sys.exit(1)

        self.setup_ui()
        self.setup_tray()
        self.setup_timer()
        logging.info("Application initialized successfully")

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label = QLabel("System Temperature Monitor")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title_label)

        # CPU Temperature
        self.cpu_label = QLabel("CPU Temperature: -- °C")
        self.cpu_label.setFont(QFont("Arial", 10))
        self.layout.addWidget(self.cpu_label)

        # GPU Temperature
        self.gpu_label = QLabel("GPU Temperature: -- °C")
        self.gpu_label.setFont(QFont("Arial", 10))
        self.layout.addWidget(self.gpu_label)

        # Version
        version_label = QLabel(f"Version: {VERSION}")
        version_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(version_label)

        self.setLayout(self.layout)
        self.setFixedSize(300, 150)

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        
        # Create tray menu
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show)
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(QApplication.quit)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_temps)
        self.timer.start(5000)  # Update every 5 seconds
        self.update_temps()  # Initial update

    def update_temps(self):
        try:
            cpu_temp = self.wintmp.CPU_Temp()
            gpu_temp = self.wintmp.GPU_Temp()
            
            self.cpu_label.setText(f"CPU Temperature: {cpu_temp} °C")
            self.gpu_label.setText(f"GPU Temperature: {gpu_temp} °C")
            
            # Update tray tooltip
            self.tray_icon.setToolTip(f"CPU: {cpu_temp}°C\nGPU: {gpu_temp}°C")
            logging.debug(f"Temperatures updated - CPU: {cpu_temp}°C, GPU: {gpu_temp}°C")
        except Exception as e:
            logging.error(f"Error updating temperatures: {str(e)}")
            self.cpu_label.setText("CPU Temperature: Error")
            self.gpu_label.setText("GPU Temperature: Error")
            self.tray_icon.setToolTip("Error reading temperatures")

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Temperature Monitor",
            "Application minimized to tray. Right-click the tray icon to show or quit.",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

def main():
    try:
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        
        widget = TempWidget()
        widget.show()
        
        logging.info("Application started successfully")
        sys.exit(app.exec())
    except Exception as e:
        logging.critical(f"Critical error: {str(e)}")
        QMessageBox.critical(
            None,
            "Critical Error",
            f"An unexpected error occurred: {str(e)}\nPlease check the log file for details."
        )
        sys.exit(1)

if __name__ == "__main__":
    main() 