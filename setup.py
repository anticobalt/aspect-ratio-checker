import pickle
import time
import os
import shutil


class Setup:

    def __init__(self):

        self.wd = os.path.dirname(os.path.realpath(__file__))
        self.roaming = os.getenv('APPDATA')
        self.appdata = os.path.join(self.roaming, "AspectRatioChecker")
        self.save_address = os.path.join(self.appdata, "preferences.pkl")
        self.menu_location = os.path.join(self.roaming, "Microsoft\Windows\SendTo")
        
        self.mobile = "arc-mobile.py"
        self.cmd = "AspectRatioChecker.bat"
        self.org = "arc.py"

        try:
            self.load()
        except FileNotFoundError:
            self.in_menu = False
            self.editor = "C:\WINDOWS\system32\mspaint.exe"
        finally:
            try:
                if not os.path.exists(self.appdata):
                    os.mkdir(self.appdata)
                    exe = os.path.join(self.wd, self.cmd)
                    with open(exe, "w") as f:
                        f.write("@echo off\n")
                        f.write("cls\n")
                        f.write("python " + os.path.join(self.appdata, self.mobile) + " %1\n")
                    for file in [self.cmd, self.org]:
                        src = os.path.join(self.wd, file)
                        shutil.move(src, self.appdata)
                        if file == self.org:
                            os.rename(os.path.join(self.appdata, file), os.path.join(self.appdata, self.mobile))
                            shutil.copy(os.path.join(self.appdata, self.mobile), self.wd)
                            os.rename(os.path.join(self.wd, self.mobile), src)
                    self.menu_add(alert=False)
                    self.save()
                    print("Initial setup complete.")
                    print()
            except FileNotFoundError:
                print("Required source files missing.")

    def main(self):

        while 1:
            options = ["Add to context menu", "Remove from context menu", "Set default editor", "Check status", "Exit"]
            operations = [self.menu_add, self.menu_remove, self.set_editor, self.check]
            num = 1
            print("Choose an option:")
            for option in options:
                print(num, option)
                num += 1
            choice = input(">> ")
            print()
            try:
                if int(choice) in range(1, len(options)):
                    operations[int(choice) - 1]()
                elif int(choice) == len(options):
                    self.save()
                    break
            except ValueError:
                pass
            print()

    def menu_add(self, alert=True):

        if self.in_menu:
            print("Already in context menu.")
        else:
            src = os.path.join(self.appdata, self.cmd)
            shutil.move(src, self.menu_location)
            self.in_menu = True
            if alert:
                print("Added.")

    def menu_remove(self):

        if self.in_menu:
            f = os.path.join(self.menu_location, self.cmd)
            shutil.move(f, self.appdata)
            self.in_menu = False
            print("Removed.")
        else:
            print("Not in context menu.")

    def set_editor(self):

        program = input("Gimp 2.8 (1) or Paint (2)? ")
        if program == "1":
            self.editor = os.path.join("C:\Program Files\GIMP 2", "bin\gimp-2.8.exe")
        else:
            self.editor = "C:\WINDOWS\system32\mspaint.exe"
            if program != "2":
                print()
                print("Paint it is.")
                time.sleep(1)
        print("Editor set.")

    def check(self):

        print("In Context Menu:", self.in_menu)
        print("Editor Location:", self.editor)
        print("Context Menu Location:", self.menu_location)
        print("Program Location:", self.appdata)

    def save(self):

        data = (self.in_menu, self.editor)
        f = open(self.save_address, "wb")
        pickle.dump(data, f)

    def load(self):

        f = open(self.save_address, "rb")
        self.in_menu, self.editor = pickle.load(f)

s = Setup()
s.main()
