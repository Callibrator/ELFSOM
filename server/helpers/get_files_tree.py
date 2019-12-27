import os


def get_files_tree(main_dir):
    listOfFile = os.listdir(main_dir)
    allFiles = []

    # Iterate over all the entries
    for entry in listOfFile:
        fullPath = os.path.join(main_dir, entry)

        if os.path.isdir(fullPath):
            allFiles = allFiles + get_files_tree(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

if __name__ == "__main__":
    print(get_files_tree("./../"))