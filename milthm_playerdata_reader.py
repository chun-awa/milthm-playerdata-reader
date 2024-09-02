import ctypes
import sys
import os
import xml.etree.ElementTree
import base64

try:
    import winreg
except ModuleNotFoundError:
    pass


def get_win():
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Morizero\\Milthm") as key:
        i = 0
        while True:
            try:
                name, data, _ = winreg.EnumValue(key, i)
                if "PlayerFile" in name:
                    return data.decode()
                i += 1
            except OSError:
                break


def get_linux():
    config_path = os.getenv(
        "XDG_CONFIG_HOME", os.path.join(os.getenv("HOME", ""), ".config")
    )
    root = xml.etree.ElementTree.parse(
        os.path.join(config_path, "unity3d", "Morizero", "Milthm", "prefs")
    ).getroot()
    for i in root:
        if i.attrib["name"] == "PlayerFile":
            return base64.b64decode(i.text.encode()).decode()


if __name__ == "__main__":
    if os.name == "nt":
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
        print(get_win())
    elif os.name == "posix":
        print(get_linux())
