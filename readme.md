Projet 6 Openclassrooms
Automatisation de configurations des switchs Cisco avec Netmiko et Python3
Ici nous allons configurer les VLANS, les ports ACCESS, les ports en mode TRUNK
et tester si les PCS (en DHCP) arrivent à communiquer entre eux.
Prérequis pour la réalisation de ce projet :
  - 1 serveur Debian 10 srvnmaster : 
      Installation de DHCP : apt install isc-dhcp-server
     Configuration de VLANS 
        nano /etc/default/isc-dhcp-server
          INTERFACESv4="enp0s3.10 enp0s3.20 enp0s3.30" 
          ensuite configurer le réseau dans /etc/network/Interfaces suivant les pools d'adresses (voir image)
          
  - 1 Poste Administration sous Debian 10 avec une adresse dans le même réseau des 4 switchs
            Installation de Python et Netmiko :
            apt-get install python3-pip
            pip3 install netmiko
   - Configuration initiale des switchs :
        1. Vérification de la version de l'équipement Cisco pour le protocole SSH
          Avant toute chose, il faut vérifier que la version de votre switch ou routeur Cisco est bien compatible avec le protocole SSH. 
          Pour cela, passez en mode configuration etentrez en ligne de commande “show version”. Il faut retrouver dans la version de l’équipement le mot “K9”.
          Si c’est le cas, vous pouvez passer à l’étape suivante.
        2. Création des noms d'hôte et de domaine, et d'un mot de passe pour le mode privilégié   
        3. Génération de la paire de clés asymétriques RSA (ici choixir 1024)
        4. Activation du protocole SSH
        5. mettre le timer en Disable : line vty 0 3 , exec-timeout 0
        6; Connexion sur chaque  switch en ssh depuis le PC Administration pour la reconnaissance des clefs
* Le script Networkcisco.py pour la configuration des switchs 2,3,4 avec le fichier vconfigs (autant de lignes que de switchs à configurer)
* Le script esw1network.py pour la configuration du switch fédérateur avec le fichier sw1conf.txt
Mettre en route les switchs
  les scripts sont sur la machine Administration on lance d'abord administration~# python3 Networkcisco.py
                                ensuite administration~# python3 Networkcisco.py                                
contrôler si vos PCS ont bien une adresse ip provenant de svnmaster. 

![pr6](https://user-images.githubusercontent.com/68608846/92990372-55577980-f4dc-11ea-87ab-66878d8bcc78.JPG)
