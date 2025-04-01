import os
import shutil
import tarfile

# 1. Create a copy of a file
def copy_file(source_path, destination_path):
    shutil.copy(source_path, destination_path)
    print(f"Copied file from {source_path} to {destination_path}")

# 2. Extract a tar file
def extract_tar(file_path, extract_to):
    with tarfile.open(file_path, 'r') as tar:
        tar.extractall(path=extract_to)
        print(f"Extracted tar file {file_path} to {extract_to}")

# 3. Find the patter
def find_files_with_pattern(directory, pattern):
    files = os.listdir(directory)
    for file in files:
        if pattern in file and file.endswith('.xml'):
            print(f"Found file: {file}")
            return file
    return None

# 4. Extract ID
def extract_id(filename):
    parts = filename.split("_")
    if len(parts) > 1:
        id_with_extension = parts[1]
        return id_with_extension.split(".")[0]
    return None

# 5. Make Copies
def make_copies(original_file, directory, num_copies=10):
    for i in range(num_copies):
        new_filename = f"page_{i}.xml"
        new_filepath = f"{directory}/{new_filename}"

        shutil.copyfile(original_file, new_filepath)
        print(f"Created copy: {new_filename}")

# 6. Change all instances of that id to that number (page_*.xml)
def replace_id_in_files(directory, original_id, num_files=10):
    for i in range(num_files):
        filename = f"page_{i}.xml"
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                content = file.read()

            updated_content = content.replace(original_id, str(i))

            with open(filepath, 'w') as file:
                file.write(updated_content)

            print(f"Updated file: {filename} (Replaced ID with {i})")
        else:
            print(f"File not found: {filename}")

# 7. Change all instances of that id to that number (page_*.xml)
def update_content_xml(ID, filepath, num_pages):
    with open(filepath, 'r') as file:
        content = file.read()

    content = content.replace(f'<Property name="activeId">{ID}</Property>',
                              '<Property name="activeId">0</Property>')

    pages_section = ""
    for i in range(num_pages):
        pages_section += f'<Page href="page_{i}.xml"/>'

    content = content.replace(f'<Pages><Page href="page_{ID}.xml"/></Pages>',
                              f'<Pages>{pages_section}</Pages>')

    with open(filepath, 'w') as file:
        file.write(content)

    print(f"Updated content.xml: Active ID set to 0 and added {num_pages} pages.")


# 8. Change all instances of that id to that number (*.png)
def process_thumbnails(directory, original_id, num_copies=10):
    original_file = os.path.join(directory, f"{original_id}.png")

    if not os.path.exists(original_file):
        print(f"Original file not found: {original_file}")
        return

    for i in range(num_copies):
        new_filename = f"{i}.png"
        new_filepath = os.path.join(directory, new_filename)

        shutil.copyfile(original_file, new_filepath)
        print(f"Created copy: {new_filename}")


# 9. Change all instances of that label to that number (page stencils)
def replace_label_in_pages(directory, num_pages=10):
    for i in range(num_pages):
        filename = f"page_{i}.xml"
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                content = file.read()

            updated_content = content.replace("CDATA[Label]", f"CDATA[{i}]")

            with open(filepath, 'w') as file:
                file.write(updated_content)

            print(f"Updated file: {filename} (Replaced 'Label' with {i})")
        else:
            print(f"File not found: {filename}")

def main():
    originalFile = "test.epgz"
    directory = "./test/"
    copy_file(originalFile, directory)
    extract_tar(originalFile, directory)
    fileFound = find_files_with_pattern(directory, "page")
    if fileFound:
        print(f"Processing file: {fileFound}")
    else:
        print("No matching files found.")
    ID = extract_id(fileFound)
    make_copies(f"{directory}page_{ID}.xml", directory)
    os.remove(f"{directory}page_{ID}.xml")
    replace_id_in_files(directory, ID, num_files=10)
    update_content_xml(ID, f"{directory}content.xml", 10)
    process_thumbnails(f"{directory}/thumbnails/", ID)
    os.remove(f"{directory}/thumbnails/{ID}.png")
    replace_label_in_pages(directory, num_pages=10)

if __name__ == "__main__":
    main()
