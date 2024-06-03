from ReNam.handlers.DirectoryHandler import DirectoryHandler
from ReNam.handlers.ConfigsHandler import ConfigHandler


from pathlib import Path


config_data = {
        "first_path_occurrence": False,
        "num_of_processes": 100,
        "drives": ["C:/", "D:/"],
        "excluded_paths": [Path("C:/Windows"), Path("C:/MinGW"), Path("C:/Program Files"),  Path("C:/ProgramData"), Path("C:/ProgramData/Microsoft")]
    }


c = ConfigHandler(config_data)
d = DirectoryHandler(c)


#paths = "C:\XboxGames\GameSave\wgs"
path = "C:\\Users\\fabri\\OneDrive\\Área de Trabalho\\DIO\\Cursos\\01 - Python - Python AI Backend Developer\\01 - Git e GitHub - Desenvolvimento Colaborativo com Git e GitHub"

# path = "Downloads"

#path = "C:\\Users\\fabri\\OneDrive\\Área de Trabalho\\ReNam\\ReNam v0.5\\app"
p = Path(path)
print(p)


paths = d.search_drives(path=p)
print(paths)

lista_paths = d.get_directory_files(paths[0])

for path in lista_paths:
    print(d.get_path_name([path]))
    print(d.get_path_suffix([path]))