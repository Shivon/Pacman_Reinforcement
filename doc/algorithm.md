### Reinforcement Algorithmus: Lineare Approximation

#### Vorwort Pacman
Die Spielfigur Pac-Man muss Punkte in einem Labyrinth fressen, während sie von Gespenstern verfolgt wird. Frisst man eine „Kraftpille“ (im Folgenden "PowerPellet"), kann man für eine gewisse Zeit umgekehrt selbst die (nun weiß eingefärbten) Gespenster verfolgen. [Wikipedia-Artikel dazu](https://de.wikipedia.org/wiki/Pac-Man)

#### Relevante Begriffe
* __Pacman__: Die gelbe Spielfigur: ![Hier sollte ein gelber Halbkreis mit offenem Maul sein](http://files.softicons.com/download/game-icons/classic-games-icons-by-thvg/png/24/Pacman.png "Pacman \o/")
* __Geister__: Die bunten Geister zB: ![Beispielgeist in Rot](http://files.softicons.com/download/game-icons/classic-games-icons-by-thvg/png/24/Pacman%201.png "Beispielgeist")
* __Fresspunkte__: Die kleinen weißen Punkte (in der API von UC Berkeley "Food" genannt)
* __PowerPellet__: Die großen weißen Punkte (in der API von UC Berkeley "Capsule" genannt)
* __State__: Der State ist ein Zustand des Zustandsraums des gesamten Spiels. Es beinhaltet alle Positionen der (noch existenten) Fresspunkte, PowerPellets, Geister und deren Zustand sowie Pacman selbst.
* __Feature__: Ein Feature ist eine für den Agenten interessante Teilausprägung des States wie zB der nächstgelegene Fresspunkt. Dabei verwendet es bestimmte Aspekte des States (in diesem Beispiel die Position von Pacman und die der Fresspunkte) und berechnet auf ihrer Grundlage den entsprechenden Rückgabewert. Dieser wird für jede mögliche Richtug, in die Pacman gehen kann berechnet, sodass er zB am Ende weiß, welcher Fresspunkt in welche Richtung am nächsten ist.

#### Einführung
Wir haben in Python unter Verwendung der UC Berkeley API einen Agenten für Pacman implementiert, die Geister selber werden momentan von einem Random-Agenten gesteuert.
Um unseren Agenten zu trainieren, haben wir den Q-Learning-Algorithmus gewählt und arbeiten zur Vereinfachung des States mit linearer Approximation. Dies heißt im Konkreten, dass wir uns im State auf ein paar wesentliche Features beschränken, anstatt den gesamten State abzuspeichern. Momentan werden die Features "nearestFoodDist" und "nearestGhostDistance" im Masterbranch verwendet. Es gibt noch separate Branches, in denen jeweils die Features "nearestEatableGhost" und "nearestSafeJunction" implementiert, aber noch nicht ausgereift sind. Hier unser [Git-Repo](https://github.com/Shivon/Pacman_Reinforcement).

#### Grobe Beschreibung:
Wir arbeiten mit Feature. Ein Feature ist z.B. die Entfernung zu dem nächsten Punkt oder zum nächsten Geist.
Diese Zahlen werden dann miteinander verechnet und Pacman lernt in welchem Verhältnis die Features sein müssen.  

#### Genauere Beschreibung:
Unsere Features lauten:
* Entfernung zum nächsten Fresspunkt (Kleine Punkte im Spiel)
* Entfernung zum nächsten Geist (Nicht fressbare Geister)
* Entfernung zur nächsten Safe Junction (Safe Junction ist eine Kreuzung mit mehr als zwei/drei Richtungen)
* Entfernung zum nächsten Powerpellit (Große Punkte im Spiel)

Berechnung eines Feature Wertes:
Beispiel: Sei die Entfernung von Pacman zum nächsten fressbaren Punkt 5 Schritte.
Am Anfang werden alle Features gleich bewertet. Haben wir also vier Features, werden alle mit 25% bewertet.


#### Links
* [Unser Git-Repo](https://github.com/Shivon/Pacman_Reinforcement)
* [UC Berkeley API](http://ai.berkeley.edu/project_overview.html)
* [Was uns auf lineare Approximation gebracht hat](http://www.jair.org/media/2368/live-2368-3623-jair.pdf)
