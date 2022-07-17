import shutil
import tarfile
from zipfile import ZipFile
from tarfile import TarFile
import os
import re

#Function to unzip all the zips in the given directory
def recursive_unzip_worker(directory):
    #Searches the whole directory
    for root, dir, files in os.walk(directory):
        #For each file in root
        for file in files:
            #If the file ends in .zip
            if re.search(r'\.zip$', file):
                #Path to extract to (root)
                to_path = os.path.join(root, file.split('.zip')[0])
                #Zip to extract
                zip_file = os.path.join(root, file)

                #If the path doesn't exist, create the path
                if not os.path.exists(to_path):
                    os.makedirs(to_path)
                    #Extraction
                    with ZipFile(zip_file, 'r') as zfile:
                        zfile.extractall(path=to_path)
                    #Deletes zip file (necessary to stop recursion)
                    os.remove(zip_file)
                
                #Returns true to make sure recursion continues
                return True

    #Returns false to end recursion, once no more zips are found
    return False

#Function to initialize the unzipping
def recursive_unzip(directory):
    #Setting up directory
    if(os.path.exists(directory)):
        print("ZippedLogs folder exists.")
    else:
        print("ZippedLogs folder didn't exist, creating now...")
        os.mkdir("ZippedLogs")
    
    #Checks if files are ready
    #
    #
    #might need to rework
    input1 = input("Are the zip files placed in the Logs folder? (There may be multiple) Y/N: ")
    input2 = input("The zip files will be deleted after completion, is there a backup? Y/N: ")
    input3 = input("Final check. Y/N: ")

    if(input1 == 'Y' and input2 == 'Y' and input3 == 'Y'):
        #Runs unzip_directory until exists_zip is false
        run = True
        while run:
            run = recursive_unzip_worker(directory) #run will equal false once no more zips are found.
        print("Completed")
        return True #To know if operation was completed
    else:
        print("All conditions must be Y")
        print("Cancelling operation.")
        return False #To know if operation failed

#Function to grab all tar files after the unzip has taken place
def grab_tar_files(source_directory, result_directory):
    if not os.path.exists(result_directory):
        os.mkdir(result_directory)
    
    for root, dir, files in os.walk(source_directory):
        for file in files:
            try:
                if re.search(r'\.tgz$', file):
                    file_path = os.path.join(root, file)
                    shutil.move(file_path, result_directory)
            except:
                print("Error with shutil.move")

def grab_log_files(directory):
    for file in os.listdir(directory):
        tar_path = os.path.join(directory, file)

        tar_file = tarfile.open(tar_path)
        tar_file_files = tar_file.getnames()

        for item in tar_file_files:
            if ("app-aid-wwu") in item:
                tar_file.extract(item, path=directory)

        tar_file.close()
        #Deletes zip file (necessary to stop recursion)
        os.remove(tar_path)

#Executions
source_dir ='ZippedLogs'
result_dir = 'Logs'
if recursive_unzip(source_dir):
    print("Grabbing tar files..")
    grab_tar_files(source_dir, result_dir)
    print("Grabbing log files..")
    grab_log_files(result_dir)
    print("Creating excel sheet..")
    exec(open("updated_folder_parser.py").read())