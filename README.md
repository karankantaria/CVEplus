# CVEplus
CVE+ is a pyhton script that automates part of the exploiting process.
<br>
Firstly,it starts an NMAP scan on whatever ip the user wishes. From here it makes a search for whatever service the nmap scan finds. It searches using searchsploits exploit database and returns results as JSON. 
From here it checks the results to find if any have CVE's associated with them.
You can mirror the wanted CVE from here or you can continue to find out more information from them.
If you chose to learn more it checks https://github.com/CVEProject/cvelist
<br>
from here it finds additional information from the repo about the chosen CVE. This includes references, assigners, state etc.
Then you can either mirror the CVE to current dir or make another search.
Furthermore, if there is a HTTP server running the script automatically prompts the use of dirbuster.

## Examples
#### yuh
![examples1](https://raw.githubusercontent.com/karankantaria/CVEplus/main/img/Capture.PNG)

![examples2](https://raw.githubusercontent.com/karankantaria/CVEplus/main/img/Capture_2.PNG)

![examples2](https://raw.githubusercontent.com/karankantaria/CVEplus/main/img/Capture_3.PNG)

![examples2](https://github.com/karankantaria/CVEplus/blob/main/img/Capture4.PNG)

![examples2](https://raw.githubusercontent.com/karankantaria/CVEplus/main/img/Capture2.PNG)

![examples2](https://raw.githubusercontent.com/karankantaria/CVEplus/main/img/Capture3.PNG)

![examples2](https://github.com/karankantaria/CVEplus/blob/main/img/Capture5.PNG)
