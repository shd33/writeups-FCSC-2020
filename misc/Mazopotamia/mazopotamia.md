Mazopotamia - writeup
=====================
*shd33*


Mazopotamia a été pour moi un challenge assez dissuasif. Récupérer l'information sous forme d'image, je n'en avais pas particulièrement envie :P

En fin de compte il s'est avéré être assez rigolo :)

En effet, toutes les images avaient un format plutôt sympa : des png organisés en blocs de 64 pixels, avec des marges de dimensions fixes.

Après avoir codé la connexion au serveur et la reconnaissance d'image, il ne restait plus que l'algorithme.
L'exploration de labyrinthes me fait penser à un algo de type flood-fill (DFS). La seule différence avec une exploration classique est la présence de couleurs. Pour cela, j'ajoute une dimension au problème : au lieu de me souvenir de si une case a déjà été visitée, je me souviens de si elle a été visitée en provenant d'une couleur donnée. De même pour la détermination des cases précédentes et la reconstitution du chemin.

L'algorithme fonctionne, je récupère le flag !

(le code est en PJ)