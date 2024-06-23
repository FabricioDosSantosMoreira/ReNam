from app.Interface import Interface
from handlers.ConfigsHandler import ConfigHandler
from handlers.InterfaceHandler import InterfaceHandler
from handlers.DirectoryHandler import DirectoryHandler
from handlers.MidiaHandler import MidiaEnum
from classes.APIFetcher import APIFetcher


class Main():

    def __init__(self) -> None:
        self.is_running: bool = True

        self.on_init()

        
    def on_init(self) -> None:
        # Handlers
        self.configs = ConfigHandler(self)
        self.interface_handler = InterfaceHandler(self)
        self.directory_handler = DirectoryHandler(self)
        self.midia_handler = MidiaEnum
        self.api_fetcher = APIFetcher(self)

        # Interface
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
        self.run()


if __name__ == '__main__':
    app = Main()
    app.run()
