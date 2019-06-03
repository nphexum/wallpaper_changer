import pythoncom
from win32com.shell import shell, shellcon


def invoke(image):
    pythoncom.CoInitialize()
    iad = pythoncom.CoCreateInstance(shell.CLSID_ActiveDesktop, None,
                                     pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IActiveDesktop)
    iad.SetWallpaper(image, 0)
    iad.ApplyChanges(shellcon.AD_APPLY_ALL)
