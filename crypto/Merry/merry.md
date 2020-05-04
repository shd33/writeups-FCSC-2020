Merry - Writeup
===============
*shd33*


### 1. Observations

Le Merry se présente comme un serveur permettant d'initier des échanges de clés de manière sécurisée.
Pour cela, il génère une bi-clé, donne la clé publique au client. Celui-ci peut alors générer sa propre clé et renvoie au serveur de quoi générer la clé commune.

...enfin, dans l'idée, car en regardant le code de plus près l'implémentation me semble assez étrange.

Déjà, toutes les clés sont des matrices. Ok, pourquoi pas. Les clés privées du serveur sont uniquement composées de -1, 0 et 1. Étonnant.

La fonction `__decode` effectue des opérations exotiques sur nos matrices pour semble-t-il les renormaliser. Très étonnant.

De plus, il est possible d'envoyer la clé commune au serveur en même temps que les matrices pour la générer, et de savoir sa l'échange de clés a "réussi".
En gros, ont peut faire effectuer au serveur un calcul impliquant sa clé privée `__S_a` sur les matrices que l'on veut, et avoir des retours sur le résultat du calcul.

Plus précisément, on peut savoir si l'on a bien deviné le résultat du calcul effectué par le serveur. Difficile sans connaître sa clé privée à priori, mais la clé commune est très petite (matrice 4\*4).

### 2. Trouver `__S_a`

C'est là-dessus que l'on va s'appuyer pour retrouver `__S_a`.
Le calcul de la clé commune côté serveur est le suivant : `key_a = self.__decode(np.mod(C - np.dot(U, self.__S_a), self.q))`. `U` et `C` sont les matrices (de tailles 4\*280 et 4\*4 respectivement) que l'on envoie au serveur. `U * __S_a`... on peut donc "sélectionner" une ligne de la clé `__S_a` en plaçant un unique 1 sur la colonne correspondante de `U`.

Mais essayer de deviner une ligne de `__S_a` prendrait donc en moyenne (3^4)/2 = 40,5 requêtes. Il y a 280 lignes à deviner : cela nous amène à plus de 11000 requêtes au serveur, en moyenne. C'est un peu beaucoup. Mais on peut optimiser !

En effet, on peut aussi choisir la patrice `C`, et tirer profit des propriétés de la fonction `__decode` pour deviner d'abord la position des 0, puis la position des -1.

Je passe ici les calculs, le code est en PJ.

Deviner une ligne de `__S_a` en deux temps prend donc en moyenne (2^4 + 2^4)/2 = 16 essais. Pour 280 lignes, cela fait moins de 5000 requêtes au serveur. On pourrait encore faire quelques petites optimisations, mais ça me semble raisonnable.

### 3. Trouver `__E_a`

La deuxième clé privée, `__E_a`, n'apparaît pas dans le calcul de clé partagée. Toutefois, elle est utilisée lors de la génération des clés publiques du serveur : `B = (A*__S_a + __E_a)%q`. On connaît A, B et q et on vient de voir comment trouver `__S_a`. C'est donc facile de trouver `__E_a` en faisant les opérations inverses, et en faisant attention à ce qu'elle ne contienne que des 0, 1 et -1 (pas de 'q-1'...).

### 4. Du code

Je code les fonctions que je viens de décrire, et je lance le script. Au bout d'une dizaine de minutes et quelques milliers de requêtes, le flag apparaît :)