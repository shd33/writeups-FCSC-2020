Bestiary - writeup
==================
*shd33*


En regardant le code source de la page, je me rends compte que des requêtes GET sont faites au serveur en passant le nom du monstre souhaité.
J'essaie alors de demander à la page un monstre inexistant - le monstre "bonjour", par exemple - et j'obtiens l'erreur suivante :
`Warning: include(bonjour): failed to open stream: No such file or directory in /var/www/html/index.php on line 33
Warning: include(): Failed opening 'bonjour' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 33`.

Le script PHP semble passer directement la chaîne de caractères envoyée à la fonction `include`, signe qu'une attaque LFI est possible.

J'essaie alors de demander au serveur de me montrer le monstre "flag". Non seulement le monstre tant attendu ne s'affiche pas, mais en plus de cela je ne reçois plus d'erreur liée à une mauvaise inclusion. J'essaie avec d'autres monstrer similaires : "flag.txt", "flag.php" etc. mais rien n'y fait, le résultat est toujours le même. Je soupconne alors le serveur de filtrer les requêtes contenant le mot interdit.

Je vérifie cela sur un monstre exotique : "bonjourflagmonster33". Toujours pas d'erreurs, ce qui confirme mes soupçons.

Il faut donc trouver un moyen d'accéder au flag sans passer directement pas index.php... Je tente donc un log poisoning.

Je cherche donc dans des emplacements classiques de logs. Je ne trouve rien de très intéressant, jusqu'à ce que je tombe sur `/proc/self/fd/10` qui affiche la dernière requête de monstre effectuée depuis ma session.

Je peux donc envoyer au serveur une requête de monstre contenant un script php à exécuter, et lire le résultat dans `/proc/self/fd/10` !

J'essaie avec `<?php print_r(scandir('/var/www/html'));?>`. Je constate qu'il y a bien un fichier `flag.php` à la racine.
J'essaie alors de l'ouvrir avec `<?php show_source('f' . 'lag.php');?>` (j'ai pris soin de ne pas écrire "flag" dans l'expression pour éviter le filtre).
Le serveur me répond avec l'erreur suivante : `Warning: show_source() has been disabled for security reasons in /var/www/html/sessions/sess_5d44ff62ffd51ca63063d619c68f734e on line 1`.

Je vais donc sur la doc de php pour voir s'il n'existe pas une autre fonction ayant un rôle similaire. En effet, il apparaît que `show_source` est un alias de `highlight_file` !
J'essaie donc : `<?php highlight_file('f' . 'lag.php');?>`.

Je vais voir dans `/proc/self/fd/10` : le flag s'y trouve :)