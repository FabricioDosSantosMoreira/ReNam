import os
from abc import ABC, abstractmethod
from collections.abc import Iterator
from multiprocessing.pool import ApplyResult, ThreadPool
from pathlib import Path
from typing import List, Union

import scandir

from handlers.ConfigsHandler import ConfigHandler


class DirectoryHandler():

    __absolute_path_found: bool = False

    def __init__(self, configs: ConfigHandler) -> None:

        self._first_path_occurrence: bool
        self._num_of_processes: int

        self._drives: List[Path]
        self._excluded_paths: List[Path]

        self.paths: List[Path]
        self.selected_path: Path

        self.update_configs(configs=configs)


    def update_configs(self, *, configs: ConfigHandler) -> None:

        self.first_path_occurrence = configs.get_config("first_path_occurrence")
        self.num_of_processes = configs.get_config("num_of_processes")

        self.drives = configs.get_config("drives")
        self.excluded_paths = configs.get_config("excluded_paths")

        self.selected_path = configs.get_config("selected_path")


    @staticmethod
    def get_drives() -> list[Path]:
        drives: list[Path] = []

        for drive in DriveIterator(os.listdrives()):
            drives.append(drive)

        return drives


    @staticmethod
    def get_directory_files(path: Path) -> List[Path]:
        files: List[Path] = []

        try:
            for file in path.iterdir():
                if file.is_file():
                    files.append(file)

            return files

        # TODO: Arrumar isso
        except PermissionError as e:
            print(f"\nPermissionError {e}")
        except NotADirectoryError as e:
            print(f"\nNotADirectoryError {e}")
        except FileNotFoundError as e:
            print(f"\nFileNotFoundError {e}")
        except Exception as exc:
            print(f"\nException {exc}")


    @staticmethod
    def get_path_name(paths: List[Path]) -> List[str]:
        names: List[str] = []

        for path in PathIterator(paths):
            names.append(path.name)

        return names


    @staticmethod
    def get_path_suffix(paths: List[Path]) -> List[str]:
        suffixes: List[str] = []

        for path in PathIterator(paths):
            suffixes.append(path.suffix)

        return suffixes


    def search_drives(self, path: Path) -> Union[List[Path], None]:

        self.absolute_path_found = False

        thread_pool = ThreadPool(processes=self.num_of_processes)
        async_results: list[ApplyResult] = []

        for drive in DriveIterator(self.drives):
            async_result = thread_pool.apply_async(
                self.__search_drive,
                args=(
                    path,
                    drive,
                ),
            )
            async_results.append(async_result)

        # Wait for all async results to finish.
        thread_pool.close()
        thread_pool.join()

        search_results: list[Path] = []

        for async_result in async_results:
            result = async_result.get()
            if result is not None:

                for sub_result in result:
                    if sub_result is not None:
                        search_results.append(sub_result)

        for exc_path in PathIterator(self.excluded_paths):
            for path in PathIterator(search_results):
                if path.is_relative_to(exc_path):
                    search_results.remove(path)

                break

        return search_results


    def __search_drive(self, path: Path, drive: Path) -> Union[List[Path], None]:

        # Verify if 'path' is absolute, if 'path' exists and if 'path' is in the same drive as 'drive'
        if path.is_absolute() and path.exists() and path.anchor == drive.anchor:
            self.absolute_path_found = True
            return [path]

        _paths: list[Path] = []
        for dirpath, dirnames, filenames in scandir.walk(drive):
            if self.absolute_path_found:
                break

            for dirname in PathIterator(dirnames):

                if path.is_relative_to(dirname):

                    if self.first_path_occurrence:
                        return [Path(os.path.join(dirpath, path))]

                    else:
                        _paths.append(Path(os.path.join(dirpath, path)))

        return _paths


    @property
    def absolute_path_found(self) -> bool:
        return self.__absolute_path_found

    @absolute_path_found.setter
    def absolute_path_found(self, value: bool) -> None:
        self.__absolute_path_found = value

    @property
    def first_path_occurrence(self) -> bool:
        return self._first_path_occurrence

    @first_path_occurrence.setter
    def first_path_occurrence(self, value: bool) -> None:
        self._first_path_occurrence = value

    @property
    def num_of_processes(self) -> int:
        return self._num_of_processes

    @num_of_processes.setter
    def num_of_processes(self, value: int) -> None:
        self._num_of_processes = value

    @property
    def drives(self) -> List[Path]:
        return self._drives

    @drives.setter
    def drives(self, value: List[Path]) -> None:
        self._drives = value

    @property
    def excluded_paths(self) -> List[Path]:
        return self._excluded_paths

    @excluded_paths.setter
    def excluded_paths(self, value: List[Path]) -> None:
        self._excluded_paths = value


class GenericIterator(ABC):

    __counter: int = 0

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

    @property
    def counter(self) -> int:
        return self.__counter

    @counter.setter
    def counter(self, value: int) -> None:
        self.__counter = value


class PathIterator(GenericIterator, Iterator[Path, str]):

    def __init__(self, paths: List[Union[Path, str]]) -> None:
        self._paths: List[Union[Path, str]] = paths

    def __iter__(self) -> 'PathIterator':
        return self

    def __next__(self) -> Path:
        try:
            path = Path(self._paths[self.counter])
            return path

        except IndexError:
            raise StopIteration

        finally:
            self.counter += 1


class DriveIterator(GenericIterator, Iterator[Path, str]):

    def __init__(self, drives: List[Union[Path, str]]) -> None:
        self._drives: List[Union[Path, str]] = drives

    def __iter__(self) -> 'DriveIterator':
        return self

    def __next__(self) -> Path:
        try:
            drive = Path(self._drives[self.counter])
            return drive

        except IndexError:
            raise StopIteration

        finally:
            self.counter += 1
