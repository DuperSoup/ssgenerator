from other_functions import *
import sys

def main():
    # 1. Read basepath from CLI args, default to "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    source_dir = "./static"
    destination_dir = "./docs"

    copy_files_from_src_to_dst(source_dir, destination_dir)

    generate_pages_recursive("./content", "./template.html", "./docs", basepath)


if __name__ == "__main__":
    main()