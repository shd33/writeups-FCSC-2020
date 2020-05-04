Premiers artéfacts - writeup
============================
*shd33*


Le plus compliqué a été la génération du profil Volatility adapté au système un peu particulier sur lequel le dump a été effectué.

En effet, Volatility ne propose pas de profils par défaut pour les systèmes GNU/Linux.
Comme vu lors du challenge *C'est la rentrée*, le dump a été effectué sur une machine sous Debian Bullseye, avec un kernel Linux 5.4.0-4-amd64. J'installe donc une VM avec la bonne version de Debian. Toutefois, je me rends compte que le kernel livré avec Debian Bullseye n'est plus le même que lorsque le dump a été effectué (5.5 depuis avril 2020...).

J'installe donc le bon kernel, mais apt refuse de télécharger les headers linux correspondants... J'installe donc les headers, ainsi que toutes leurs dépendances à la main...

Je peux enfin fabriquer le profil voulu !! :)

Je commence alors l'analyse dans Volatility.

J'exécute `linux_pslist`, mais le processus 1254 n'apparaît pas :/
Je réessaie avec `linux_psscan`. Cette fois-ci ça marche !

Je retrouve la commande lancée à l'heure indiquée avec l'instruction `linux_bash`.

Pour le nombre d'IP-DST uniques, j'essaie `linux_netscan` et `linux_netstat` (+ grep ESTABLISHED) qui me renvoient toutes deux le même résultat.