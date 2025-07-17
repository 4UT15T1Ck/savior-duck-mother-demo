import sys
import os
import json
from play import Play

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def create_shortcut_once():
    try:
        import winshell
        config_file = os.path.join(os.getenv("APPDATA"), "savior_duck_mother_config.json")

        if os.path.exists(config_file):
            return

        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "SaviorDuckMother.lnk")
        target = sys.executable

        if not os.path.exists(shortcut_path):
            with winshell.shortcut(shortcut_path) as link:
                link.path = target
                link.description = "Mama duck saving em ducklings!!!"
                link.icon_location = (target, 0)

        with open(config_file, "w") as f:
            json.dump({"shortcut_created": True}, f)

    except ImportError:
        pass


if __name__ == "__main__":
    create_shortcut_once()
    Play()
