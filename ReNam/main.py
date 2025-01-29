from app.classes.handlers.config_handler import ConfigHandler
from app.classes.handlers.interface_handler import InterfaceHandler
from app.classes.handlers.directory_handler import DirectoryHandler

from app.classes.APIFetcher import APIFetcher

from app.interface.interface import Interface


class Main():

    def __init__(self) -> None:
        self.is_running: bool = True

        self.on_init()

   
    def on_init(self) -> None:
        # Handlers
        self.config_handler = ConfigHandler(self)
        self.interface_handler = InterfaceHandler(self)
        self.directory_handler = DirectoryHandler(self)

        # API Fetcher
        self.api_fetcher = APIFetcher(self)

        # Interface
        self.interface = Interface(self)
        

    def run(self) -> None:
        while self.is_running:

            self.interface.menu()


    def quit(self) -> None:
        self.is_running = False

        quit("\nByeBye from ReNam v0.0.1!")


    def update(self) -> None:
        self.config_handler.update()
        self.interface_handler.update()
        self.directory_handler.update()
        self.api_fetcher.update()


if __name__ == '__main__':
    app = Main()
    app.run()
