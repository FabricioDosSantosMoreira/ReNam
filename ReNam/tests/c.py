    def rename(self, files: List[Path], info: List[str]) -> None:
         
        
         
        root_path: Path = files[0].parent
        files_name: List[str] = self.app.directory_handler.get_path_name(files)


        result, total_results = self.extract_eps_order(files=files_name, patterns=self.regex_patterns)
        if total_results != len(files):
            print(f"\n'extract_eps_order' dindn't work. 1")
            return None


        episodes_info: List[str] = []
        for i, episode in enumerate(info):
            
            season = ""
            if len(str(episode[2])) <= 1:
                season = "0" + str(episode[2]) 
            else:
                season = str(episode[2])

            episode_str = ""
            if len(str(episode[1])) <= 1:
                episode_str = "0" + str(episode[1]) 
            else:
                episode_str = str(episode[1])

            episodes_info.append(f"S{season}E{episode_str} - {episode[0]}")
        
        episodes, total_results = self.extract_eps_order(files=episodes_info, patterns=[re.compile("E(\\d+)")])
        if total_results != len(episodes_info):
            print(f"\n'extract_eps_order' dindn't work. 2")
            return None


        new_names: List = []
        for key in result.keys():
            name = episodes.get(key, [])[0]
            if name:
                new_names.append(name)

        episodes, total_results = self.extract_eps_order(files=new_names, patterns=[re.compile("E(\\d+)")])
        if total_results != len(result):
            print(f"\n'extract_eps_order' dindn't work. 3")
            return None

        if len(result) != len(episodes):
            print(f"not enough correspondencies")
            return None


        old_paths: List[Path] = []
        new_paths: List[Path] = []
        old_names: List[str] = []
        new_names: List[str] = []
        for key, values in result.items():
            for value in values:
                old_name = self.app.directory_handler.get_path_name(paths=[value])[0]
                suffix = self.app.directory_handler.get_path_suffix(paths=[old_name])[0]
                new_name = f"{self.title} {episodes.get(key, [])[0]}{suffix}"
                new_name = re.sub(r'[<>:"/\\|?*]', '', new_name)

                old_path = Path(root_path / old_name)
                new_path = Path(root_path / new_name)

                old_paths.append(old_path)
                new_paths.append(new_path)
                old_names.append(old_name)
                new_names.append(new_name)


        if len(old_paths) != len(new_paths):
            print("Couldn't rename. Missing paths correspondencies")

        interface = self.app.interface_handler

        HEADERS = ["OLD FILE NAMES", "NEW FILES NAMES"]
        CONTENTS = []
        for i in range(len(old_paths)):
            CONTENTS.append([old_names[i], new_names[i]])

        interface.display_interface(headers=HEADERS, contents=CONTENTS)
        value = input("press y to rename, else cancel: ")

        if str(value).lower() == "y":
            for i in range(len(old_paths)):
                if old_paths[i].exists():
                    os.rename(old_paths[i], new_paths[i])
                else:
                    print(f"{old_paths[i]} does not exist")
