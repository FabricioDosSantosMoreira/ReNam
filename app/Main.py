from DirectoryHandler import DirectoryHandler
from MidiaHandler import MidiaHandler
from Interface import Interface 


class Main():
    def __init__(self):
        self.is_running = True


    def run(self):
        if self.is_running:

            self.DH = DirectoryHandler()
            self.MH = MidiaHandler()

            self.interface = Interface()
            self.interface.menu()


if __name__ == "__main__":
    app = Main() 
    app.run()
