Macaron - writeup
=================
*shd33*


Macaron est une tentative (ratée) d'implémentation de HMAC pour signer at authentifier des messages de manière sécurisée.

Je commence par faire des recherches sur HMAC, et les différentes fonctions utilisées (padding...) pour bien comprendre tout le code.

L'algorithme permet de générer un "macaron cryptographique" pour un message donné en entrée, ainsi que de vérifier une telle signature pour un message.
Si l'on parvient à générer un macaron valide pour un message non encore macaroné, on obtient le flag.

Pour générer le macaron, le serveur coupe ce dernier en blocs de 30 bytes et ajoute devant chaque bloc un nonce de 2 bytes qui s'incrémente. Il applique ensuite la fonction hmac (avec la 1ère clé privée, et sha256 comme fonction de hachage) sur chaque bloc de 64 bytes, en se décalant de 32 bytes à chaque fois, et fais un XOR binaire sur tous les hashs obtenus.
Pour finir, il applique hmac avec la deuxième clé privée au résultat.

### La faille

La faille se site à deux niveaux. Le premier est au niveau du XOR - on va profiter du fait que `a XOR a = 0`. Le deuxième est au niveau du nonce : l'algorithme de génération de macaron ajoute des nonce différents devant chaque bloc de 30 bytes du message, mais l'algorithme de vérification des macarons nous laisse choisir l'ensemble des nonces qui seront préfixés aux blocs !

### La solution

- On génère un macaron pour un message de 59 bytes (ainsi le padding rajoutera juste \x01 à la fin) : `00000000000000000000000000000'\x01'00000000000000000000000000000`. Ce message, avec le padding ajouté est constitué de deux partie égales 0...0'\xO1'.
- On vérifie le message de 2\*60-1 bytes suivant :
`00000000000000000000000000000'\x01'00000000000000000000000000000'\x01'
00000000000000000000000000000'\x01'00000000000000000000000000000`  
avec le tag donné à l'étape précédente, et le nonce `0000000100010001`.

Les deux derniers `big_block` hashés sont donc les mêmes (`00000000000000000000000000000'\x01'00000000000000000000000000000'\x01'`) et ont par conséquent le même hash. Ainsi le XOR les annule et le tag obtenu est le même que pour le premier message.