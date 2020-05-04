Chapardeurs de mots de passe - writeup
======================================
*shd33*


Je regarde à quoi ressemble la capture réseau dans wireshark. Il y a beaucoup trop de paquets pour tout analyser à la main. Je regarde les différentes adresses ip distantes. Elles sont assez nombreuses, et il semble y avoir un peu de tout. Il semblerait d'ailleurs que notre ami s'intéresse beaucoup aux network forensics :P

Pour cibler mon analyse, je fais des recherches sur le virus KPOT v2.0.

Je comprends alors qu'il se communique avec une interface de gestion à distance, par l'intermédiaire de requêtes HTTP GET et POST. Il semblerait de plus qu'une telle interface se situe à des url se terminant en `gate.php`.

Un filtrage dans wireshark sur le mot "gate" me permet de trouver l'IP du serveur distant : `203.0.113.42`.

Je filtre alors sur cette IP pour avoir un aperçu de l'ensemble des paquets échangés.
Seule une requête POST a été envoyée par le virus ! Sans doute le flag.

Toutefois, comme je l'avais vu en me renseignant sur KPOT v2.0, le virus "chiffre" ses requêtes en effectuant un XOR avec une clé fixée de 16 bytes.

Pour retrouver la clé et déchiffrer le flag, je regarde la réponse à la requête GET correspondant à la demande d'envoi du flag. Normalement, elle devrait être encodée en base64 et "chiffrée" avec la même clé que le flag. D'après mes recheches, cette réponse HTTP a une forme particulière. En effet, elle commence par une série de 16 0/1 qui correspondent à des flags utilisés par le virus, puis contient des informations sur la nature des fichiers à chercher, délimitées par le mot clé `__DELIMM__`.

Je tente alors un XOR avec `1111111111111111`, je récupère les 16 premiers caractères du résultat, et j'effectue un XOR avec ceux-ci. Petit à petit, en changeant des 1 en 0 là où des caractères étaient mal décodés (notamment en regardant `__DELIMM__` et `__GRABBER__`...), je reconstitue la clé.

Celle-ci est : tDlsdL5dv25c1Rhv.

La réponse à la requête GET est :
```
0110101110111110__DELIMM__218.108.149.373__DELIMM__appdata__GRABBER__*.log,*.txt,__GRABBER__%appdata%__GRABBER__0__GRABBER__1024__DELIMM__desktop_txt__GRABBER__*.txt,__GRABBER__%userprofile%\Desktop__GRABBER__0__GRABBER__0__DELIMM____DELIMM____DELIMM__
```

Et le flag est :
```
_DRAPEAU_P|us2peurQue2M4l!  R4ssur3z-Votre-Am1-Et-vo1c1Votredr4peau_FCSC
{469e8168718996ec83a92acd6fe6b9c03c6ced2a3a7e7a2089b534baae97a7}
_DRAPEAU_
```