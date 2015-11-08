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


### Launcher Usage

For ease of use, you could start our programm via launcher.
This works both with double-click on the file launcher.py or by executing the following terminal command: `python launcher.py`. The prerequisite is that [Python](https://www.python.org/downloads/) is installed on the target computer and Python is registered in the PATH environment variable.

### Implementation details

* Positions are represented by (x,y) Cartesian coordinates and any arrays are indexed by [x][y]
* Actions available for agent: `north`, `west`, `south`, `east` and `stop`

### State
<a href="./doc/ReinforcementSave.html">PyDoc Eintrag</a><br />
Der ReinforcementState setzt sich aus den Geistern und der Richtung, in die das nächste fressbare Objekt liegt zusammen. Dieser Status ist, und muss bei Änderungen, eindeutig in eine Binärcodierung überführbar sein. <br />
ACHTUNG! Wird die binärrepräsentation geändert, muss auch die Speicherung angepasst werden.

### Saving
<a href="./doc/ReinforcementSave.html">PyDoc Eintrag</a><br>
Das Speichern erfolgt Lokal auf die Festplatte. Der Algorytmus verwendet die Binärrepräsentation des State zur Aderssierung der Werte. Wenn eine Anpassung der Binärrepräsentation gemacht wurde, ist auch eine Anpassung der Speicherung notwendig.<br />
Um das Laden und speichern von Werten zu beschleunigen, und nicht den Arbeitsspeicher unnötig auszulasten, ist ein Seitenersetzungssystem eingebaut. Das heißt, es wir nicht die Vollständige Datei im Arbeitssppeicher gehalten, sondern nur Teile, die dynamisch wechseln. Im Standard Werden 16 MB im Arbeitsspeicher gehalten, und eine Seite beinhaltet 2⁷ Zustände<br />
<br />
TODO: Das Speichern generischer machen, so das nicht jede Änderung am State eine Änderung des Speichervorgang nach sich zieht.<br />
TODO: Z.Z. wir das FIFO Prinzip für die Seitenersetzung genutzt, prüfen ob dies Performancemäßig reicht, oder ob ein anderes Verfahren gewählt werden sollte.

### Open tasks and bugs

*
