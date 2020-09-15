Projet 6 Openclassrooms
Automatisation de configurations des switchs Cisco avec Netmiko et Python3
Ici nous allons configurer les VLANS, les ports ACCESS, les ports en mode TRUNK

Prérequis pour la réalisation de ce projet :
         
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
Mettre en route les switchs.
Sur  la machine ADMINISTRATION  vous trouvez les différents scripts et fichiers texte pour les configurations.

      * Le script Networkcisco.py pour la configuration des switchs 2,3,4 avec le fichier vconfigs (autant de lignes que de switchs à configurer)
      Le script élabore avec succès la connexion SSH aux équipements désignés dans le fichier texte : vconfigs
 ############### fichier configswitch.txt############################################# 
 Ici une configuration pour 3 switches :

                  192.168.99.1 ESW2 user cisco cisco 1 4 3 fa1/1-v10 fa1/2-v20 fa1/3-v30 1 fa1/0-v10/30 
                  192.168.99.2 ESW3 user cisco cisco 1 4 3 fa1/1-v10 fa1/2-v20 fa1/3-v30 1 fa1/0-v10/30 
                  192.168.99.3 ESW4 user cisco cisco 1 4 3 fa1/1-v10 fa1/2-v20 fa1/3-v30 1 fa1/0-v10/30 
      
       ##### 0 adresse ip du switch : ip = (line.split()[0]) 
       ##### 1 nom   du switch : id = (line.split()[1]) 
       ##### 2 nom   utilisateur :usr= (line.split()[2]) 
       ##### 3 passwd pwd= (line.split()[3]) 
       ##### 4 passwd secret : sct= (line.split()[4]) 
       ##### 5 debut de la boucle pour les VLANS à créer : r1=  (line.split()[5]) 
       ##### 6 fin de la boucle des vlans à créer : r2=  (line.split()[6]) 
       ##### 7 nombre de ports access si =0 alors pas de création d'access vlans : + \ 
       ## ici nous allons retrouver x lignes x est nle nombre de ports + \ 
       ## à configurer voir ##### 7 dans notre exemple : 3 lignes (nbpacc)
       ##### 8 config port access séparateur "-" si range alors sous la forme + \ 
       ## fa1/1-3-v2(ex: int range fa1/1-3 ...) 
       ##### 9 config port access séparateur "-" si range alors sous la forme + \ 
       ## fa1/1-3-v2(ex: int range fa1/1-3 ...) 
       ##### 10 config port access séparateur "-" si range alors sous la forme + \ 
       ## fa1/1-3-v2(ex: int range fa1/1-3 ...) 
       ##### 11 (suivant le nombre de ports access à configurer à partir + \ 
       ## de la pos 7 : 7+3+ switchs1 donc ligne nb=3 ) + \ 
       ##### nombre de ports mode trunk si =0 alors pas de création :+ \  
       #####  il y aura autant de lignes qu'il y a de ports trunk à configuer (nbportr)
       ##### 12 config port mode trunk séparateur "-"  \ (postr)
       ##### fa1/1-3-v2(ex: int range fa1/1-3 ...) 
        Utilisation des modules  process et  Netmiko pour se connecter 
############### script Networkcisco.py############################################# 
ce script va sur chaque switch et  éxecuter les commandes pour  la: 
                - création des vlans 
                - des ports access 
                - des ports trunk 
                  pour la connexion On Execute la fonction en utilisant les commandes du module  Netmiko.""" 
                  remote_conn = ConnectHandler(**a_device) 
en passant les paramètres du fichier vconfigs dans la fonction def exec_confcmd(a_device,r1,r2,nbpacc,nbportr,postr)
et on utilise la commande remote_conn.send_config_set("commands") pour les configurations commands représente la chaine string construite à partir des paamètres.

Ensuite exécuter le script sur la machine Administration : administration~# python3 Networkcisco.py
                                ensuite administration~# python3 Networkcisco.py

Dans le cas d'améliorations ou de futures créations j'ai séparé la configuration du coeur en créant deux autres fichiers :
      * Le script esw1network.py pour la configuration et le fichier sw1conf.txt (autant de lignes que de switchs à configurer)
       ############### fichier sw1conf.txt############################################# 
 Ici une configuration pour 1 switches :
           192.168.99.1 ESW1 user cisco 1 4 cisco 0 4 fa0/1-v10/v30 fa1/1-v10/30 fa1/2-v10/30 fa1/3-v10/30
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
############### script esw1network.py############################################# 
ce script va sur chaque switch et  éxecuter les commandes pour  la: 
                - création des vlans 
                - des ports trunk 
                  pour la connexion On Execute la fonction en utilisant les commandes du module  Netmiko.""" 
                  remote_conn = ConnectHandler(**a_device) 
en passant les paramètres du fichier vconfigs dans la fonction def exec_confcmd(a_device,r1,r2,nbpacc,nbportr,postr)
et on utilise la commande remote_conn.send_config_set("commands") pour les configurations commands représente la chaine string construite à partir des paamètres.

Ensuite exécuter le script sur la machine Administration : administration~# python3 esw1network.py
                                ensuite administration~# python3 esw1network.py
Dans les deux scripts pour accélérer les traitements j'utilise la librairie Python threading :
                     my_proc = Process(target=exec_confcmd,args=(a_device,.... 
                     my_proc.start() 
                     procs.append(my_proc) 





![pr6](https://user-images.githubusercontent.com/68608846/92990372-55577980-f4dc-11ea-87ab-66878d8bcc78.JPG)
