# Pacman_Reinforcement

Implementing an agent for Pacman, trained by reinforcement learning


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


### Implementation details

* Positions are represented by (x,y) Cartesian coordinates and any arrays are indexed by [x][y] 
* Actions available for agent: `north`, `west`, `south`, `east` and `stop`


### Open tasks and bugs

*