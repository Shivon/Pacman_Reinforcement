# Pacman_Reinforcement

Implementing an agent for Pacman, trained by reinforcement learning

### Downloads
Windows requires python 2.* 32Bit and must be added to PATH environment variable.
If you are using a windows operation system then you need to install numpy before you can run this project.
It should be numpy-1.10.1-win32-superpack-python2.7.exe
http://sourceforge.net/projects/numpy/files/NumPy/1.10.1/

### API

We are using the Pacman-API of UC Berkeley, see http://ai.berkeley.edu

### Terminal Usage

For full information: `python <filename> -h`, e.g. `python pacman.py -h`

Often used:
* `python pacman.py -z 0.5 -k 0`
	* `-z`: set zoom level (0..1)
	* `-k`: set number of ghosts
* `python gridworld.py -g MazeGrid -w 100`
	* `-w`: set pixel per box of maze
* `python pacman.py -l originalClassic`
	* `-l`: set map which shall be used


### Launcher

Um den Programmstart einfacher zu machen, haben wir einen Launcher erstellt, mit dem man zu Programmbeginn sämtliche relevanten Konfigurationen angeben kann. Gestartet werden kann dieser über einen Doppelklick auf die Datei `launcher.py` oder auf der Konsole durch den Befehl `python launcher.py`. Für jede der Einstellungen im Launcher sind Standartwerte vorgeben, die jederzeit zurückgesetzt werden können. Weiterhin gibt es die Möglichkeit die aktuellen Konfigurationen zu speichern und wieder zu laden. Die Konfigurationen werden in der Datei `src/settings.ini` gespeichert, welche auch auf der `.gitignore` aufgeführt ist.

Derzeit sind folgende Konfigurationen mit Launcher vorhanden:
* **Spieleinstellungen**:
  * **Anzahl der Trainings**: Gibt die Anzahl der (ungewerteten) Trainingsspiele für den lernenden Agenten an. Diese Option kann nur bei lernenden Pacman-Agenten gesetzt werden!
  * **Anzahl der Spiele**: Gibt die Anzahl der (gewerteten) Spiele an.
  * **Anzahl der Geister**: Gibt die Anzahl der Geister an. Die maximale Anzahl der Geister ist abhängig von Spielfeld, darf allerdings in jedem Fall nicht größer als 5 sein.
  * **Spielfeld**: Gibt an, auf welchem Spielfeld die Spiele durchgeführt werden sollen.
  * **Pacman-Agent**: Gibt an, welcher Agent für Pacman genutzt werden soll.
  * **Feste Random-Seed**: Wenn aktiviert, verhalten sich die Geister im Spiel immer aus gleiche Art und Weise. Kann genutzt werden, um Agenten besser vergleichen zu können.
* **Anzeigeeinstellungen**:
  * **Zoomfaktor**: Gibt an, wie groß das Spielfeld dargestellt werden soll. Ein Wert größer als 1 sorgt dafür, dass das Spielfeld größer als standartmäßig darstellt wird. Ein Wert kleiner als 1 sorgt dafür, dass das Spielfeld kleiner als standartmäßig darstellt wird.
  * **Ausgabe als Text**: Schaltet die GUI ab und stellt das Spielfeld in jedem Zug auf der Konsole dar.
  * **Minimale Ausgabe**: Schaltet die GUI ab und stellt ausschließlich am Ende jeder Spiels die Punktezahl und ob das Spiel gewonnen wurde dar.
  * **Debug-Modus**: Aktiviert Debug-Ausgaben und sorgt dafür, dass der nächste Zug nur durch Tastendruck ausgeführt wird.

##### Änderungen an Konfigurationswerten
Sollten Änderungen an den Konfigurationswerten im Launcher durchgeführt werden (z.B. Hinzufügen weiterer Einstellungen oder Löschen bestehender Einstellungen), sind folgende Stellen im Programmcode anzupassen:
* `LauncherView #initialize(self):`  
Darstellung der Einstellung in der View.

  **Beispiel: Erzeugung einer Textbox** für die Einstellung "Anzahl der Spiele", wobei der Wert der Einstellung im Attribut `numGamesVar` gespeichert wird (als StringVar).
  ``` python
    self.createLabel("Anzahl der Spiele", self.nextRow)
    self.numGamesVar = self.createTextbox(self.nextRow)
    self.finishRow()
  ```

  **Beispiel: Erzeugung einer Drop-Down-Liste** für die Einstellung "Pacman-Agent", wobei der Wert der Einstellung im Attribut `pacmanVar` gespeichert wird (als StringVar). `values` ist eine Liste von Strings, die die möglichen Optionen für die Einstellung beinhaltet.
  ``` python
  self.createLabel("Pacman-Agent", self.nextRow)
  self.pacmanVar = self.createDropDown(self.nextRow, values)
  self.finishRow()
  ```

  **Beispiel: Erzeugung einer Checkbox** für die Einstellung "Ausgabe als Text", wobei der Wert der Einstellung im Attribut `textGraphicsVar` gespeichert wird (als StringVar mit den Werten `"True"` oder `"False"`).
  ``` python
  self.createLabel("Ausgabe als Text", self.nextRow)
  self.textGraphicsVar = self.createCheckBox(self.nextRow)
  self.finishRow()
  ```

  **Beispiel: Erzeugung einer Überschrift** für die Katergorie "Spieleinstellungen".
  ``` python
  self.createHeader("Spieleinstellungen", self.nextRow)
  self.finishRow()
  ```
* `LauncherController #getArgumentArray(self):`  
Generierung des Kommandozeilen-Arguments (siehe [Terminal Usage](#terminal-usage)). Die Variable `argumentValues` in eine Liste von Strings, welche die einzelnen Kommandozeieln-Argumente beinhaltet (vergleichbar mit dem Parameter `args` einer `main`-Methode in Java).

  **Beispiel** für die Einstellung "Anzahl der Spiele".
  ``` python
  argumentValues.append("-x " + self.view.numTrainingVar.get())
  ```

* `LauncherController #getInvalidFields(self):`  
Überprüfung auf Gültigkeit der Einstellungswerte. Die Variable `argumentValues` in eine Liste von Strings, welche die anzuzeigenden Fehlermeldungen enthält (sofern vorhanden).

  **Beispiel** für die Einstellung "Anzahl der Spiele".
  ``` python
  # Datatype checking
  if (not DatatypeUtils.isIntegerString(self.view.numTrainingVar.get())):
    invalidFields.append("'Anzahl der Trainings' muss eine Ganzzahl sein (zum Beispiel: 1)!")

  # Value checking
  if (DatatypeUtils.isIntegerString(self.view.numGamesVar.get())):
    numGamesValue = DatatypeUtils.stringToInteger(self.view.numGamesVar.get())
    if (numGamesValue < 1):
      invalidFields.append("'Anzahl der Spiele' muss groesser oder gleich " + str(1) + " sein!")
  ```

* `LauncherController #loadDefaultSettings(self):`  
Festlegen eines Default-Wertes. Der Wert der Einstellung (im Beispiel `"1"`) ist als String an die `set`-Methode der entsprechenden StringVar (im Beispiel `numGamesVar`) zu übergeben.

  **Beispiel** für die Einstellung "Anzahl der Spiele".
  ``` python
  self.view.numGamesVar.set("1")
  ```

* `LauncherController #loadSettingsFromConfigFile(self):`  
Laden des Einstellungswertes aus der Datei `src/settings.ini`. Der Wert der Einstellung ist als String an die `set`-Methode der entsprechenden StringVar (im Beispiel `numGamesVar`) zu übergeben. Bestimmt wird dieser Wert durch den Aufruf von `get(section, option)`, wobei `section` die Kategorie der Einstellung als String (hier `'GameSettings'`) und `option` der Bezeichner der Einstellung als String ist (hier `numGames`). Der Name der Einstellung wird durch die Methode `LauncherController #saveSettingsToConfigFile` bestimmt (siehe nächster Unterpunkt).

  **Beispiel** für die Einstellung "Anzahl der Spiele".
  ``` python
  self.view.numGamesVar.set(Config.get('GameSettings', 'numGames'))
  ```

* `LauncherController #saveSettingsToConfigFile(self):`  
Speichern des Einstellungswertes in die Datei `src/settings.ini`. Genutzt wird hier die Methode `set(section, option, value)`, wobei `section` und `option` das gleiche bedeuten, wie beim Laden einer Einstellung (siehe vorheriger Unterpunkt) und `value` den Wert der Einstellung darstellt. Dieser wird durch die StringVar der Einstellung bestimmt.

  **Beispiel** für die Einstellung "Anzahl der Spiele".
  ``` python
  Config.set('GameSettings', 'numGames', self.view.numGamesVar.get())
  ```

  Sollte eine neue Kategorie für die Einstellungen eingeführt werden ist vor dem Setzen der entsprechenden Einstellungen durch die `set`-Methode die Methode `add_section(section)` aufzurufen!

  **Beispiel** für die Katergorie "Spieleinstellungen".
  ``` python
  Config.add_section('GameSettings')
  ```

### Einstellungen zur Laufzeit
Es ist möglich die Spielgeschwindigkeit und die Einstellungen für den Learning-Algorithmus zur Laufzeit zu ändern. Dazu können bei aktiviertem Spiel folgende Tasten genutzt werden:
* `O`: Verringern der Spielgeschwindikeit
* `P`: Erhöhen der Spielgeschwindigkeit
* `I`: Zurücksetzen der Spielgeschwindigkeit
* `U`:  Einblendung des Dialoges für die Einstellung des Learning-Algorithmus (beim Öffnen des Dialoges wird das Spiel pausiert bis der Dialog geschlossen wird)

Die Tastaturbelegungen können in der Datei `src/keyBindings.py` angepasst werden. Eine vollständige Liste aller möglichen Werte ist hier zu finden: http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/key-names.html. Die Attribute der Klasse `KeyBindings` müssen dabei mit dem entsprechenden Wert aus der Tabelle in der Spalte `.keysym` gesetzt werden.

Zur Anpassung der Einstellungen für den Learning-Algorithmus ist wie im Kapitel [Änderungen an Konfigurationswerten](#Änderungen-an-konfigurationswerten) vorzugehen, nur das bei den Einstellungen für den Learning-Algorithmus die Dateien `src/runtimeSettings.py` und `src/runtimeSettingsController.py` genutzt werden (statt `src/launcher.py` und `src/launcherController.py`).

### Messung der Lernentwicklung

Um die Lernentwicklung messbar zu machen, haben wir einen zusätzlichen Launcher erstellt, mit dem man zu Programmbeginn sämtliche für die Messung relevanten Konfigurationen angeben kann. Gestartet werden kann dieser über einen Doppelklick auf die Datei `statistics.py` oder auf der Konsole durch den Befehl `python statistics.py`. Für jede der Einstellungen im Launcher sind Standartwerte vorgeben, die jederzeit zurückgesetzt werden können. Weiterhin gibt es die Möglichkeit die aktuellen Konfigurationen zu speichern und wieder zu laden. Die Konfigurationen werden in der Datei `src/statistic_settings.ini` gespeichert, welche auch auf der `.gitignore` aufgeführt ist. Die generierte Ausgabedatei liegt nach Ausführung der Messung in dem Ordner `src/output`, mit dem entsprechenden Dateinamen.

Derzeit sind folgende Konfigurationen mit Launcher vorhanden:
* **Statistikeinstellungen**:
  * **Maximale Anzahl der Trainings**: Gibt die maximale Anzahl der (ungewerteten) Trainingsspiele für den lernenden Agenten an. Die Anzahl Trainingsspiele fängt bei 0 an und steigert sich dann solange, bis der Wert dieser Option erreicht ist. Die Steigerung ist in der Option 'Abstufung der Trainings' angeben.
  * **Abstufung der Trainings**: Gibt an, um viele Trainingsspiele sich der Anzahl der Trainingsspiele erhöhen soll.
  * **Anzahl der Wertungsspiele**: Gibt die Anzahl der (gewerteten) Spiele an.
  * **Ausgabedatei**: Gibt den Namen der Datei an, in der die Ergenisse gespeichert werden sollen. Die Dateiendung (.csv) muss ebenfalls angegeben werden, der Ausgabeordner `output` jedoch nicht.

* **Spieleinstellungen**:
  * **Anzahl der Geister**: Gibt die Anzahl der Geister an. Die maximale Anzahl der Geister ist abhängig von Spielfeld, darf allerdings in jedem Fall nicht größer als 5 sein.
  * **Spielfeld**: Gibt an, auf welchem Spielfeld die Spiele durchgeführt werden sollen.
  * **Pacman-Agent**: Gibt an, welcher Agent für Pacman genutzt werden soll.
  * **Feste Random-Seed**: Wenn aktiviert, verhalten sich die Geister im Spiel immer aus gleiche Art und Weise. Kann (und sollte) genutzt werden, um verschiedene Agenten besser vergleichen zu können.

### Implementationsdetails

* Positionen werden als 2-dimensionale kartesisches Koordinaten (x,y) darstellt. Im Programmcode werden diese Werte als Tupel mit 2 Elementen umgesetzt. Der erste Wert ist die x-Koordinate und der zweite Wert ist die y-Koordinate. Die Benutzung von Tupeln in Python wird hier erläutert: http://www.tutorialspoint.com/python/python_tuples.htm.

  Einzige Ausnahme bei der Umsetzung ist unser [BFS-Suchalgorithmus](#bfs-suchalgorithmus), welcher aus Effitienzgründen 1-dimensionale Koordinaten benutzt. Diese werden vom Algorithmus aus den 2-dimensionale kartesisches Koordinaten berechnet.

* Globale Variablen (also solche die von mehreren Programmteilen benötigt werden) werden in der Klasse `PacmanGlobals` (in der Datei `src/pacmanGlobals.py`) gespeichert.

* Wenn das Rating gesetzt wird und der Wert größer als MaxFloat oder kleiner als MinFloat ist, wird setRating() eine Value Exception werfen und sofort terminieren

### State
<a href="https://rawgit.com/Shivon/Pacman_Reinforcement/master/doc/ReinforcementState.html">PyDoc Eintrag</a><br />
Der ReinforcementState setzt sich aus den Geistern und der Richtung, in die das nächste fressbare Objekt liegt zusammen. Dieser Status ist, und muss bei Änderungen, eindeutig in eine Binärcodierung überführbar sein. <br />
ACHTUNG! Wird die binärrepräsentation geändert, muss auch die Speicherung angepasst werden.

### Saving
<a href="https://rawgit.com/Shivon/Pacman_Reinforcement/master/doc/ReinforcementSave.html">PyDoc Eintrag</a><br>
Das Speichern erfolgt Lokal auf die Festplatte. Der Algorytmus verwendet die Binärrepräsentation des State zur Aderssierung der Werte. Wenn eine Anpassung der Binärrepräsentation gemacht wurde, ist auch eine Anpassung der Speicherung notwendig.<br />
Um das Laden und speichern von Werten zu beschleunigen, und nicht den Arbeitsspeicher unnötig auszulasten, ist ein Seitenersetzungssystem eingebaut. Das heißt, es wir nicht die Vollständige Datei im Arbeitssppeicher gehalten, sondern nur Teile, die dynamisch wechseln. Im Standard Werden 16 MB im Arbeitsspeicher gehalten, und eine Seite beinhaltet 2⁷ Zustände<br />
<br />
TODO: Das Speichern generischer machen, so das nicht jede Änderung am State eine Änderung des Speichervorgang nach sich zieht.<br />
TODO: Z.Z. wir das FIFO Prinzip für die Seitenersetzung genutzt, prüfen ob dies Performancemäßig reicht, oder ob ein anderes Verfahren gewählt werden sollte.

### BFS-Suchalgorithmus
Der BFS-Algorithmus wird von Pacman genutzt, um die nächstgelegende Richtung zum nächsten fressbaren Punkt und zu allen Geistern zu bestimmen. Die Ergebnisse der Resulte werden in einem Objekt der Klasse `ReinforcementState` ([siehe Dokumentation](#state)) gespeichert. Zu finden ist unser Algorithmus in der Klasse `ReinforcementSearch` der Datei `src/bfsSearch.py`.

BFS steht für "breadth-first search" uns ist ein Verfahren der Breitensuche. Eine detalierte Erläuterung des Algorithmus (inkl. Pseudocode) ist hier zu finden: https://de.wikipedia.org/wiki/Breitensuche.

Auf unsere Problemstellung bezogen, läuft der Algorithmus bei uns wie folgt ab:
* `initializeInput(self)`:  
Auslesen der benötigten Daten aus eingehenden Pacman-State, welches durch den Konstruktur als Attribut `self.state` gespeichert wurde. Dabei werden die Positionen aller Wände, fressbaren Punkte, sowie der Geister und Pacman in 1-dimensionale Koordinaten umgewandelt und dann als Attribute gespeichert. Zudem wird gespeichert, ob die Geister fressbar sind oder nicht (für jeden Geist einzeln).
* `executeBFS(self)`:  
Ausführung der Suche. Die Suche wird solange ausgeführt, bis sowohl ein fressbarer Punkt, als auch alle Geister gefunden wurden. Der Punkt, der als erstes gefunden wurde hat die geringste Entfernung zu Pacman und wird daher für das Ergebnis der Suche gespeichert.
Zur Bestimmung aller benachbarten Positionen einer gegebenen Position `position`, welche von Pacman begehbar sind und daher in die Suche einfließen müssen, wird die Methode `getChilds(self, position)` genutzt. Geliefert wird eine Liste von 1-dimensionalen Punkten, die die Nachbarpositionen beinhaltet.  
Der schnellste Weg von Pacman zu einer Position `targetPosition` kann durch die Methode `getPath(self, targetPosition)` bestimmt werden (jedoch erst nach Ausführung der Methode `executeBFS(self)`). Geliefert wird eine Liste von 1-dimensionalen Punkten, die den Weg darstellen. Dabei ist das erste Element die Position `targetPosition` und das letzte Element die Position von Pacman selbst. Der nächste Schritt für Pacman zum Ziel ist damit das vorletzte Element, welches durch den Index `-2` bestimmt werden kann.
* `generateResult(self)`:  
Generierung eines Objekt der Klasse `ReinforcementState` mit dem Ergebnis der Suche.

### Open tasks and bugs

*
