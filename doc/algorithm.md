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

#### Vorgehen während des Semesters    
__Erster Ansatz__    
Da von Anfang an klar war, dass der Speicherbedarf zu groß wird, wenn wir den gesamten State speichern, haben wir versucht selbigen zu abstrahieren. Dafür haben wir einen eigenen Zustandsraum definiert, wofür wir, uns da noch unbewusst, auf Features zurückgegriffen haben. Wir haben zB die Distanz der Geister gespeichert und in welcher von 4 Gefahrenkategorien sie sich befinden. Da aber auch der vereinfachte State zu groß für das Handling im RAM wurde, haben wir eine eigene Speicherverwaltung implementiert.
Zu diesem State haben wir je einen Sarsa-Lambda-Agent und einen Q-Learning-Agent implementiert. Dies wurde immernoch zu komplex und führte nicht zu dem gewünschten Ergebnis, weshalb wir diesen State nicht mehr verwenden. Der State ist nun ausgelagert und noch in dem [Git-Branch](https://github.com/Shivon/Pacman_Reinforcement/tree/StateSaveAlternative) in den Dateien ReinforcementSave.py und ReinforcementState.py zu finden.    

__Zweiter Ansatz__    
Bei unserem ersten Ansatz gab es das Problem, dass immernoch zu viele Kombinationsmöglichkeiten der verschiedenen Features und somit zu viele Zustände vorhanden waren. Dadurch kam Pacman nicht häufig genug in die verschiedenen Zustände und konnte so kaum lernen.
Auf der Suche nach anderen oder ergänzenden Ansätzen fanden wir zunächst das unten aufgeführte [Paper1](#Paper_Approx). Daraus ergab sich, dass Pacmans Zustandsraum zu groß wird, um ihn zum Lernen zu verwenden und lineare Approximation unser Problem lösen könnte. Das Paper selbst verwendet statt Features ein regelbasiertes System, uns erschienen Features in Kombination mit einem Q-Learning-Agent aber passender.    

Berechnung eines Feature Wertes:
Beispiel: Sei die Entfernung von Pacman zum nächsten fressbaren Punkt 5 Schritte.
Am Anfang werden alle Features gleich bewertet. Haben wir also vier Features, werden alle mit 25% bewertet.

#### Wieso Approximation und Features
 Die volle Beschreibung eines States sieht folgender Maßen aus:
 * Jedes Feld auf dem Spielfeld kann folgende Zustände annehmen (je punkt 1bit):
  1. Enthält eine Mauer
  1. Enthält ein Fresspunkt
  1. Enthält ein nichtfressbaren Geist
  1. Enthält ein Fressbaren Geist
  1. Enthält Pacman
 * Daraus folgt jedes Feld kann 2⁵ = 32 mögliche Zustände annehmen
 * Angenommen ein Spielfeld besteht aus 20 * 11 = 220
 * Daraus folgt es kann 220³² = 9,068298062×10⁷⁴ mögliche Zustände für das Spielfeld geben. Dies entspricht ungefähr der Anzahl der Atom im Universum
 * Daher ist die Featurebildung unumgänglich

Aber selbst mit Features dauert das Lernen normale Q-Learning verfahren relativ Lange. Mit den von uns gewählten einfachen Features:
* Entfernung zum nächsten Geist
* Entfernung zum nächsten Fresspunkt

werden bereits 160 Spiele benötigt werden, um ein gutes Ergebnis zu erzielen. Dies wird mit weiteren Features deutlich ansteigen.
 
TODO: eigenes Vorgehen während Semester, Erkenntnisse (wieso Approx), Abhängigkeiten von Features (nicht!), Suche (Art),
zweiteilung berechnung + update => Combines Value, als nächstes müsste man nur noch an ReinforcementAgent.py arbeiten (außer fancy Extra-Stuff)

#### Links
* [Unser Git-Repo](https://github.com/Shivon/Pacman_Reinforcement)
* [UC Berkeley API](http://ai.berkeley.edu/project_overview.html)
* [Sutton Buch zu Machine Learning](https://webdocs.cs.ualberta.ca/~sutton/book/ebook/node1.html)
* <a name="Paper_Approx"></a>[Paper1, was uns auf lineare Approximation gebracht hat](http://www.jair.org/media/2368/live-2368-3623-jair.pdf)
* [Paper2, ähnlich zu unserer Lösung, leider zu spät gefunden](https://www.cs.cf.ac.uk/PATS2/@archive_file?c=&p=file&p=263&n=final&f=1-FYP.pdf)
