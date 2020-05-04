Pippin - writeup
================
*shd33*


Cette fois-ci, le code n'est plus disponible, et on ne peut plus faire autant de requêtes que l'on veut (elles sont limitées à 3000).
C'est embêtant, mais l'énoncé indique que la génération des clés ne fonctionne plus très bien.

Je lance alors le script fraîchement préparé pour merry sur le serveur de pippin, en affichant les lignes de `__S_a` dans l'espace des 3000 requêtes disponibles.
Je vois que chaque ligne de la clé `__S_a` contient exactement deux 0, un 1 et un -1.

Si c'est toujours vrai, on peut réduire de nombre de requêtes nécessaires pour déterminer une ligne de `__S_a` :
- il y a 6 possibilités pour les emplacements des 0
- quand on connaît la position des 0, il n'y a que deux possibilités restantes (-1 suivi de 1, ou l'inverse).

On réduit donc le nombre moyen de requêtes effectuées par deux. C'est suffisant pour passer en-dessous de la barre des 3000 et obtenir le flag :)