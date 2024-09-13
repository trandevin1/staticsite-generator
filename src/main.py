from block_markdown import markdown_to_html_node, extract_title
import os
import shutil
from pathlib import Path


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
            print(f"Copying {file} from {source} to {destination}")
            shutil.copy(folder, destination)

    for directory in directories:
        copy(os.path.join(source, directory), os.path.join(destination, directory))

    return 0


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {os.path.relpath(from_path)} to {os.path.relpath(dest_path)} using {os.path.relpath(template_path)}."
    )

    markdown = ""
    template = ""

    with open(from_path, "r") as file:
        markdown = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    res = markdown_to_html_node(markdown).to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", res)

    # grab the directories
    destination = os.path.dirname(dest_path)

    # check to see if the destination directory already exists
    if not os.path.exists(destination):
        os.makedirs(destination)

    with open(dest_path, "w") as file:
        file.write(template)

    return 0


def rename_file(path, ext):
    path = Path(path)
    new_file_path = path.with_suffix("." + ext)
    path.rename(new_file_path)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content = os.listdir(dir_path_content)

    directory = []

    for file in content:

        if os.path.isfile(os.path.join(dir_path_content, file)):
            from_path = os.path.join(dir_path_content, file)
            dest_path = os.path.join(dest_dir_path, file)
            generate_page(
                from_path,
                template_path,
                dest_path,
            )
            rename_file(dest_path, "html")

        else:
            directory.append(file)

    for folder in directory:
        generate_pages_recursive(
            os.path.join(dir_path_content, folder),
            template_path,
            os.path.join(dest_dir_path, folder),
        )


def main():
    static_path = "/home/tran/Projects/boot_dev/staticsite/static"
    public_path = "/home/tran/Projects/boot_dev/staticsite/public"
    source_path = "/home/tran/Projects/boot_dev/staticsite/content"
    template_path = "/home/tran/Projects/boot_dev/staticsite/template.html"
    dest_path = "/home/tran/Projects/boot_dev/staticsite/public"

    copy(static_path, public_path)
    generate_pages_recursive(source_path, template_path, dest_path)


if __name__ == "__main__":
    main()
