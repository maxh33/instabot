"""
Device Manager for Instagram Bot
Handles both USB (physical) and network (emulator) device connections
"""
import os
import subprocess
import sys
from typing import Literal, Optional

DeviceType = Literal["usb", "network"]


class DeviceManager:
    """Manages ADB device connections for both USB and network devices"""

    def __init__(self, device_id: str):
        self.device_id = device_id
        self.device_type = self.detect_device_type(device_id)

    @staticmethod
    def detect_device_type(device_id: str) -> DeviceType:
        """
        Detect if device is USB or network based on device ID format

        USB format: alphanumeric (e.g., fbc9d1f30eb2)
        Network format: IP:port (e.g., 127.0.0.1:21533)
        """
        if ":" in device_id and "." in device_id:
            return "network"
        return "usb"

    def ensure_connected(self, logger=None) -> bool:
        """
        Ensure device is connected
        - USB devices: Just check connection
        - Network devices: Attempt connection if not connected

        Returns True if device is connected, False otherwise
        """
        def log(msg: str, level: str = "INFO"):
            if logger:
                getattr(logger, level.lower())(msg)
            else:
                print(f"{level} | {msg}")

        # Check if device is already connected
        if self.is_device_connected():
            log(f"Device {self.device_id} is already connected ({self.device_type})")
            return True

        # For network devices, attempt connection
        if self.device_type == "network":
            log(f"Network device {self.device_id} not found, attempting connection...")
            return self.connect_network_device(logger)

        # For USB devices, can't auto-connect
        log(f"USB device {self.device_id} not found. Please check USB connection.", "ERROR")
        return False

    def is_device_connected(self) -> bool:
        """Check if device is in adb devices list"""
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return self.device_id in result.stdout
        except Exception:
            return False

    def connect_network_device(self, logger=None) -> bool:
        """Connect to network device (emulator)"""
        def log(msg: str, level: str = "INFO"):
            if logger:
                getattr(logger, level.lower())(msg)
            else:
                print(f"{level} | {msg}")

        try:
            log(f"Connecting to network device: {self.device_id}")
            result = subprocess.run(
                ["adb", "connect", self.device_id],
                capture_output=True,
                text=True,
                timeout=15
            )

            if "connected" in result.stdout.lower() or "already connected" in result.stdout.lower():
                log(f"Successfully connected to {self.device_id}")
                return True
            else:
                log(f"Failed to connect: {result.stdout.strip()}", "ERROR")
                return False

        except subprocess.TimeoutExpired:
            log(f"Connection timeout for {self.device_id}", "ERROR")
            return False
        except Exception as e:
            log(f"Error connecting to device: {e}", "ERROR")
            return False

    def disconnect_network_device(self, logger=None) -> bool:
        """Disconnect network device (emulator)"""
        if self.device_type != "network":
            return True

        def log(msg: str, level: str = "INFO"):
            if logger:
                getattr(logger, level.lower())(msg)
            else:
                print(f"{level} | {msg}")

        try:
            log(f"Disconnecting network device: {self.device_id}")
            result = subprocess.run(
                ["adb", "disconnect", self.device_id],
                capture_output=True,
                text=True,
                timeout=10
            )
            log(f"Disconnect result: {result.stdout.strip()}")
            return True
        except Exception as e:
            log(f"Error disconnecting device: {e}", "WARNING")
            return False

    @staticmethod
    def list_connected_devices() -> list[tuple[str, DeviceType]]:
        """
        List all connected devices with their types
        Returns list of (device_id, device_type) tuples
        """
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True,
                timeout=10
            )

            devices = []
            for line in result.stdout.split("\n")[1:]:  # Skip header
                if "\tdevice" in line:
                    device_id = line.split("\t")[0].strip()
                    device_type = DeviceManager.detect_device_type(device_id)
                    devices.append((device_id, device_type))

            return devices
        except Exception:
            return []

    @staticmethod
    def check_adb_available() -> bool:
        """Check if ADB is installed and accessible"""
        try:
            result = subprocess.run(
                ["adb", "version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False


def load_device_from_env(account_suffix: str = "") -> Optional[str]:
    """
    Load device ID from environment variables

    Args:
        account_suffix: Optional suffix for multi-account (e.g., "_A", "_B")

    Returns:
        Device ID or None if not found

    Priority:
    1. DEVICE_{suffix} (e.g., DEVICE_A)
    2. DEVICE_ID_{suffix} (legacy)
    3. DEVICE (default)
    """
    from dotenv import load_dotenv
    load_dotenv()

    if account_suffix:
        # Try new format first
        device = os.getenv(f"DEVICE{account_suffix}")
        if device:
            return device

        # Try legacy format
        device = os.getenv(f"DEVICE_ID{account_suffix}")
        if device:
            return device

    # Fallback to default DEVICE
    return os.getenv("DEVICE")


if __name__ == "__main__":
    """Test device manager functionality"""
    print("=== Device Manager Test ===\n")

    # Check ADB
    if not DeviceManager.check_adb_available():
        print("ERROR: ADB is not installed or not in PATH")
        sys.exit(1)

    print("[OK] ADB is available\n")

    # List connected devices
    devices = DeviceManager.list_connected_devices()
    print(f"Connected devices: {len(devices)}")
    for device_id, device_type in devices:
        print(f"  - {device_id} ({device_type})")
    print()

    # Test device from .env
    device_id = load_device_from_env()
    if device_id:
        print(f"Device from .env: {device_id}")
        dm = DeviceManager(device_id)
        print(f"  Type: {dm.device_type}")
        print(f"  Connected: {dm.is_device_connected()}")

        if not dm.is_device_connected():
            print(f"  Attempting connection...")
            success = dm.ensure_connected()
            print(f"  Result: {'[OK] Success' if success else '[FAILED]'}")
    else:
        print("No DEVICE found in .env")
