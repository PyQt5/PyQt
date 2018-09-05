from ctypes import CDLL
dll = CDLL('ScreenShot.dll')
dll.PrScrn()
