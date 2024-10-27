file_path = "путь_к_вашему_файлу.txt"


def read(file_path, message):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if message == "1":
            return (list(map(int, lines[0].split())))
        if message == "2":
            return (list(map(int, lines[0].split())))
            return (list(map(int, lines[1].split())))
