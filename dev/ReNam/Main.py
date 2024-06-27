from app.interface.interface import Interface
from app.classes.APIFetcher import APIFetcher

from app.classes.handlers.config_handler import ConfigHandler
from app.classes.handlers.interface_handler import InterfaceHandler
from app.classes.handlers.directory_handler import DirectoryHandler
from app.classes.handlers.midia_handler import MidiaEnum


class Main():

    def __init__(self) -> None:
        self.is_running: bool = True

        self.on_init()

   
    def on_init(self) -> None:

        self.configs = ConfigHandler(self)
        self.interface_handler = InterfaceHandler(self)
        self.directory_handler = DirectoryHandler(self)
        self.midia_handler = MidiaEnum
        self.api_fetcher = APIFetcher(self)


        self.interface = Interface(self)
        

    def run(self) -> None:
        while self.is_running:

            self.interface.menu()


    def quit(self) -> None:
        self.is_running = False

        quit("\nByeBye from ReNam v0.5!")


    def update(self) -> None:
        self.configs.update()
        self.interface_handler.update()
        self.directory_handler.update()
        self.api_fetcher.update()


if __name__ == '__main__':
    app = Main()
    app.run()
