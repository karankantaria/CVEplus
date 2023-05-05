import os
import json
import requests
from subprocess import Popen, PIPE
import xmltodict

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

# made by Karan Kantaria lil watermark innit


def get_searchsploit_results_detailed(service):
    cmd_test = 'searchsploit'  # opening searchsploit
    check = service
    cmd = cmd_test+" --json "+check  # gets searchsploit results as json
    stdout = Popen(cmd, shell=True, stdout=PIPE).stdout
    clear = 'clear'
    output = stdout.read()  # saves results to output
    output = json.loads(output)
    path = []
    result_tittle = []
    CVE_path = []
    CVE_results = []
    CVE_title = []
    # iterates through results in json
    for x in range(len(output['RESULTS_EXPLOIT'])):
        # saves results to lists
        result_tittle.append(output['RESULTS_EXPLOIT'][x]['Title'])
        # saves paths of results to list
        path.append(output['RESULTS_EXPLOIT'][x]['Path'])
    for i in range(len(result_tittle)):
        print(result_tittle[i])
    for i in range(len(output['RESULTS_EXPLOIT'][i]['Codes'])):
        current = str(output['RESULTS_EXPLOIT'][i]['Codes'])
        # Some results have multiple codes so this splits them
        current_list = current.split(';')
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


def nmap_scan(ip):
    ip = str(ip)
    cmd = "nmap -p 1-65535 -T4 -A -v -sV -oX nmap_output.xml " +ip+" 1>/dev/null 2>/dev/null"
    # stdout = Popen(cmd, shell=True, stdout=PIPE).stdout
    os.system(cmd)
    temp_open = open(str("nmap_output.xml"))
    xml_content = temp_open.read()
    temp_open.close()
    nmap_JSON = json.dumps(xmltodict.parse(
        xml_content), indent=4, sort_keys=True)
    nmap_JSON = json.loads(nmap_JSON)
    http_status = False
    cmd_run = nmap_JSON['nmaprun']['@args']
    ports = nmap_JSON['nmaprun']['host']['ports']['port']
    open_ports = []
    services = []
    product = []
    Found_CVE = []
    for i in range(len(ports)):
        open_ports.append(ports[i]['@portid'])
        services.append(ports[i]['service']['@name'])
        # product.append(ports[i]['service']['@product'])
    for i in range(len(open_ports)):
        print("Port: ", open_ports[i], " Service: ", services[i])
    find_CVE = input("Would you like to search for CVE's? [y/n]")
    if find_CVE.lower() == "y":
        os.system("clear")
        for i in range(len(services)):
            if get_searchsploit_results(services[i]):
                Found_CVE.append(services[i])
            else:
                print("No CVE's found for ", services[i])
        if len(Found_CVE) > 0:
            os.system("clear")
            for i in range(len(Found_CVE)):
                print("\033[91mFound\033[00m CVE's for: ", Found_CVE[i])
            loop = True
            while loop == True:
                exploit_menu = input("Would you like to \033[91mexploit\033[00m? [y/n]?")
                if exploit_menu.lower() == "y":
                    for i in range(len(services)):
                        if services[i] == "http":
                            http_status = True
                    exploit(Found_CVE, http_status, ip)
                    loop = False
                elif exploit_menu.lower() == "n":
                    print("BYE")
                    loop = False
                    exit()
                else:
                    print("Invalid Choice")


def get_searchsploit_results(service):
    cmd_test = 'searchsploit'  # opening searchsploit
    check = service
    cmd = cmd_test+" --json "+check  # gets searchsploit results as json
    stdout = Popen(cmd, shell=True, stdout=PIPE).stdout
    clear = 'clear'
    output = stdout.read()  # saves results to output
    output = json.loads(output)
    for x in range(len(output['RESULTS_EXPLOIT'])):
        for i in range(len(output['RESULTS_EXPLOIT'][x]['Codes'])):
            current = str(output['RESULTS_EXPLOIT'][i]['Codes'])
            # Some results have multiple codes so this splits them
            current_list = current.split(';')
            for x in range(len(current_list)):
                if "CVE" in current_list[x]:
                    yes = True
                    return yes
                else:
                    yes = False
                    return yes


def dirbuster(ip):
    os.system("clear")
    path_to_wordlist = input("Enter path to wordlist: ")
    cmd = "gobuster dir -u https://"+ip+" --wordlist "+path_to_wordlist+" -t 100 -o gobuster_output.txt"
    os.system(cmd)


def exploit(Found_CVE, http_status, ip):
    os.system("clear")
    CVE_list = Found_CVE
    http_Status=http_status
    print(http_Status)
    count = 0
    if http_Status == True:
        for i in range(len(CVE_list)):
            print("["+str(count)+"] "+CVE_list[i])
            count += 1
        choice = input(
            "Enter which service you would like to exploit or enter d to run dirbuster on the http site: ")
        if choice.lower() == "d":
            dirbuster(ip)
        else:
            os.system("clear")
            get_searchsploit_results_detailed(CVE_list[int(choice)])


# main
banner()
get_ip=input("Enter \033[91mIP\033[00m: ")
nmap_scan(get_ip)
