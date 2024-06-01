from app.Interface import Interface
from handlers.ConfigsHandler import ConfigHandler
from handlers.InterfaceHandler import InterfaceHandler


class Main():

    def __init__(self) -> None:
        self.is_running: bool = True
        
        self.configs = ConfigHandler()
        

    def om_init(self) -> None:
        self.interface = Interface(self)
        self.interface_handler = InterfaceHandler(self)


    def run(self) -> None:
        while self.is_running:

            self.interface.menu()


    def quit(self) -> None:
        self.is_running = False

        quit("\nByeBye from ReNam v0.5!")


    def update(self) -> None:
        self.configs.update()
        self.interface_handler.update()
        self.run()


if __name__ == '__main__':
    app = Main()
    app.run()
