def read_str_from_file(path: str) -> str:
    content = ""
    with open(path, "r") as f:
        content = f.read()
    return content


def write_str_on_file(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)
