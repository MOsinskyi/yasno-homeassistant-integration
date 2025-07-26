class JSONHandler():
    def __init__(self, filename: str) -> None:
        self._filename: str = filename

    @property
    def is_empty(self) -> bool:
        return not os.path.exists(self._filename) \
                or os.path.getsize(self._filename) == 0

    def read(self) -> any:
        with open(self._filename, "r") as f:
            loaded_data: any = json.load(f)

        return loaded_data

    def write(self, data: any) -> None:
        with open(self._filename, "w") as f:
            json.dump(data, f, indent=4)
