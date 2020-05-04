Clepsydre - writeup
===================
*shd33*


Le challenge clepsydre est très déroutant. Le serveur demande un mot de passe, et pour le trouver j'ai comme seules indications la définition wikipédia d'une clepsydre et une citation de La Fontaine...

Malgré le peu d'informations, tout tourne autour du temps. Je pense alors à une attaque par canal auxiliaire basée sur le temps.
Je tente plusieurs premières lettres pour le mot de passe en regardant le temps de réponse du serveur dans wireshark (pour être sûr de connaître précisément le temps d'envoi et de réception des paquets). Toutefois je n'obtiens rien (j'avais oublié des lettres :P).

Je finis par essayer de rentrer comme mot de passe la citation. Et là, le serveur met considérablement plus de temps à répondre (1 seconde, exactement). Je code donc un script python qui tente successivement une liste de caractères alphanumériques et mesure le temps de réponse du serveur. SI ce temps a augmenté de 1 seconde, il passe au caractère suivant.

Au bout de quelques minutes, ma patience est récompensée lors de l'essai 'T3mp#!' par un gentil message contenant le flag :)

(le code est en PJ)