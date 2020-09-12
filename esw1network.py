
#!/usr/bin/python3
#-*- coding Utf-8 -*-
############### fichier configswitch.txt#############################################
##### 0 adresse ip du switch : ip = (line.split()[0])
##### 1 nom   du switch : id = (line.split()[1])
##### 2 nom   utilisateur :usr= (line.split()[2])
##### 3 passwd pwd= (line.split()[3])
##### 4 passwd secret : sct= (line.split()[4])
##### 5 debut de la boucle pour les VLANS à créer : r1=  (line.split()[5])
##### 6 fin de la boucle des vlans à créer : r2=  (line.split()[6])
##### 7 nombre de ports access si =0 alors pas de création d'access vlans : + \
## ici nous allons retrouver x lignes x est nle nombre de ports + \
## à configurer voir ##### 7 dans notre exemple : 0lignes
##### 8 (suivant le nombre de ports access à configurer à partir + \
## de la pos 7 : 7+0+1 donc ligne nb=3 ) + \
##### nombre de ports mode trunk si =0 alors pas de création :+ \ 
#####  il y aura autant de lignes qu'il y a de ports trunk à configuer ici 9 à 12
##### 9 config port mode trunk séparateur "-" si range alors sous la forme + \
##### fa1/1-3-v2(ex: int range fa1/1-3 ...)
#####ci dessous exemple de ligne du fichier :

## 192.168.99.4 ESW1 user cisco cisco 1 4 0 4 fa1/0-v10/v30 fa1/1-v10/30 fa1/2-v10/30 fa1/3-v10/30
################################# ####################################################




"""
Utilisation des modules  process et  Netmikopour se connecter
sur chaque switch et  éxecuter les commandes pour  la:
- création des vlans
- des ports access
- des ports trunk
- Utilisation d'un fichier vconfigs.txt  pour connaitre la configuration à effe$
On récupère la date et le temps pour la réalisation des proccess.
"""
# récupération des librairies

from __future__ import print_function, unicode_literals
from multiprocessing import Process

from datetime import datetime
from netmiko import ConnectHandler
import logging

# création d'un fichier log netmiko
logging.basicConfig(filename='fcesw1.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

#initialisation de la variable configuration des switch
switches=[]

# initialisation du tableau des ports access
confacc=[]

# initialisation du tableau des ports  trunk
confprt=[]

### fonction qui sera appelée dans le process pour executer les commandes

def exec_confcmd(a_device,r1,r2,nbpacc,nbportr,postr):
    """On Execute la fonction en utilisant les commandes du module  Netmiko."""
    remote_conn = ConnectHandler(**a_device)
    capture = remote_conn.enable(cmd='enable 15')
   if int(r1)*int(r2)>0:
        print ("\nConfiguration des  VLANS")
        for n in range (int(r1),int(r2)):
            print ("#" * 80)
            conf_com = ['vlan ' + str(n*10), 'name SwVlan' + str(n*10)]
            print ("#" * 80)
            print(remote_conn.send_config_set(conf_com))
    # creation des ports access vlans
    if int(nbpacc)>0:
        print ("\nConfiguration des  ports ACESS")
        j=0
        while (j<int(nbpacc)):
            asplit=(line.split()[8+j])
            confacc=['interface ' + asplit[0:asplit.find("-")], + \
            'switchport access vlan ' + asplit[asplit.find("-")+2:len(asplit)]]
            j=j + 1
            print ("#" * 80)
            print(remote_conn.send_config_set(confacc))
        confacc=[]
    # creation des ports  trunk
    if int(nbportr)>0:
        print ("\nConfiguration des  ports trunk")
        k=0
        chtr=""
        while(k<int(nbportr)):
            """
             Séparation du texte du fichier vconfigs.txt : 
                    fa1/0-v10/30 (vlan de 10 a 30)
            """
            asplit=(line.split()[postr+k])
            chtr=(asplit[asplit.find("-")+1:len(asplit)])
            chtr=chtr.replace("v", "")
            chtr=chtr.replace("/", "-")]
            confprt=['interface ' + asplit[0:asplit.find("-")], + \ 
            'switchport trunk encapsulation dot1q', + \
            'switchport mode trunk', + \
            'switchport trunk allowed vlan 1-2,'+chtr+',1002-1005']
            print(remote_conn.send_config_set(confprt))
            confprt=[]
            k=k+1
    print('#' * 80)
    print()
    remote_conn.disconnect()

with open("sw1conf.txt") as fh:
        fh2=fh.readlines()
for line in fh2:
    if (line == ""):
        break
    else:
        ip = (line.split()[0])
        id = (line.split()[1])
        usr= (line.split()[2])
        pwd= (line.split()[3])
        sct= (line.split()[4])
        r1=  (line.split()[5])
        r2=  (line.split()[6])
        nbpacc= (line.split()[7])
        nb=int(nbpacc)+1
        nbportr= (line.split()[7+nb])
 # numero de position du premier port trunk a configurer :
        postr=7+nb+1

 # On definit le dictionnaire cisco necessaire netmiko
    SWS= {
    'device_type': 'cisco_ios',
    'ip': ip,
    'username': usr,
    'password': pwd,
    'secret': sct,
    'blocking_timeout': 120
   }

    switches.append(SWS)
print("ici les switchs" )
print(switches)
print ("#" * 80)

def main():
    start_time = datetime.now()
    xnb=0
    procs = []
    for a_device in switches:
        print("début des process " + str(xnb))
        my_proc = Process(target=exec_confcmd,args=(a_device,r1,r2,nbpacc,nbpo$
        my_proc.start()
        procs.append(my_proc)
        print(procs)
        xnb=xnb+1
   for a_proc in procs:
        print(a_proc)
        a_proc.join()

    print("\nElapsed time: " + str(datetime.now() - start_time))


if __name__ == "__main__":
    main()










