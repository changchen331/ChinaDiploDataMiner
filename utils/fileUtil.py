def write_file_start(path_to_file, data):
    with open(path_to_file, 'w', encoding='utf-8') as file:
        file.write(data)


def write_file(path_to_file, data):
    with open(path_to_file, 'a', encoding='utf-8') as file:
        file.write(data)