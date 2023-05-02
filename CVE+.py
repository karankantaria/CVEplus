import git
import os
import re
import json
import requests
from subprocess import Popen, PIPE

# Made by Karan Kantaria
# Too lazy to comment everything sooooo
#  https://github.com/karankantaria/

def get_CVE_detailes(CVE_Year, CVE_Id, Path_CVE):
    os.system("clear")
    CVE_year = str(CVE_Year)
    CVE_Id = str(CVE_Id)
    CVE_Id_int = int(CVE_Id)
    ID_Status = ""
    if len(CVE_Id) < 4:
        for i in range(4-len(CVE_Id)):
            CVE_Id = "0"+CVE_Id
    ID_Status = ""
    if len(CVE_Id) >= 5:
        ID_Status = CVE_Id[0]+CVE_Id[1]+"xxx"
    elif len(CVE_Id) >= 4:
        ID_Status = CVE_Id[0]+"xxx"
    else:
        ID_Status = "0xxx"

    url = 'https://raw.githubusercontent.com/CVEProject/cvelist/master/' + \
        CVE_year+'/'+ID_Status+'/CVE-'+CVE_year+'-'+CVE_Id+'.json'
    json_data = requests.get(url).json()
    CVE_offic_id = json_data['CVE_data_meta']['ID']
    Assigner = json_data['CVE_data_meta']['ASSIGNER']
    State = json_data['CVE_data_meta']['STATE']
    x = 0
    Version_info_get = json_data['affects']['vendor']['vendor_data'][0]['product'][
        'product_data'][0]['version']['version_data'][0]['version_value']
    Version_info = []
    for x in range(len(json_data['affects']['vendor']['vendor_data'][0]['product']['product_data'][0]['version']['version_data'])):
        Version_info.append(json_data['affects']['vendor']['vendor_data'][0]['product']
                            ['product_data'][0]['version']['version_data'][x]['version_value'])

    Description = json_data['problemtype']['problemtype_data'][0]['description'][0]['value']
    Description_detailed = json_data['description']['description_data'][0]['value']

    references_name = []
    references_url = []
    for l in range(len(json_data['references']['reference_data'])):
        references_name.append(
            json_data['references']['reference_data'][l]['name'])
        references_url.append(
            json_data['references']['reference_data'][l]['url'])
    print("\033[91mASSIGNER\033[00m: ", Assigner)
    print("\033[91mSTATE\033[00m: ", State)
    print("\033[91mOFFICIAL CVE\033[00m:", CVE_offic_id)
    print("\033[91mAffected versions\033[00m: ")
    for i in range(len(Version_info)):
        print(Version_info[i])
    print("\033[91mDescription\033[00m: ", Description)
    print(Description_detailed)
    print("\033[91mREFERENCES\033[00m: ")
    for i in range(len(references_name)):
        print("\033[91mName\033[00m: ", references_name[i])
        print("\033[91mURL\033[00m: ", references_url[i])
    loop = True
    while loop == True:
        choice = input(
            "Would you like to \033[91mmirror\033[00m to current dir? [y/n]")
        if choice.lower() == "y":
            loop = False
            mirror(Path_CVE)
        elif choice.lower() == "n":
            loop = False
            os.system("clear")
            print("BYE")
            exit()
        else:
            print("Invalid selection")

#made by Karan Kantaria lil watermark innit
def get_searchsploit_results():
    cmd_test = 'searchsploit' # opening searchsploit
    check = input("Enter what \033[91mservice\033[00m you wish to check: ")
    cmd = cmd_test+" --json "+check # gets searchsploit results as json
    stdout = Popen(cmd, shell=True, stdout=PIPE).stdout
    clear = 'clear'
    output = stdout.read() # saves results to output
    output = json.loads(output)
    path = []
    result_tittle = []
    CVE_path = []
    CVE_results = []
    CVE_title = []
    for x in range(len(output['RESULTS_EXPLOIT'])): # iterates through results in json
        result_tittle.append(output['RESULTS_EXPLOIT'][x]['Title']) # saves results to lists
        path.append(output['RESULTS_EXPLOIT'][x]['Path']) # saves paths of results to list
    for i in range(len(result_tittle)):
        print(result_tittle[i])    
    for i in range(len(output['RESULTS_EXPLOIT'][i]['Codes'])):
        current = str(output['RESULTS_EXPLOIT'][i]['Codes'])
        current_list = current.split(';') # Some results have multiple codes so this splits them
        for x in range(len(current_list)):
            if "CVE" in current_list[x]:
                CVE_results.append(current_list[x]) 
                CVE_title.append(result_tittle[x])
                CVE_path.append(path[x])
    os.system(clear)
    pr("CVE DETECTED")
    for i in range(len(CVE_results)):
        print('[', i+1, ']', 'Info: ', CVE_title[i], 'CVE: ', CVE_results[i])
    choice = input(
        "Enter \033[91mchoice\033[00m or \033[91mm+choice\033[00m  to mirror: ")
    if "m" in choice:
        choice = choice[0]
        choice = int(choice)
        mirror(CVE_path[choice-1])
    else:
        choice = int(choice[0])
        split_CVE = []
        split_CVE = CVE_results[choice-1].split("-")
        get_CVE_detailes(split_CVE[1], split_CVE[2], CVE_path[choice-1])
    print("bye")
    exit()


def mirror(CVE_path):
    os.system("clear")
    CVE_path = str(CVE_path)
    cmd = 'searchsploit -m '+CVE_path
    os.system(cmd)


def pr(skk): print("\033[91m {}\033[00m" .format(skk))


def banner():
    banner = """
    _____________   _______________            
    \_   ___ \   \ /   /\_   _____/    \033[91m.__\033[00m      
    /    \  \/\   Y   /  |    __)_   \033[91m__\033[91m|  |___\033[00m 
    \     \____\     /   |        \ \033[91m/__    __/\033[00m  
     \______  / \___/   /_______  /    \033[91m|__|\033[00m         
            \/                  \/  
            by \033[91mKaran Kantaria\033[00m           
        """
    print(banner)


#main
banner()
get_searchsploit_results()
