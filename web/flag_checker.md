Flag Checker - writeup
======================
*shd33*


Le challenge se présente comme un outil de vérification de flags.
En jetant un coup d'œil au code source, je me rends compte que tout est exécuté côté client :)
Mais le js est horrible à lire :(

Je commence auto-indenter le js pour y voir plus clair. Je comprends qu'il s'agit d'un wrapper pour exécuter du code C dans le navigateur. En particulier, il appelle un script WebAssembly qui est le cœur du flag checker.

D'après le script.js, la fonction "check" correspond à la fonction `b` du fichier wasm. Celle-ci effectue un XOR sur l'entrée avec 3 (répété), puis elle appelle la fonction `$func3` qui compare le résultat à la chaîne ``E@P@x4f1g7f6ab:42`1g:f:7763133;e0e;03`6661`bee0:33fg732;b6fea44be34g0~``.

Je fais donc un XOR sur cette chaîne pour inverser l'opération, et j'obtiens le flag.