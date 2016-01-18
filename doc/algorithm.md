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
Auf der Suche nach anderen oder ergänzenden Ansätzen fanden wir zunächst das unten aufgeführte [Paper1](http://www.jair.org/media/2368/live-2368-3623-jair.pdf). Daraus ergab sich, dass Pacmans Zustandsraum zu groß wird, um ihn zum Lernen zu verwenden. Bei dem Versuch, den Ansatz des Papers umzusetzen, sind wir darauf gestoßen, dass lineare Approximation unser Problem lösen könnte. Das Paper selbst verwendet statt Features ein regelbasiertes System, uns erschienen Features in Kombination mit einem Q-Learning-Agent aber passender.    

#### Wieso Approximation und Features
Die komplette Beschreibung eines States sieht folgendermaßen aus:
 * Jedes Feld des Spielfeldes kann folgende Zustände annehmen (1 Bit je Punkt):
  1. Enthält eine Mauer
  2. Enthält einen Fresspunkt
  3. Enthält einen nichtfressbaren Geist
  4. Enthält einen fressbaren Geist
  5. Enthält Pacman    
 => Jedes Feld kann 2⁵ = 32 mögliche Zustände annehmen
 * Führt selbst bei Spielfeldern, die kleiner als das Original sind, zu viel zu großen Zustandsräumen
 * Beispiel:
    * Ein Spielfeld bestehe aus 20 * 11 = 220 Feldern (Orginalgröße wäre 27 * 29 )
    * Mögliche Zustände für das Spielfeld: 2⁽⁵*²²⁰⁾ = 2¹¹⁰⁰ = 1,358298529*10³³¹ (zum Vergleich: Anzahl der Atome im Universum ca 10⁸⁰)    
    => Featurebildung unumgänglich

Trotz Vereinfachung des States durch die Features dauert das Training mit dem normalen Q-Learning-Algorithmus immernoch verhältnismäßig lange.
* Gewählten Features:
  * Entfernung zum nächsten Geist
  * Entfernung zum nächsten Fresspunkt
* Dauer des Trainings: 160 Spiele für ein gutes Ergebnis (steigend je zusätzlichem Feature)

#### Berechnung eines Featurewertes
Die Featurewerte stellen eine Gewichtung dar, die mit den feature-spezifischen Eigenschaften verrechnet wird, um eine Bewertung des nächsten Schrittes zu erhalten.    
Die Gewichtung der Features wird am Anfang gleichmäßig verteil, bei 4 Features trägt also jedes Feature anfangs zu 25% zu Gewinn oder Niederlage bei. Diese Gewichtung ist das, was der Agent schlussendlich lernt und immer weiter ausfeilt. Später könnte die Gewichtung dann bei 4 Features zB 10:40:30:20 sein.    

Beispiel am Feature "Entfernung zum nächsten Fresspunkt":    
Sei die Entfernung von Pacman beim einem Schritt nach links zum nächsten fressbaren Punkt 5 Schritte und wir sind am Anfang unseres Spiels mit 4 Features. Die Bewertung des nächsten Schrittes in Richtung dieses Fresspunktes verrechnet dann 25% mit 5 (Distanz). Für die anderen möglichen Richtungen wird ebenfalls so eine Berechnung durchgeführt (wie weit wäre der nächste Fresspunkt von da aus entfernt). Die Richung, mit dem besten Wert, wird dann gewählt.

#### Unabhängikeit von Features
Features müssen ohne Abhängigkeiten voneinander modelliert werden, da sonst das Ergebnis verfälscht wird.    
Unabhängig bedeutet hierbei, dass es keinen kausalen Zusammenhang zwischen dem einen Feature und einem anderen geben darf. Die Feature "Entfernung zum nächsten Fresspunkt" und "Entfernung zum nächsten Geist" sind beispielsweise unabhängig voneinander.    
Abhängig hingegen wären die Features "Entfernung zum nächsten Powerpellet" und "Entfernung zum nächsten fressbaren Geist", da die Geister erst fressbar werden, wenn Pacman ein Powerpellet gefressen hat. Feature "Powerpellet" müsste also eintreten, bevor Feature "fressbarer Geist" interessant für Pacman wird. Pacman würde dies aber nicht lernen, da er solche Zusammenhänge nicht erkennt. Somit könnte es passieren, dass er etwas Falsches lernt, wie dass es richtig sei zu einem Geist zu laufen, auch wenn er nicht fressbar ist.

#### Suchalgorithmus
Wir haben uns für den BFS (Breadth First Search - Standard Breitensuche) entschieden, weil er immer optimal ist und es möglich ist, mehrere Spielgegenstände (Geister, Fresspunkte) gleichzeitig zu suchen.

#### Lernalgorithmus
Wie bereits erwähnt, verwenden wir den Q-Learning-Algorithmus mit linearer Approximation.    
Grundsätzlich entspricht das dem normalen Q-Learning-Algorithmus, im Folgenden der Pseudocode dazu, zunächst vom Agenten:

```
getQValue(state, action){
  //Get the Q-Value of a State Direction Pair
}
setQValue(state, action, value){
  //Set the Q-Value of a State Direction Pair
}

getBestAction(state){
  bestAction = null
  bestVal = Float.getNeagtiveInfinity()
  for(Action action: state.getPossibleActions()){
    tmpVal = getQValue(state, action)
    if(tmpVal > bestVal){
      bestAction = action
      bestVal = tmpVal
    }
  }
  return bestAction, bestVal
}

qLearning(self){
  state = getInitialState()
  while(!game.isEnded){
    action, qVal = getBestAction(state, direction)
    reward, futureState = game.execute(action)
    futureAction, futureQVal = getBestAction(futureState)
    setQValue(state, action, qVal + alpha * (reward + gamma * futureQVal - qVal) )
    state = futureState
  }
}
```

Hier nun der von uns genutzte Algorithmus als Pseudocode, wobei eine Action einer Richtung entspricht, in die Pacman gehen kann:

```
featurePower = Map<Feature, float>() //default is 0.0
getQValue(state, direction){
  combinedValue = 0.0
  for(Feature feature: getFeatures(state, direction)){
    combinedValue += feature.getValue() * featurePower[feature]
  }
  return combinedValue
}

getFeatures(state){
  //returns a List<Features>
}

getBestAction(state){
  bestAction = null
  bestVal = Float.getNeagtiveInfinity()
  for(Action action: state.getPossibleActions()){
    tmpVal = getQValue(state, action)
    if(tmpVal > bestVal){
      bestAction = action
      bestVal = tmpVal
    }
  }
  return bestAction, bestVal
}

qLearning(self){
  state = getInitialState()
  while(!game.isEnded){
    action, qVal = getBestAction(state, direction)
    reward, futureState = game.execute(action)
    futureAction, futureQVal = getBestAction(futureState)
    for(Feature feature: getFeatures(state)){
      featurePower[feature] = featurePower[feature] + alpha * (reward + gamma * futureQVal - qVal) * feature.getValue()
    }
    state = futureState
  }
}
```
Das alles ist im Quellcode in den Methoden updater, getCombinedValue und getAction des Reinforcement__R__Agents zu finden. Die Aufteilung ergibt sich aus der genutzten API, der Updater wird vor jedem Spiel mit dem neuen State gecallt, getAction im Anschluss.

##### Was tun, wenn nicht immer alle Features vorhanden sind?
Es ist wichtig, dass eine FeaturePowerMap auch genau die Features enthält, die man mit getFeatures erhält.
Die Lösung ist eine ```Map<Set<Feature>, Map<Feature, float>>``` einzuführen und immer die FeaturePowerMap zu entnehmen, die zu den erhaltenen Features passt. Eine FeaturePowerMap ist dabei für jeden Zustandsraum, der sich aus der differierenden Feature-Liste ergibt, unterschiedlich und es wird entsprechend neu gelernt.

#### Weiterarbeiten am Projekt
Sollte an diesem Projekt weitergearbeitet werden, so müssen nur Änderungen im ReinforcementAgent.py vorgenommen werden. In dieser Datei könnten die Algorithmen und Features verbessert werden. Möchte man weitere Fancy-Verbesserungen vornehmen (zB am Launcher), so müssen auch andere Dateien ggf verändert werden.
Mögliche Fortsetzungen:
* Geist Intelligenz
* Kampf gegen mehrere Geister
* Geister jagen
* Andere Lernverfahren z.B.:
  * Low-Complexity Rule-Based Policies with Cross-Entropy Method
  * Neuronale Netze
  * Andere Verfahren, die keine lineare Unabhängigkeit vorraussetzen

#### Links
* [Unser Git-Repo](https://github.com/Shivon/Pacman_Reinforcement)
* [UC Berkeley API](http://ai.berkeley.edu/project_overview.html)
* [Sutton Buch zu Machine Learning](https://webdocs.cs.ualberta.ca/~sutton/book/ebook/node1.html)
* [Paper1, was uns auf lineare Approximation gebracht hat](http://www.jair.org/media/2368/live-2368-3623-jair.pdf)
* [Paper2, ähnlich zu unserer Lösung, leider zu spät gefunden](https://www.cs.cf.ac.uk/PATS2/@archive_file?c=&p=file&p=263&n=final&f=1-FYP.pdf)
