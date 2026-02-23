"""
App Controller
Central bridge between Frontend (Tabs) and Backend (Services)
"""

from typing import Optional
from backend.services.device_service import DeviceService


class AppController:
    """Main application controller (bridge layer)"""

    def __init__(self):
        self.device_service: Optional[DeviceService] = DeviceService()
        self.ps2_service = None
        self.ps1_service = None

    # =============================
    # DEVICE OPERATIONS
    # =============================

    def get_available_devices(self):
        """Return list of detected storage devices"""
        if not self.device_service:
            return []

        try:
            devices = self.device_service.list_devices()
            return devices or []
        except Exception as e:
            print(f"[AppController] Device error: {e}")
            return []

    # =============================
    # PS2 OPERATIONS (placeholder)
    # =============================

    def write_ps2_game(self, iso_path: str, target_device: str):
        if not self.ps2_service:
            print("[AppController] PS2 service not available")
            return False

        try:
            return self.ps2_service.write_game(iso_path, target_device)
        except Exception as e:
            print(f"[AppController] PS2 write error: {e}")
            return False

    # =============================
    # PS1 OPERATIONS (placeholder)
    # =============================

    def write_ps1_game(self, bin_path: str, target_device: str):
        if not self.ps1_service:
            print("[AppController] PS1 service not available")
            return False

        try:
            return self.ps1_service.write_game(bin_path, target_device)
        except Exception as e:
            print(f"[AppController] PS1 write error: {e}")
            return False