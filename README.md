# Pacman_Reinforcement

Implementing an agent for Pacman, trained by reinforcement learning

### Downloads
Windows requires python 2.* 32Bit
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

Um den Programmstart einfacher zu machen, haben wir einen Launcher erstellt, mit dem man zu Programmbeginn sämtliche relevanten Konfigurationen angeben kann. Für jede dieser Einstellungen sind Standartwerte vorgeben, die jederzeitig im Launcher zurückgesetzt werden können. Weiterhin gibt es die Möglichkeit die aktuellen Konfigurationen zu speichern und wieder zu laden. Die Konfigurationen werden in der Datei `src/settings.ini` gespeichert, welche auch auf der `.gitignore` aufgeführt ist.

##### Konfigurationswerte des Launchers
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
Generierung des Kommandozeilen-Arguments (siehe [Terminal Usage](#TerminalUsage)). Die Variable `argumentValues` in eine Liste von Strings, welche die einzelnen Kommandozeieln-Argumente beinhaltet (vergleichbar mit dem Parameter `args` einer `main`-Methode in Java).

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


### Implementation details

* Positions are represented by (x,y) Cartesian coordinates and any arrays are indexed by [x][y]
* Actions available for agent: `north`, `west`, `south`, `east` and `stop`

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

### Open tasks and bugs

*
