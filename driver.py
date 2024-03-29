import shutil
import tarfile
from zipfile import ZipFile
from tarfile import TarFile
import os
import re

# Global variables
SOURCE_DIR = 'ZippedLogs'
RESULT_DIR = 'Logs'
AID_RESULT_DIR = 'AIDLogs'
AWLU_RESULT_DIR = 'AWLULogs'


# Function to unzip all the zips in the given directory
def recursive_unzip_worker(directory):
    # Searches the whole directory
    for root, dir, files in os.walk(directory):
        # For each file in root
        for file in files:
            # If the file ends in .zip
            if re.search(r'\.zip$', file):
                # Path to extract to (root)
                to_path = os.path.join(root, file.split('.zip')[0])
                # Zip to extract
                zip_file = os.path.join(root, file)

                # If the path doesn't exist, create the path
                if not os.path.exists(to_path):
                    os.makedirs(to_path)
                    # Extraction
                    with ZipFile(zip_file, 'r') as zfile:
                        zfile.extractall(path=to_path)
                    # Deletes zip file (necessary to stop recursion)
                    os.remove(zip_file)

                # Returns true to make sure recursion continues
                return True

    # Returns false to end recursion, once no more zips are found
    return False


# Function to initialize the unzipping
def recursive_unzip(directory):
    # Setting up directory
    if (os.path.exists(directory)):
        print("ZippedLogs folder exists.")
    else:
        print("ZippedLogs folder didn't exist, creating now...")
        os.mkdir("ZippedLogs")

    # 4 checks done so user knows how the script runs
    input1 = input("Are the zip files placed in the ZippedLogs folder? (There may be multiple) Y/N: ")
    if (input1 != 'Y'):
        print("Cancelling operation")
        return False

    input2 = input("The zip files will be deleted after completion, is there a backup? Y/N: ")
    if (input2 != 'Y'):
        print("Cancelling operation")
        return False

    input3 = input("Final check. Y/N: ")
    if (input3 != 'Y'):
        print("Cancelling operation")
        return False

    else:
        # Runs unzip_directory until exists_zip is false
        print("Unzipping files..")
        run = True
        while run:
            run = recursive_unzip_worker(directory)  # run will equal false once no more zips are found.
        return True  # To know if operation was completed


# Function to grab all tar files after the inital unzip has taken place
def grab_tar_files(source_directory, result_directory):
    # Create directory if it doesn't exist
    if not os.path.exists(result_directory):
        os.mkdir(result_directory)

    # Loop to search through the directory for any tar files
    for root, dir, files in os.walk(source_directory):
        for file in files:
            # Try/except in case there are any issues with moving
            # (Ran into an issue with one of the zip files, still trying to find out why)
            try:
                # If it ends in .tgz, move it to the result directory
                if re.search(r'\.tgz$', file):
                    file_path = os.path.join(root, file)
                    shutil.move(file_path, result_directory)

                # In case there are some logs that aren't inside a TGZ file
                # elif re.search(r'\.log', file):
                #    file_path = os.path.join(root, file)
                #    shutil.move(file_path, result_directory)

            except:
                print("Error with shutil.move")


# Function to grab log files from each tar file that was found
def grab_log_files(directory):
    # Loop for each tar file in the log folder
    for file in os.listdir(directory):
        if file.endswith(".tgz"):
            tar_path = os.path.join(directory, file)  # path of tar file
            tar_file = tarfile.open(tar_path, 'r')  # tar file object
            tar_file_files = tar_file.getnames()  # items in tar file

            # Checks for any aid log files in the tar file
            for item in tar_file_files:
                if (('app-aid-wwu') in item) or (('app-wwu') in item):
                    # Extracts them when found
                    tar_file.extract(item, path=directory)
                    break  # end the search here, only one aid-wwu is inside so no need to keep searching

            # Closes and deletes tar file (necessary to stop recursion)
            tar_file.close()
            os.remove(tar_path)


# Function to separate AID and AWLU log files
def sort_log_files(source, aid, awlu):
    # Create directory if it doesn't exist
    if not os.path.exists(aid):
        os.mkdir(aid)
    if not os.path.exists(awlu):
        os.mkdir(awlu)

    for file in os.listdir(source):
        path = os.path.join(source, file)
        if ('aid-wwu') in file:
            shutil.move(path, aid)
        elif ('app-wwu') in file:
            shutil.move(path, awlu)


# Driver function which executes all relevant functions
def driver(source, result, aid, awlu):
    # If the recursive unzip fails, cancel the operation
    if not recursive_unzip(source):
        print("Error with unzipping, cancelling operation")
        return False

    # Only runs if recursive unzip is successful
    print("Grabbing tar files..")
    grab_tar_files(source, result)
    print("Opening tar files..")
    grab_log_files(result)
    print("Separating log files..")
    sort_log_files(result, aid, awlu)
    print("Creating excel sheet..")

    # Deletes the zipped logs directory as it's not needed anymore.
    shutil.rmtree(result)
    shutil.rmtree(source)


# Execution of code
driver(SOURCE_DIR, RESULT_DIR, AID_RESULT_DIR, AWLU_RESULT_DIR)
exec(open("log_parser.py").read())

