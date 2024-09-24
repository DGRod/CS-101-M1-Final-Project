# Python Text Battleship

## Background

- For my Computer Science 101 Module 1 Final Project, I decided to create a text-based Battleship game in Python. I felt that this project would be a good test of my ability to work with back-end logic, Object Oriented Programming, and user interface and display.

- This project turned out to be more difficult than I expected, but with enough classes and objects I was able to implement every feature that I wanted the program to have. I designed this program to be modular, making it as easy as possible to add new features, such as more ships, alternate rules, or more difficult enemy AI's.

## Python Code

### Modules

- This program imports the random and time modules

### Classes

- The Point class contains the position, value, and other data associated with each point in a ship or grid. The .slicer() method returns a list of all Point objects in a line between the Point it is called on and the Point given as its argument. The .neighbors() method is responsible for identifying the four Point objects that border this Point.

- The Ship class contains a list of Point objects that represents the space on a grid occupied by a ship. It also contains a list of all possible positions on a grid that the ship could occupy. Lastly, it includes statistics associated with that ship, such as length and health. 

- The Grid class contains 10 lists of Point objects that form the 10 rows in the grid. It also contains a list of Ship objects that have been placed on the grid. The method .print_grid() is responsible for printing the Grid object to the terminal with the most recent information. The .place_ship() method is responsible for assigning each ship a position on the grid, depending on whether the user would like to place their ships manually, choose from the presets, or have their ships placed randomly. 

- The Player class contains a grid that belongs to the player, an enemy grid to target, a list of all the player's ships, and a list of all points that have been succesfully hit so far. The .search() method is responsible for identifying the nearest border or previously hit point on all sides of any given point, useful for calculating the probablity of the point containing a ship. The .ai() method is responsible for determining which point on the enemy grid to target based on previous hits, the current state of the enemy grid, and the difficulty selected by the player. (Could easily be adapted to provide the player with suggestions of where to fire.) For example, the Hard difficulty calculates the probablity of each point having a ship on it, and fires randomly at the most probable points that lie on the currently selected "firing solution" until it hits a ship. Subsequently, it will fire randomly at the hit point's neighbors until it hits the ship again. Then, it will fire at all points in the line formed by those two points until it misses on both ends, confirming destruction of the ship. The .fire() method uses either the player input or the .ai() method output to target a Point on the enemy grid and update its status.

### User Interface

- The title screen consists of a small ASCII logo and the initial user prompt to begin the game or read the manual. After asking for the user's name, it will ask the player how they would like to place their ships: manually, randomly, or with a preset.

- Next, the user will be prompted to choose what difficulty enemy they would like to play against.

- The game will now begin and continue until all of one of the player's ships are sunk or the user enters "clear" or "exit". Depending on which player's ships were sunk, the game will print a victory or defeat message to the user.

- All prompts for user input will return feedback if the player's input is unclear or a mistake. This prevents the program from breaking if the player makes a typo or other error and gives them another chance to input their choice.

## Future Improvements

- If possible, I would like to add many more features to this program. For example, it would be relatively simple to add more difficult enemy AI's to the game for a greater challenge. Alternatively, the game could be shortened by incorporating the rules from the "Salvo" variant of Battleship. Another possible improvement is the simple addition of more presets to choose from before the game begins.
