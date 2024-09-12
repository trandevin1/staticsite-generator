from textnode import TextNode
import os
import shutil


def main():
    node1 = TextNode("Some text", "type1", "www.testurl.com")


def copy(source, destination):
    # first delete all contents of the destination directory first
    if os.path.exists(destination):
        # if this exists then delete it:
        shutil.rmtree(destination)

    os.mkdir(destination)

    directories = []

    current_directory = os.listdir(source)

    for file in current_directory:
        folder = os.path.join(source, file)
        if not os.path.isfile(folder):
            directories.append(file)
        else:
            print(f"copying {file} from {source} to {destination}")
            shutil.copy(folder, destination)

    # print(directories)
    for directory in directories:
        copy(os.path.join(source, directory), os.path.join(destination, directory))

    return 0


if __name__ == "__main__":
    copy(
        "/home/tran/Projects/boot_dev/staticsite/static",
        "/home/tran/Projects/boot_dev/staticsite/public",
    )
