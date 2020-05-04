Rainbow Pages v2 - Writeup
==========================
*shd33*


Le challenge se présente comme une suite au challenge Rainbow Pages. C'est important, car c'est en étudiant comment la version 1 a pu évoluer en version 2 que j'ai pu déduire comment la v2 a été codée.  
La différence principale entre les deux versions semble se situer dans la manière dont le client effectue sa requête :
- En v1, il l'envoyait toute entière `{ allCooks (filter: { firstname: {like: "%'+searchInput+'%"}}) { nodes { firstname, lastname, speciality, price }}}`.
- En v2, il envoie directement `searchInput` au serveur.
Tout laisse à penser que la requête est à peu près la même, à celà près que `searchInput` n'y est plus intégré côté client mais côté serveur, ce qui réduit notre marge de manœuvre.

### 1. Contexte

Pour v1, il m'avait suffi de deviner comment modifier la requête pour obtenir le flag. Pour v2, j'ai besoin de mieux comprendre comment sera traîtée ma requête pour tenter une injection.

La première étape de la résolution a donc été de comprendre quelle est la technologie utilisée côté serveur pour répondre aux requêtes effectuées par le client.
Pour cela, le plus simple est sans doute de provoquer une erreur. J'observe la requête de v1. `%"` devrait provoquer une erreur de syntaxe, si ces caractères ne sont pas échappés. J'ajoute un `console.log(data)` pour voir la réponse du serveur, et je tente.  
Ça marche ! Une injection est visiblement possible. J'obtiens alors la jolie erreur :
`"Syntax Error: Cannot parse the unexpected character "%"."`. Après une rapide recherche google, je comprends que j'ai affaire à GraphQL (technologie que je ne connaissais pas).

### 2. Recherches, 1ère tentative

Je me documente alors sur GraphQL pour en savoir plus sur la syntaxe utilisée.

Je tente une première injection sur la base de la requête utilisée en v1 :
```
{ allCooks (filter: { firstname: {like: "%
------------------
Thibault%"}}) { nodes { firstname, lastname, speciality, price }}, allFlags {nodes {flag}}, allCooks (filter: { firstname: {like: "%Thibault
------------------
%"}}) { nodes { firstname, lastname, speciality, price }}}
```

Celle-ci fonctionne bien en v1, mais me renvoie une erreur en v2. Je me rends alors compte que non seulement la v2 a été rendue plus sécurisée, mais elle a également été améliorée en intégrant la possibilité de chercher les chefs par nom de famille.

La manière la plus simple de faire cela semble être de rajouter une condition `or` dans la requête GraphQL.
Une requête de la forme suivante, donc :
`{ allCooks (filter: { or: [{firstname: {like: "%'+searchInput+'%"}}, {lastname: {like: "%'+searchInput+'%"}}]}) { nodes { firstname, lastname, speciality, price }}}`.

Ainsi, le `searchInput` du client serait injecté à 2 endroits différents, ce qui explique l'erreur lors de la première tentative d'injection.

### 3. 2ème tentative

La solution à cela : commenter la fin de la requête, comme il est classique de le faire poue les injections SQL.
Le symbole de commentaire ici est `#`.

Ainsi, 2ème tentative d'injection :
```
{ allCooks (filter: { or: [{firstname: {like: "%
------------------
Thibault%"}}]}) { nodes { firstname, lastname, speciality, price }}, allFlags {nodes {flag}}}#
------------------
...
```

Le serveur me renvoie l'erreur suivante :
`"Cannot query field "allFlags" on type "Query". Did you mean "allCooks"?"`.
Ce n'est plus une erreur de syntaxe : l'injection est passée ! :)
Mais je n'ai toujours pas le flag :(

### 4. Introspection

Je regarde de plus près : la table `Flag` n'existe plus dans notre base de données... aurait-elle été renommée ? :O

Sans doute, mais heuresement pour moi GraphQL propose une service "d'introspection" !
Et donc... une injection introspective :
`Thibault%"}}]}) { nodes { firstname, lastname, speciality, price }}, __schema {types {name}}}#`
GraphQL obéit, et me renvoie son schéma interne. La table `Flag` a en effet été renommée en `FlagNotTheSameTableName`.
Je devine un `flagNotTheSameFieldName` pour le champ, et je retente mon injection :
```
{ allCooks (filter: { or: [{firstname: {like: "%
------------------
Thibault%"}}]}) { nodes { firstname, lastname, speciality, price }}, allFlagNotTheSameTableNames {nodes {flagNotTheSameFieldName}}}#
------------------
...
```
Bingo !
GraphQL me renvoie gentiment le flag :
`flagNotTheSameFieldName: "FCSC{70c48061ea21935f748b11188518b3322fcd8285b47059fa99df37f27430b071}"`.