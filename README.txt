Pour lancer le jeu en local avec le protocole TLS sur la même machine on lance le main pour le serveur (le certificat donné n'étant actif que pour l'adresse IPv4 127.0.0.1 qui est l'adresse localhost pour beaucoup de machines):
./main.py   
puis pour les clients:
./main.py 127.0.0.1 7777

Sinon on peut mettre en commentaire les références au protocole TLS dans le fichier reseau.py
(la démarche y est expliquée en commentaire à la fin du fichier)

et lancer le serveur de cette manière:
./main
puis les clients:
./main.py 'Adresse_IPv4 ou v6 si modification' 7777


