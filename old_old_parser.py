from pydoc import doc
from zipfile import ZipFile
import os
import re

#Function to unzip all the zips in the given directory
def recursive_unzip_worker(directory):
    #Searches the whole directory
    for root, dir, files in os.walk(directory):
        #For each file in root
        for name in files:
            #If the file ends in .zip
            if re.search(r'\.zip$', name):
                #Path to extract to (root)
                to_path = os.path.join(root, name.split('.zip')[0])
                #Zip to extract
                zip_file = os.path.join(root, name)

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

def recursive_unzip(directory):
    #Setting up directory
    if(os.path.exists(directory)):
        print("Logs folder exists.")
    else:
        print("Logs folder didn't exist, creating now...")
        os.mkdir("Logs")
    
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
    else:
        print("All conditions must be Y")
        print("Cancelling operation.")

recursive_unzip("Logs")