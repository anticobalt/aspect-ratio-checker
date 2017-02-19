import pickle
import time
import os
import shutil


def main():
    s = Setup()
    s.startup()
    s.main_loop()


class Setup:

    def __init__(self):

        self.WORKINGDIR = os.path.dirname(os.path.realpath(__file__))
        self.ROAMINGDIR = os.getenv('APPDATA')
        self.APPDATADIR = os.path.join(self.ROAMINGDIR, "AspectRatioChecker")
        self.RIGHTMENUDIR = os.path.join(self.ROAMINGDIR, "Microsoft\Windows\SendTo")

        self.SAVEFILE = os.path.join(self.APPDATADIR, "preferences.pkl")
        self.MOBILEFILE = os.path.join(self.APPDATADIR, "arc-mobile.py")

        self.ORIGINALFILENAME = "arc.py"
        self.BATCHFILENAME = "AspectRatioChecker.bat"

        self.in_menu = False
        self.editor = "C:\WINDOWS\system32\mspaint.exe"
        self.batch_file = os.path.join(self.APPDATADIR, self.BATCHFILENAME)

    def startup(self):

        try:
            self.load()
        except FileNotFoundError:
            pass

        if self.in_menu:
            self.batch_file = os.path.join(self.RIGHTMENUDIR, self.BATCHFILENAME)

        try:
            if not os.path.exists(self.APPDATADIR):
                os.mkdir(self.APPDATADIR)
                self.handle_files()
                self.save()
                print("Initial setup complete.")
                print()
        except FileNotFoundError:
            print("Required source files missing.")

    def handle_files(self):

        with open(self.batch_file, "w") as f:
            f.write("@echo off\n")
            f.write("cls\n")
            f.write("python " + os.path.join(self.APPDATADIR, self.MOBILEFILE) + " %1\n")
        src = os.path.join(self.WORKINGDIR, self.ORIGINALFILENAME)
        shutil.copy(src, self.APPDATADIR)
        os.rename(os.path.join(self.APPDATADIR, self.ORIGINALFILENAME), self.MOBILEFILE)

    def main_loop(self):

        while 1:
            options = ["Add to context menu", "Remove from context menu", "Set default editor", "Check status",
                       "Update files", "Exit"]
            operations = [self.menu_add, self.menu_remove, self.set_editor, self.check, self.update]
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
            shutil.move(self.batch_file, self.RIGHTMENUDIR)
            self.in_menu = True
            self.batch_file = os.path.join(self.RIGHTMENUDIR, self.BATCHFILENAME)
            if alert:
                print("Added.")

    def menu_remove(self):

        if self.in_menu:
            shutil.move(self.batch_file, self.APPDATADIR)
            self.in_menu = False
            self.batch_file = os.path.join(self.APPDATADIR, self.BATCHFILENAME)
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
        print("Context Menu Location:", self.RIGHTMENUDIR)
        print("Program Location:", self.APPDATADIR)

    def save(self):

        data = (self.in_menu, self.editor)
        with open(self.SAVEFILE, "wb") as f:
            pickle.dump(data, f)

    def load(self):

        with open(self.SAVEFILE, "rb") as f:
            self.in_menu, self.editor = pickle.load(f)

    def update(self):

        for file in [self.MOBILEFILE, self.batch_file, self.SAVEFILE]:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass
        time.sleep(1)
        self.handle_files()
        self.save()
        print("Force update of files complete. You should now be running the latest code.")

main()
