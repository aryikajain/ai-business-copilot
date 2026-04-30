import os

BASE_PATH = "data/uploads"


def save_file(user_id: str, file):
    user_folder = os.path.join(BASE_PATH, user_id)
    os.makedirs(user_folder, exist_ok=True)

    file_path = os.path.join(user_folder, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path