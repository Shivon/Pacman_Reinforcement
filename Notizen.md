## Notizen zur Umsetzung

* Zum Thema __Wegfindung im Labyrinth/ Zustandsraum minimieren__:
	* Problem: Ggf. lernt Agent nur Labyrinth auswendig, wollen wir nicht.	
	* Also: Shortest-path Algo für Wegfindung zu Grunde legen, dann in Zustandsmodellierung an Pacman nur günstigsten nächsten Schritt mitgeben (4 Ausprägungen -> north, west, south, east) => Zustandsraum deutlich eingeschränkt	
	* Zu Geistern: Ob Geist im Weg und wie damit umgegangen ähnlich mitgegeben, wie nächster günstigster Schritt
		* __Ausweichen__ (wenn Geist direkt neben Pacman => Ausweichen)    
		_Umsetzung_: Entfernung zu Geistern mit Shortest-path feststellen und an Pacman weitergeben    
		Gefahrenzonen definieren, Entfernung zu ihm gm Shortest Path in verschiedene Bereiche unterteilen, z.B. 2 Felder entfernt => Gefahrenzone = nah; 7 Felder entfernt => Gefahrenzone = mittel    
		Speicherung in Gefahrenmatrix: Jede Zeile = 1 Geist, Spalten = Gefahrenzone & Richtung
		* __Fressen__ (Geister brauchen Zustände, ob fressbar oder nicht! Initial alle Geister auf fressbar setzen, wenn großes Pellet gefressen, wenn Geist das erste Mal gefressen wurde, wird er wieder nicht-fressbar)


## Software für Grundverständnis anschauen:
	* RL Sim: Simulations-Software für Value Iteration & Q-Learning
	* RL Glue: Kommunikations-Schnittstelle für Verteilte Systeme (?) - hier aber nur Dokumentation interessant, weil Lernen gut erklärt wird