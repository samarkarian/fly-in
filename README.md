## Chapter VI

## Chapitre VI — Format du fichier d'entrée

- La première ligne contient le nombre de drones utilisés => `nb_drones: INT`

- Zone de départ : `start_hub: hub 0 0 [color=green]`
- Zone d'arrivée : `end_hub: goal 10 10 [color=yellow]`

- Les hubs sont les zones où peuvent stationner les drones :
    - `hub: roof1 3 4 [zone=restricted color=red]`
    - `hub: roof2 6 2 [zone=normal color=blue]`
    - `hub: corridorA 4 3 [zone=priority color=green max_drones=2]`
    - `hub: tunnelB 7 4 [zone=normal color=red]`
    - `hub: obstacleX 5 5 [zone=blocked color=gray]`

    - `zone=normal`     : coûte 1 tour (par défaut)
    - `zone=blocked`    : le drone ne doit pas entrer ni passer par ce hub
    - `zone=restricted` : coûte 2 tours
    - `zone=priority`   : coûte 1 tour, et le chemin doit passer en priorité par ici

- Les couleurs sont optionnelles et peuvent être utilisées pour la représentation visuelle :
    - Les valeurs acceptées sont toutes les chaînes de caractères valides composées
      d'un seul mot (ex. : red, blue, gray). Il n'existe pas de liste fixe de couleurs autorisées.

- Les connexions :
    - `connection: hub-roof1`
    - `connection: hub-corridorA`
    - `connection: roof1-roof2`
    - `connection: roof2-goal`
    - `connection: corridorA-tunnelB [max_link_capacity=2]`
    - `connection: tunnelB-goal`

    - Elles définissent une liaison **bidirectionnelle** entre deux zones
    - Les noms de zones ne doivent **pas** contenir de tiret (interdit par la syntaxe des connexions)
    - `max_link_capacity` (par défaut : 1) : nombre maximal de drones pouvant
      emprunter simultanément cette connexion

- Les commentaires commencent par `#` et sont ignorés.

- Les coordonnées des zones sont toujours des entiers.
- Il y a toujours exactement une zone de départ et une zone d'arrivée.

## Chapter VII

## VII.1 — Pathfinding et algorithme

- Les drones peuvent se déplacer simultanément
- L'algorithme doit gérer :
    - La distribution des drones sur plusieurs chemins
    - L'attente stratégique si le déplacement est bloqué
    - L'évitement des conflits et interblocages
- Il doit prendre en compte :
    - Les coûts de déplacement selon le type de zone
    - La planification par tour (éviter les collisions)
    - La structure du graphe (chemins disjoints ou chevauchants)
    - Les capacités : max_drones (zone) et max_link_capacity (connexion)
- Une représentation visuelle est obligatoire :
    - Sortie terminal colorée ET/OU interface graphique

## VII.2 — Règles d'occupation des zones

- Par défaut : max 1 drone par zone par tour
- Exception : zones avec max_drones=N => jusqu'à N drones simultanément
- Exceptions spéciales :
    - Zone de départ : tous les drones peuvent y cohabiter au début
    - Zone d'arrivée : plusieurs drones peuvent y arriver (considérés comme livrés)
- Un drone ne peut pas entrer dans une zone qui dépasserait sa capacité maximale
- max_link_capacity : limite le nombre de drones traversant une connexion simultanément
- Les drones quittant une zone libèrent de la capacité pour ce même tour

## VII.3 — Mécanique des déplacements et des tours

- À chaque tour, un drone peut :
    - Se déplacer vers une zone adjacente (si capacité disponible)
    - Entrer dans une connexion vers une zone restricted (2 tours) :
        - Il DOIT atteindre la destination au tour suivant
        - Il NE PEUT PAS attendre sur la connexion
    - Rester en place (attente ou blocage)

- Coût de déplacement selon le type de la zone DESTINATION :
    - normal    => 1 tour
    - restricted => 2 tours (occupe la connexion pendant le transit)
    - priority  => 1 tour (à privilégier dans le pathfinding)
    - blocked   => inaccessible

## VII.4 — Contraintes du parseur

- Première ligne obligatoire : nb_drones: <entier_positif>
- Exactement 1 start_hub et 1 end_hub
- Chaque zone : nom unique + coordonnées entières valides
- Noms de zones : tout caractère sauf tirets et espaces
- Connexions : uniquement entre zones déjà définies
- Pas de connexion en double (a-b == b-a)
- Types de zones valides : normal | blocked | restricted | priority
- Capacités (max_drones, max_link_capacity) : entiers positifs uniquement
- Toute erreur => arrêt du programme + message clair (ligne + cause)

## VII.5 — Format de sortie

- Une ligne par tour de simulation
- Format : D<ID>-<zone> ou D<ID>-<connexion> (si en transit vers restricted)
- Les drones immobiles sont omis de la ligne
- Les drones arrivés à destination ne sont plus affichés
- La simulation s'arrête quand tous les drones sont arrivés

- Exemple :
    D1-roof1 D2-corridorA
    D1-roof2 D2-tunnelB
    D1-goal  D2-goal

## VII.6 — Système de notation

- Critère principal : nombre total de tours (moins = mieux)
- La simulation doit :
    - Respecter toutes les règles de déplacement et d'occupation
    - Gérer les coûts de déplacement par type de zone
    - Respecter les capacités (zones et connexions)
    - Éviter tout conflit

- Métriques secondaires (optionnelles) :
    - Nombre de drones déplacés par tour
    - Nombre moyen de tours par drone
    - Coût total des chemins
    - Qualité de la représentation visuelle

## VII.7 — Benchmarks de performance

| Difficulté | Carte                        | Drones | Cible     |
|------------|------------------------------|--------|-----------|
| Facile     | Chemin linéaire              | 2      | ≤ 6 tours |
| Facile     | Fourche simple               | 3      | ≤ 6 tours |
| Facile     | Capacité de base             | 4      | ≤ 8 tours |
| Moyen      | Piège impasse                | 5      | ≤ 15 tours|
| Moyen      | Boucle circulaire            | 6      | ≤ 20 tours|
| Moyen      | Puzzle priorité              | 4      | ≤ 12 tours|
| Difficile  | Labyrinthe cauchemardesque   | 8      | ≤ 45 tours|
| Difficile  | Enfer de capacité            | 12     | ≤ 60 tours|
| Difficile  | Défi ultime                  | 15     | ≤ 35 tours|
| Challenger | Le Rêve impossible           | 25     | < 45 tours|