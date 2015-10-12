## Notizen zur Umsetzung

* Zum Thema __Wegfindung im Labyrinth/ Zustandsraum minimieren__:
	* Problem: Ggf. lernt Agent nur Labyrinth auswendig, wollen wir nicht.	
	* Also: Shortest-path Algo für Wegfindung (zum nächsten Fresspunkt) zu Grunde legen, dann in Zustandsmodellierung an Pacman nur günstigsten nächsten Schritt mitgeben (4 Ausprägungen -> north, west, south, east) => Zustandsraum deutlich eingeschränkt	
	* Zu Geistern: Ob Geist im Weg und wie damit umgegangen ähnlich mitgegeben, wie nächster günstigster Schritt
		* __Ausweichen__ (wenn Geist direkt neben Pacman => Ausweichen)    
		_Umsetzung_: Entfernung zu Geistern mit Shortest-path feststellen und an Pacman weitergeben    
		Gefahrenzonen definieren, Entfernung zu ihm gm Shortest Path in verschiedene Bereiche unterteilen, z.B. 2 Felder entfernt => Gefahrenzone = nah; 7 Felder entfernt => Gefahrenzone = mittel    
		Speicherung in je einem Vektor für Gefahrenzone & Richtung (Zugriffsindex = jeweils 1 Geist)
		* __Fressen__ (Geister brauchen Zustände, ob fressbar oder nicht! Initial alle Geister auf fressbar setzen, wenn großes Pellet gefressen, wenn Geist das erste Mal gefressen wurde, wird er wieder nicht-fressbar)    
	=> ca 2^22 Zustände für 4 Geister, pro Geist erhöht sich die Anzahl an Zuständen um 2^5 (2 Bit Gefahrenzone, 2 Bit Richtung, 1 Bit fressbar/ nicht fressbar)

* Zu Klären: Wie wird umgegangen mit großen Punkten/ wie sieht die Umsetzung dazu aus? Ggf Zustandsraum erweitern oä


## Software für Grundverständnis anschauen:    
	* RL Sim: Simulations-Software für Value Iteration & Q-Learning
	* RL Glue: Kommunikations-Schnittstelle für Verteilte Systeme (?) - hier aber nur Dokumentation interessant, weil Lernen gut erklärt wird