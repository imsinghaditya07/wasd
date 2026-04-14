import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.app_window import SilentBridgeApp

if __name__ == "__main__":
    app = SilentBridgeApp()
    app.run()
