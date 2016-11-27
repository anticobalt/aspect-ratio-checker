from PIL import Image  # Pillow Module
import sys
import subprocess
import ctypes
import os
import pickle

def main():
    """
    :return: NoneType
    """
    try:
        file = sys.argv[1]
        if not same_ratio(get_image_ratio(file), get_monitor_ratio(), file):
            prompt_edit(file)
    except:
        print("No image chosen.")
        n = input("Press enter to exit.")


def get_image_ratio(file):
    """
    :param file: str
    :return: float
    """
    img = Image.open(file)
    x = img.size[0]
    y = img.size[1]
    print("Image is", x, "by", y)
    return x/y


def get_monitor_ratio():
    """
    :return: float
    """
    user = ctypes.windll.user32
    user.SetProcessDPIAware()
    x = user.GetSystemMetrics(0)
    y = user.GetSystemMetrics(1)
    print("Screen is", x, "by", y)
    return x / y


def same_ratio(img_ratio, monitor_ratio, file):
    """
    :param img_ratio: float
    :param monitor_ratio: float
    :param file: str
    :return: bool
    """
    percent = img_ratio / monitor_ratio
    diff = int(abs(percent - 1) * 100)
    if percent > 1:
        print("Image is " + str(diff) + "% too wide for screen.")
        same = False
    elif percent < 1:
        print("Image is " + str(diff) + "% too narrow for screen.")
        same = False
    else:
        print("Image is the same aspect ratio as the screen.")
        n = input("Press enter to exit.")
        same = True
    return same


def prompt_edit(file):
    """
    :param file: str
    :return: NoneType
    """
    a = input("Open in image editor? Y/N ").lower()
    if 'y' in a:
        subprocess.call([get_editor(),file])


def get_editor():
    p = os.path.join(os.getenv('APPDATA'), "AspectRatioChecker\preferences.pkl")
    f = open(p, "rb")
    return pickle.load(f)[1]
        
main()
