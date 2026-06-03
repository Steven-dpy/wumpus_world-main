
"""
Author: Dr Zhibin Liao
Organisation: School of Computer Science and Information Technology, Adelaide University
Date: 26-Apr-2026
Description: This Python script shows the basic agent template. MyAgent should be extending this Agent class.
Do not change this file, your version of this file won't be used in Gradescope Autographing.

The script is a part of Assignment 3 made for the course ARTI 2003 Artificial Intelligence for the year
of 2026. Public distribution of this source code is strictly forbidden.
"""

from definitions import ACTIONS, SENSE_NAMES


class Agent:
    """Template Wumpus agent.

    This class keeps the emulator-facing state deliberately small. Use it as a
    starting point for an intelligent agent by storing any internal map, rule
    base, or plan you need in reset(), updating it from senses in update(), and
    choosing the next action in act().
    """
    #Define the direction sequence
    DIRECTIONS = ['N', 'E', 'S', 'W']
    VECTORS = {'N':(1, 0), 'E':(0, 1), 'S':(-1, 0), 'W':(0, -1)}

    def __init__(self):
        """Create a fresh agent and initialise its state."""
        self.last_senses = None
        self.last_action = None
        self.reset()

    #At the beginning of the game, the function "reset()" will reinitialize the state.
    def reset(self):
        #The player starts at (0, 0) and faces east
        self.start = (0,0)
        self.position = (0,0)
        self.facing = 'E'
        self.forward_vector = None

        self.plan = [] #The currently planned list of actions
        self.has_gold = False #Indicating whether gold has been obtained
        self.arrwo_available = True
        self.wumpus_dead = False
        #Indicates whether the arrow is still usable and whether Wumpus has died

        self.visited = set() #The visited grids.
        self.safe = {(0,0)} #The grids that have been determined to be safe. The starting point is considered safe by default.
        self.walls = set()  #Record the position of the wall after hitting it.
        self.no_pit = {(0,0)} 
        self.no_wumpus = {(0,0)} #Indicate the grids where it is definitely confirmed that there are no holes and no Wumpus.
        self.breeze_cells = set()
        self.stench_cells = set() #Separately mark the grids for "breeze" and "stench".
        self.senses_at = {}
        
        """Reset all state before a new cave starts."""
        self.last_senses = None
        self.last_action = None



    def update(self, senses):
        if self.last_action == "FORWARD": #Update the position when moving forward.
            next_cell = self._add(self.position, self.forward_vector) #Calculate the coordinates of the adjacent grid.
            if senses["Bump"]: #Determine whether there was a collision with a wall
                self.walls.add(next_cell) #The square ahead is a wall. Add it to the "walls" collection.
                self.safe.discard(next_cell)
                self.no_pit.discard(next_cell)
                self.no_wumpus.discard(next_cell)
                #Remove from the safe squares, the hole-free squares, and the Wumpus-free squares.
            else:
                self.position = next_cell #Update current location
                self.safe.add(self.position) #Mark the current position as safe
                self.no_pit.add(self.position)
                self.no_wumpus.add(self.position)
                #Mark the current position as free of holes and free of Wumpus.

        """Receive the latest percept values keyed by sense name."""
        missing = [name for name in SENSE_NAMES if name not in senses]
        if missing:
            raise ValueError(f"Missing sense values: {', '.join(missing)}")
        self.last_senses = {name: bool(senses[name]) for name in SENSE_NAMES}

    def act(self):
        """Return the next action string.

        The base agent is passive so it can be loaded safely in the emulator.
        Assignment agents should override this method and return one of:
        FORWARD, LEFT, RIGHT, GRAB, SHOOT, EXIT, NO_ACTION.
        If no action is given for any reason (say you are changing an internal state),
        the NO_ACTION action should be returned instead.
        """
        return 'NO_ACTION'

    def remember_action(self, action):
        """Store and validate an action before returning it from a subclass."""
        if action is not None and action not in ACTIONS:
            raise ValueError(f"Unknown action: {action}")
        self.last_action = action
        return action
