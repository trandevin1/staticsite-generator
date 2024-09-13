from block_markdown import markdown_to_html_node, extract_title
import os
import shutil


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


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    markdown = ""
    template = ""

    with open(from_path, "r") as file:
        markdown = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    """ print(markdown)
    print("\n\n\n")
    print(template)
 """
    res = markdown_to_html_node(markdown).to_html()

    # print(res)

    title = extract_title(markdown)
    # print(title)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", res)
    # print(template)

    # grab the directories
    destination = os.path.dirname(dest_path)

    # check to see if the destination directory already exists
    if not os.path.exists(destination):
        os.makedirs(destination)

    with open(dest_path, "w") as file:
        file.write(template)

    return None


def main():
    static_path = "/home/tran/Projects/boot_dev/staticsite/static"
    public_path = "/home/tran/Projects/boot_dev/staticsite/public"
    source_path = "/home/tran/Projects/boot_dev/staticsite/content/index.md"
    template_path = "/home/tran/Projects/boot_dev/staticsite/template.html"
    dest_path = "/home/tran/Projects/boot_dev/staticsite/public/index.html"

    copy(static_path, public_path)
    generate_page(source_path, template_path, dest_path)


if __name__ == "__main__":
    main()
