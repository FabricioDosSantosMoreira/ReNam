from app.Interface import Interface
from handlers.ConfigsHandler import ConfigHandler


class Main():

    def __init__(self) -> None:
        self.is_running: bool = True
        self.configs = ConfigHandler()

        self.interface = Interface(self)
        


    def run(self) -> None:
        while self.is_running:
            self.interface.menu()

        quit('Bye Bye from ReNam!')


    def update(self) -> None:
        self.run()


if __name__ == '__main__':
    app = Main()
    app.run()
