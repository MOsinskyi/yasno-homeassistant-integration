class JSONHandler():
    def __init__(self, filename: str) -> None:
        self.__filename = filename

    @property
    def is_empty(self) -> bool:
        return not os.path.exists(self.__filename) or os.path.getsize(self.__filename) == 0

    def read(self) -> any:
        with open(self.__filename, "r") as f:
            loaded_data = json.load(f)
        return loaded_data

    def write(self, data: any) -> None:
        with open(self.__filename, "w") as f:
            json.dump(data, f, indent=4)
