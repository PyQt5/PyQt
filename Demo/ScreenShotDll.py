from ctypes import CDLL

dll = CDLL('Data/ScreenShot.dll')
dll.PrScrn()
