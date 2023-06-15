import os
import sys
import subprocess
import json
import concurrent.futures
from termcolor import cprint

# configuration
STIGMA_PATH = "./Stigma.py"
APK_PATH = "./apks"
MODIFIED_APK_PATH = "./modified"
DEBUG = True

# uses nodejs to get app id from query
def get_app_id(query):
    try:
        result = subprocess.check_output(["node", "./app_id_script.js", query], text=True)
        result = json.loads(result)
        return result[0]["appId"] if result else None
    except Exception as e:
        cprint(f"Error getting app id for {query}", "red", attrs=["bold"])
        return None

# uses apkeep to download apk
def download_files(apps):
    for app in apps:
        app_id = get_app_id(app)
        if app_id:
            cprint(f"Found app: {app}", "green", attrs=["bold"])
            cprint("Downloading with apkeep...", "cyan", attrs=["bold"])
            subprocess.run(["apkeep", "-a", app_id, APK_PATH], check=True)

            try: 
                # make sure to supress ls output
                file_list = subprocess.check_output(["ls", f"{APK_PATH}/{app_id}.xapk"], text=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                cprint(f"XAPK detected for {app}!", "yellow", attrs=["bold"])
                cprint("Extracting...", "cyan", attrs=["bold"])
                subprocess.run(["unzip", f"{APK_PATH}/{app_id}.xapk", "-d", f"{APK_PATH}/{app_id}"], check=True)
                subprocess.run(["mv", "-v", f"{APK_PATH}/{app_id}/{app_id}.apk", f"{APK_PATH}/{app_id}.apk"], check=True)
                subprocess.run(["rm", "-rf", f"{APK_PATH}/{app_id}", f"{APK_PATH}/{app_id}.xapk"], check=True)
            except:
                pass

            cprint(f"Done with {app}!", "green", attrs=["bold"])
        else:
            cprint(f"No app found for {app}", "red", attrs=["bold"])

# get list of files in apk directory
def get_files():
    file_list = subprocess.check_output(["ls", f"{APK_PATH}"], text=True)
    files = file_list.split("\n")
    return files

# process file with Stigma
def process_file(file):
    cprint(f"Processing {file.strip()}...", "cyan", attrs=["bold"])
    if DEBUG:
        subprocess.run(["python3", f"{STIGMA_PATH}", f"{APK_PATH}/{file.strip()}", ">>", f"{file.strip()}.log"], check=True)
    else:
        subprocess.run(["python3", f"{STIGMA_PATH}", f"{APK_PATH}/{file.strip()}"], check=True)
    subprocess.run(["mv", f"Modified_{file.strip()}", f"{MODIFIED_APK_PATH}"])


def main():
    # colored input instead
    cprint("Enter the names of the apps you want to download, separated by comma.", "green", attrs=["bold"], end=" ")
    apps = input().split(",")
    apps = [app.strip() for app in apps]

    if not os.path.exists(f"{APK_PATH}"):
        subprocess.run(["mkdir", f"{APK_PATH}"])

    if not.os.path.exists(f"{MODIFIED_APK_PATH}")
        subprocess.run(["mkdir", f"MODIFIED_APK_PATH"])

    download_files(apps)

    files = get_files()

    # create a ProcessPoolExecutor (for parallel processing)
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        executor.map(process_file, files)

if __name__ == "__main__":
    main()

