## Notizen zur Umsetzung

* Zum Thema __Wegfindung im Labyrinth/ Zustandsraum minimieren__:
	* Problem: Ggf. lernt Agent nur Labyrinth auswendig, wollen wir nicht.	
	* Also: Shortest-path Algo für Wegfindung zu Grunde legen, dann in Zustandsmodellierung an Pacman nur günstigsten nächsten Schritt mitgeben (4 Ausprägungen -> north, west, south, east) => Zustandsraum deutlich eingeschränkt	
	* Zu Geistern: Ob Geist im Weg und wie damit umgegangen ähnlich mitgegeben, wie nächster günstigster Schritt
		* Ausweichen (wenn Geist direkt neben Pacman => Ausweichen)
		* Fressen (Geister brauchen Zustände, ob fressbar oder nicht! Initial alle Geister auf fressbar setzen, wenn großes Pellet gefressen, wenn Geist das erste Mal gefressen wurde, wird er wieder nicht-fressbar)