CryptoLocker - writeup
======================
*shd33*


J'utilise Volatility pour analyser le memory dump. Celui-ci a été fait sur une machine sous Windows7 : il existe donc un profil embarqué par défaut dans Volatility pour analyser le dump (Win7SP0x86).

Je fais un `pslist` pour regarder les processus en cours d'exécution.
Je remarque un processus suspect, qui porte un nom inconnu : `update_v0.5.exe`.
Sûrement le malware en question !

J'extrais donc le binaire correspondant au processus en question à l'aide de `procdump`.
Il s'agissait en effet du malware !

Toutefois, je me rends compte que celui-ci a déjà chiffré le flag :/

J'essaie d'abord de regarder la la mémoire du programme pour voir s'il ne contient pas encore le flag en clair, mais je ne l'y trouve pas...

Je télécharge le flag encrypté à l'aide de l'outil de récupération de fichiers de Volatility, et je désassemble l'exécutable pour voir quelle méthode de chiffrement il a utilisé.

Je me rends alors compte que le cryptolocker n'utilise qu'un chiffrement par XOR !

En faisant à mon tour un XOR sur le `flag.txt.enc` avec la même clé, je récupère le flag :)