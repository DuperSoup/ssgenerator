from other_functions import *

def main():

    source_dir = "./static"
    destination_dir = "./public"

    copy_files_from_src_to_dst(source_dir, destination_dir)

    generate_pages_recursive("./content", "./template.html", "./public")


if __name__ == "__main__":
    main()