import random
import time

# X & Y Axes for the board
numbers = [str(x) for x in range(0, 10)]
abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


class Point:

    def __init__(self, xcoord, ycoord):
        # Positional Data
        self.xcoord = str(xcoord)
        self.ycoord = str(ycoord)
        self.position = self.xcoord + self.ycoord
        # Display Data
        self.value = "-"
        self.is_ship = False
        self.probability = 0
        
    def __repr__(self):
        return self.position

    def slicer(self, other_point):
        # Returns the set of points between this point and the point passed in as an argument
        if self.xcoord == other_point.xcoord: # If the points are vertically aligned:
            sliced_numbers = numbers[int(self.ycoord):int(other_point.ycoord) + 1]
            result = []
            for number in sliced_numbers:
                result.append(self.xcoord + number)
            return result
        if self.ycoord == other_point.ycoord: # If the points are horizontally aligned:
            sliced_letters = abc[abc.index(self.xcoord):abc.index(other_point.xcoord) + 1]
            result = []
            for letter in sliced_letters:
                result.append(letter + self.ycoord)
            return result
    
    def neighbors(self):
        # Returns list of 2-4 adjacent points
        neighbors = []
        # Handling of edge cases (in case point is located on the borders):
        if self.ycoord != "9": # Excludes points on the lower edge
            neighbors.append(self.xcoord + numbers[numbers.index(self.ycoord) + 1])

        if self.ycoord != "0": # Excludes points on the top edge
            neighbors.append(self.xcoord + numbers[numbers.index(self.ycoord) - 1])
        
        if self.xcoord != "J": # Excludes points on the right edge
            neighbors.append(abc[abc.index(self.xcoord) + 1] + self.ycoord) 
        
        if self.xcoord != "A": # Excludes points on the left edge
            neighbors.append(abc[abc.index(self.xcoord) - 1] + self.ycoord)
        
        return neighbors

    def hit(self):
        # Changes display value to red 'X' to mark a hit
        self.value = '\033[1;31m' + "X" + '\033[0m'
    
    def miss(self):
        # Changes display value to 'O' to mark a miss
        self.value = "O"
    
    def make_ship(self, new_value):
        # Changes display value to mark point as a ship
        self.value = new_value
        self.is_ship = True


class Ship:

    def __init__(self, name, team, health):
        self.name = name
        self.team = team
        self.sunk = False
        self.length = health
        self.health = health
        self.position = []
        # Creates a Dictionary mapping the name of each point to a Point object
        self.all_points = []
        for letter in abc:
            for number in range(0,10):
                self.all_points.append(letter + str(number))
        self.all_points_dict = {point:Point(point[0], point[-1]) for point in self.all_points}
        # Determines the set of all possible positions for a ship of certain length
        self.all_positions = []
        for letter in abc:
            for x in range(0, 11 - self.length):
                self.all_positions.append(self.all_points_dict[(letter + str(x))].slicer(self.all_points_dict[(letter + str(x + self.length - 1))]))
        for number in numbers:
            for x in range(0, 11 - self.length):
                self.all_positions.append(self.all_points_dict[abc[x] + number].slicer(self.all_points_dict[(abc[x + self.length - 1] + number)]))
                
    def __repr__(self):
        return self.name + " has " + str(self.health) + " health."

    def damage(self):
        self.health += -1 
    
    def sink(self):
        # Set the ship's status to 'sunk' when it reaches 0 health
        if self.health == 0:
            self.sunk = True
            if self.team == "Enemy":
                return print("You sunk the enemy " + self.name + "!")
            else:
                return print("Your " + self.name + " has been sunk!")


class Grid:

    def __init__(self, name):
        self.name = name
        self.all_ships = []
        self.total_health = 0
        # Set of points in the center of the grid
        self.center_points = ["D3", "D4", "D5", "D6", "E3", "E4", "E5", "E6", "F3", "F4", "F5", "F6", "G3", "G4", "G5", "G6"]
        # Placeholders for lists of all occupied points and invalid ship positions
        self.taken_points = []
        self.bad_positions = []
        
        #Defines a 2D array to store all points on the grid:
        row0 = [x + "0" for x in abc]
        row1 = [x + "1" for x in abc]
        row2 = [x + "2" for x in abc]
        row3 = [x + "3" for x in abc]
        row4 = [x + "4" for x in abc]
        row5 = [x + "5" for x in abc]
        row6 = [x + "6" for x in abc]
        row7 = [x + "7" for x in abc]
        row8 = [x + "8" for x in abc]
        row9 = [x + "9" for x in abc]
        self.rows = [row0, row1, row2, row3, row4, row5, row6, row7, row8, row9]
        # Defines a Dictionary mapping the name of each point to a Point object
        self.points_list = []
        for row in self.rows:
            for point in row:
                self.points_list.append(point)
        self.points_dict = {point:Point(point[0], point[-1]) for point in self.points_list}
        # Defines the set of all possible positions for every possible ship size
        self.all_positions_on_grid = []
        for letter in abc:
            for possible_length in range(2,6):
                for x in range(0, 11 - possible_length):
                    self.all_positions_on_grid.append(self.points_dict[(letter + str(x))].slicer(self.points_dict[(letter + str(x + possible_length - 1))]))
        for number in numbers:
            for possible_length in range(2,6):
                for x in range(0, 11 - possible_length):
                    self.all_positions_on_grid.append(self.points_dict[abc[x] + number].slicer(self.points_dict[(abc[x + possible_length - 1] + number)]))
        
        '''for position in self.all_positions_on_grid:
            while self.all_positions_on_grid.count(position) > 1:
                self.all_positions_on_grid.remove(position)'''
    
    def __repr__(self):
        print(self.name)
 
    def place_ship(self, ship, condition):
        # Defines a list of all currently available possible ship positions
        available_ship_positions = []
        for position in ship.all_positions:
            if position in self.all_positions_on_grid:
                available_ship_positions.append(position)
        # If the player chooses to place his ships manually:
        if condition == "Manual":
            while True: # Repeat until the player enters a valid position for the ship:
                player_choice = ("\nWhere would you like to place your " + ship.name + "? (Length: " + str(ship.length) + 
                        ")\nPlease type the first and last coordinates (separated by a comma) of the position where you would like to place it." + 
                        "\n    (For example, type \'A0, A" + str((ship.length)-1) + "\' to place your " + ship.name + 
                        " on the points between A0 and A" + str((ship.length)-1) + ".)\n").upper()
                processed_input = sorted((player_choice.replace(" ", "")).split(","))
                possible_position = (self.points_dict[((processed_input)[0])]).slicer(self.points_dict[((processed_input)[-1])])
                # Check if the player's selected position is valid:
                if len(possible_position) == ship.length and possible_position not in self.bad_positions:
                    # Assign ship to position
                    ship.position = possible_position
                    break
        # If the player chooses to arrange his ships randomly:
        if condition == "Random":
            ship.position = random.choice(available_ship_positions)
        # If start & end points are provided (from a preset):
        if type(condition) == list:
            point_a = self.points_dict[condition[0]]
            point_b = self.points_dict[condition[-1]]
            preset_position = point_a.slicer(point_b)
            ship.position = preset_position

        # Determines how to display the ship
        for point in ship.position:
            if ship.team == "Player":
                self.points_dict[point].make_ship(ship.name[0])
            if ship.team == "Enemy":
                self.points_dict[point].make_ship("-")
            # Add all of the ship's points to the list of occupied points
            self.taken_points.append(point)
        # Determine all invalid ship positions based on the list of occupied points
        for point in self.taken_points:
            for position in self.all_positions_on_grid:
                if point in position:
                    self.bad_positions.append(position)
        # Removes duplicates from the list of invalid ship positions
        for position in self.bad_positions:
            if self.bad_positions.count(position) > 1:
                while self.bad_positions.count(position) > 1:
                    self.bad_positions.remove(position)
        # Removes invalid ship positions from the list of all possible positions for all ships
        for position in self.bad_positions:
            if position in self.all_positions_on_grid:
                self.all_positions_on_grid.remove(position)
        # Adds ship and its health points to the grid
        self.all_ships.append(ship)
        self.total_health += ship.health

    def print_grid(self):
        print(self.name) # Displays the Grid to the player
        print("  A B C D E F G H I J")
        for row in self.rows:
            num = row[0][-1]
            symbolA = (self.points_dict[row[0]]).value
            symbolB = (self.points_dict[row[1]]).value
            symbolC = (self.points_dict[row[2]]).value
            symbolD = (self.points_dict[row[3]]).value
            symbolE = (self.points_dict[row[4]]).value
            symbolF = (self.points_dict[row[5]]).value
            symbolG = (self.points_dict[row[6]]).value
            symbolH = (self.points_dict[row[7]]).value
            symbolI = (self.points_dict[row[8]]).value
            symbolJ = (self.points_dict[row[9]]).value
            print("{} {} {} {} {} {} {} {} {} {} {}".format(num, symbolA, symbolB, symbolC, symbolD, symbolE, symbolF, symbolG, symbolH, symbolI, symbolJ))

    def reveal_ships(self): # Reveals the location of all ships on the Grid
        for ship in self.all_ships:
            for point in ship.position:
                self.points_dict[point].value = '#'


class Player:

    def __init__(self, team, name, grid, enemy_grid):
        # Classifies the player as the User or AI
        self.team = team
        self.name = name
        # Assigns a Grid w/ Ships to the player
        self.grid = grid
        self.ships = self.grid.all_ships
        # Assigns the enemy's Grid to the player
        self.enemy_grid = enemy_grid
        self.target_points = self.enemy_grid.points_list
        # Placeholders for the most recent hit and list of all successful hits
        self.hit_point = "  "
        self.hit_list = []
        # Placeholder for list of ai targets
        self.most_probable_points = []
        # Turn Counter
        self.counter = 1
        # Set of all possible enemy ship positions
        self.all_enemy_positions = []
        for letter in abc:
            for possible_length in range(2,6):
                for x in range(0, 11 - possible_length):
                    self.all_enemy_positions.append(self.enemy_grid.points_dict[(letter + str(x))].slicer(self.enemy_grid.points_dict[(letter + str(x + possible_length - 1))]))
        for number in numbers:
            for possible_length in range(2,6):
                for x in range(0, 11 - possible_length):
                    self.all_enemy_positions.append(self.enemy_grid.points_dict[abc[x] + number].slicer(self.enemy_grid.points_dict[(abc[x + possible_length - 1] + number)]))
        
        '''for position in self.all_enemy_positions:
            while self.all_enemy_positions.count(position) > 1:
                self.all_enemy_positions.remove(position)'''
        # 'Firing solution' consisting of specific points on the grid
        self.firing_solution_z2 = []
        for number in numbers:
            if int(number) % 2 == 0:
                for letter in ["A", "C", "E", "G", "I"]:
                    self.firing_solution_z2.append(letter + str(number))
            else:
                for letter in ["B", "D", "F", "H", "J"]:
                    self.firing_solution_z2.append(letter + str(number))

    def search(self, target): # Determines the nearest border or previously-targeted point on every side
        # Grab the Point object corresponding to the provided target
        target = self.enemy_grid.points_dict[target]
        # Sets of all vertical and horizontal border Points
        vert_borders = []
        horz_borders = []
        for point in self.enemy_grid.points_list:
            if point[0] == "A" or point[0] == "J":
                vert_borders.append(point)
            if point[1] == "0" or point[1] == "9":
                horz_borders.append(point)
        vert_border_points = [self.enemy_grid.points_dict[item] for item in vert_borders]
        horz_border_points = [self.enemy_grid.points_dict[item] for item in horz_borders]
        # Set default values
        left = target
        right = target
        up = target
        down = target
        # If there is space to the left of the target:
        if target.xcoord != "A":
            var = 1 # Count how many empty spaces until the nearest border or previously-target point:
            left = self.enemy_grid.points_dict[abc[abc.index(target.xcoord) - var] + target.ycoord]
            while left.value != '\033[1;31m' + "X" + '\033[0m' and left.value != "O" and left not in vert_border_points:
                var += 1
                left = self.enemy_grid.points_dict[abc[abc.index(target.xcoord) - var] + target.ycoord]
            if left.value == '\033[1;31m' + "X" + '\033[0m' or left.value == "O":
                left = self.enemy_grid.points_dict[abc[abc.index(target.xcoord) - var + 1] + target.ycoord]
        # If there is space to the right of the target:
        if target.xcoord != "J":
            var = 1 # Count how many empty spaces until the nearest border or previously-target point:
            right = self.enemy_grid.points_dict[abc[abc.index(target.xcoord) + var] + target.ycoord]
            while right.value != '\033[1;31m' + "X" + '\033[0m' and right.value != "O" and right not in vert_border_points:
                var += 1
                right = self.enemy_grid.points_dict[abc[abc.index(target.xcoord) + var] + target.ycoord]
            if right.value == '\033[1;31m' + "X" + '\033[0m' or right.value == "O":
                right = self.enemy_grid.points_dict[abc[abc.index(target.xcoord) + var - 1] + target.ycoord]
        # If there is space above the target:
        if target.ycoord != "0":
            var = 1 # Count how many empty spaces until the nearest border or previously-target point:
            up = self.enemy_grid.points_dict[target.xcoord + numbers[numbers.index(target.ycoord) - var]]
            while up.value != '\033[1;31m' + '\033[1;31m' + "X" + '\033[0m' + '\033[0m' and up.value != "O" and up not in horz_border_points:
                var += 1
                up = self.enemy_grid.points_dict[target.xcoord + numbers[numbers.index(target.ycoord) - var]]
            if up.value == '\033[1;31m' + "X" + '\033[0m' or up.value == "O":
                up = self.enemy_grid.points_dict[target.xcoord + numbers[numbers.index(target.ycoord) - var + 1]]
        # If there is space below the target:
        if target.ycoord != "9":
            var = 1 # Count how many empty spaces until the nearest border or previously-target point:
            down = self.enemy_grid.points_dict[target.xcoord + numbers[numbers.index(target.ycoord) + var]]
            while down.value != '\033[1;31m' + "X" + '\033[0m' and down.value != "O" and down not in horz_border_points:
                var += 1
                down = self.enemy_grid.points_dict[target.xcoord + numbers[numbers.index(target.ycoord) + var]]
            if down.value == '\033[1;31m' + "X" + '\033[0m' or down.value == "O":
                down = self.enemy_grid.points_dict[target.xcoord + numbers[numbers.index(target.ycoord) + var - 1]]
        # Return a list of the nearest borders or previously-targeted points in each direction
        return [left, right, up, down]

    def ai(self, difficulty=1): # Determines which point to target next, default difficulty setting = 1
        # Set of all available points within the 'firing solution'
        firing_solution_z2_clean = []
        for point in self.firing_solution_z2:     
            if point in self.target_points:
                firing_solution_z2_clean.append(point)
        # Set of all available points in the center of the grid
        clean_center_points = []
        for point in self.enemy_grid.center_points:
            if point in self.target_points:
                clean_center_points.append(point)
        # Set of all points that are at least one space away from 
        # the nearest previously-targeted point or border in any direction
        more_than_one_away = []
        for point in self.target_points:
            nearest_points = self.search(point)
            left_space = nearest_points[0].slicer(self.enemy_grid.points_dict[point])
            right_space = self.enemy_grid.points_dict[point].slicer(nearest_points[1])
            up_space = nearest_points[2].slicer(self.enemy_grid.points_dict[point])
            down_space = self.enemy_grid.points_dict[point].slicer(nearest_points[3])
            if len(left_space) >= 2 and len(right_space) >= 2 and len(up_space) >= 2 and len(down_space) >= 2:
                more_than_one_away.append(point)

        #=================================================================================================================================
        # 4th-priority choice: Probable Points 
        #=================================================================================================================================
        # Set of target points with the highest probability of containing a Ship
        probable_target_points = []
        # Calculate each point's probability of containing a Ship
        for point in self.target_points:
            # Search nearby area for borders or previously-target points
            left, right, up, down = self.search(point)
            print(left, right, up, down)
            # Measure the distance between these points
            horz_slice = left.slicer(right)
            vert_slice = up.slicer(down)
            # Default probability of 0
            point_probability = 0
            # Increment the probability based on the number of ships that could fit over the point
            # Horizontally:
            if len(horz_slice) >= 5:
                point_probability += 1
            if len(horz_slice) >= 4:
                point_probability += 1
            if len(horz_slice) >= 3:
                point_probability += 2
            if len(horz_slice) >= 2:
                point_probability += 1
            # Vertically:
            if len(vert_slice) >= 5:
                point_probability += 1
            if len(vert_slice) >= 4:
                point_probability += 1
            if len(vert_slice) >= 3:
                point_probability += 2
            if len(vert_slice) >= 2:
                point_probability += 1
            # Assign the calculated probability to the Point.probability attribute
            self.enemy_grid.points_dict[point].probability = point_probability
        # Create probability Dictionary
        proto_dict = {}
        for (key, value) in self.enemy_grid.points_dict.items():
            if key in self.target_points:
                proto_dict[key] = value
        prob_dict = {point.position:point.probability for point in proto_dict.values()}
        # Find the point with the highest probability
        max_prob = max(prob_dict.values())
        # Set of all points with the highest-calculated probability
        probable_points = []
        for point in prob_dict.keys():
            if prob_dict[point] == max_prob:
                probable_points.append(point)
        # Check if each point is an available target
        for point in probable_points:
            if point in self.target_points:
                probable_target_points.append(point)
        # Check if each point is in the 'firing solution'
        probable_firing_solution_points = []
        for point in probable_target_points:
            if point in firing_solution_z2_clean:
                probable_firing_solution_points.append(point)

        #=================================================================================================================================
        #3rd-priority choice: Hit Neighbors
        #=================================================================================================================================
        # Set of all adjacent points to a previously-hit point
        clean_hit_neighbors = []
        # If a point has been successfully hit:
        if self.hit_point != "  ":
            # Find the adjacent points
            hit_neighbors = self.enemy_grid.points_dict[self.hit_point].neighbors()
            for point in hit_neighbors:
                # Check if adjacent points are available targets
                if point in self.target_points:
                    clean_hit_neighbors.append(point)

        #=================================================================================================================================
        #2nd-priority choice: Likely Points
        #=================================================================================================================================
        # Set of all points collinear with previously hit points
        likely_points = []
        clean_likely_points = []
        # If the previously-targeted point was a successful hit:
        if self.hit_point != "  ":
            # If multiple points have been successfully hit:
            if len(self.hit_list) >= 2:
                for point in self.hit_list:
                    other_points = []
                    for pt in self.hit_list:
                        if pt != point:
                            other_points.append(pt)
                    for other_point in other_points:
                        # Identify if previously hit points are adjacent to each other
                        if other_point in self.enemy_grid.points_dict[point].neighbors():
                            # If points share x coord:
                            if point[0] == other_point[0]:
                                # If point is above other_point:
                                if point[1] < other_point[1]:
                                    # Add collinear points to likely_points
                                    if point[1] != "0":
                                        likely_points.append(point[0] + str(int(point[1]) - 1))
                                    if other_point[1] != "9":
                                        likely_points.append(other_point[0] + str(int(other_point[1]) + 1))
                                # If point is below other_point:
                                if point[1] > other_point[1]:
                                    # Add collinear points to likely_points
                                    if point[1] != "9":
                                        likely_points.append(point[0] + str(int(point[1]) + 1))
                                    if other_point[1] != "0":
                                        likely_points.append(other_point[0] + str(int(other_point[1]) - 1))
                            # If points share y coord:
                            if point[1] == other_point[1]:
                                # If point is to the left of other_point:
                                if abc.index(point[0]) < abc.index(other_point[0]):
                                    # Add collinear points to likely_points
                                    if abc.index(point[0]) != 0:
                                        likely_points.append(abc[abc.index(point[0]) - 1] + point[1])
                                    if abc.index(other_point[0]) != 9:
                                        likely_points.append(abc[abc.index(other_point[0]) + 1] + other_point[1])
                                # If point is to the right of other_point:
                                if abc.index(point[0]) > abc.index(other_point[0]):
                                    # Add collinear points to likely_points
                                    if abc.index(point[0]) != 9:
                                        likely_points.append(abc[abc.index(point[0]) + 1] + point[1])
                                    if abc.index(other_point[0]) != 0:
                                        likely_points.append(abc[abc.index(other_point[0]) - 1] + other_point[1])
            # Remove unavailable targets from likely_points
            for point in likely_points:
                if point in self.target_points:
                    clean_likely_points.append(point)
            # Remove duplicate points from likely_points
            for point in clean_likely_points:
                if clean_likely_points.count(point) > 1:
                    while clean_likely_points.count(point) > 1:
                        clean_likely_points.remove(point)

        #=================================================================================================================================
        #1st choice: Probable and Likely Points
        #=================================================================================================================================
        # Set of all points that belong to both probable_points AND likely_points
        probable_and_likely_points = []

        for point in clean_likely_points:
            if point in probable_target_points:
                probable_and_likely_points.append(point)
        
        # Set of all available points in the center of the grid
        center_firing_solution = []
        for point in clean_center_points:
            if point in more_than_one_away:
                center_firing_solution.append(point)
        # Set of all available probable points in the center of the grid
        probable_center_firing_solution = []
        for point in center_firing_solution:
            if point in probable_points:
                probable_center_firing_solution.append(point)
        # Set of all available probable points that are more than one space away
        # from the nearest previously-targeted point or border
        probable_more_than_one_away = []
        for point in more_than_one_away:
            if point in probable_points:
                probable_more_than_one_away.append(point)

        # Extra Hard AI difficulty (still in development)
        if difficulty >= 4:
            # For the first turn, 4th-priority targets are the center of the grid
            if self.counter == 1:
                priority_4 = clean_center_points
            # For turns 2-8, 4th-priority targets are probable points in the 'firing solution'
            if self.counter > 1 and self.counter <= 8:
                priority_4 = probable_center_firing_solution
            # After turn 8, 4th-priority targets are probable points from more_than_one_away
            if self.counter > 8:
                priority_4 = probable_more_than_one_away
            # If there are any 1st-priority targets, choose one at random
            if len(probable_and_likely_points) > 0:
                target = random.choice(probable_and_likely_points)
            # If there are any 2nd-priority targets, choose one at random
            elif len(clean_likely_points) > 0:
                target = random.choice(clean_likely_points)
            # If there are any 3rd-priority targets, choose one at random
            elif len(clean_hit_neighbors) > 0:
                target = random.choice(clean_hit_neighbors)
            # If there are any 4th-priority targets, choose one at random
            elif len(priority_4) > 0:
                target = random.choice(priority_4)
            # If there are any 5th-priority targets, choose one at random
            elif len(more_than_one_away) > 0:
                target = random.choice(more_than_one_away)
            # If there are any 6th-priority targets, choose one at random
            elif len(probable_firing_solution_points) > 0:
                target = random.choice(probable_firing_solution_points)
            # If there are any 7th-priority targets, choose one at random
            elif len(firing_solution_z2_clean) > 0:
                target = random.choice(firing_solution_z2_clean)
            # Otherwise, target a random point
            else:
                target = random.choice(self.target_points)
        
        # Hard AI Difficulty
        elif difficulty >= 3:
            # If there are any 1st-priority targets, choose one at random
            if len(probable_and_likely_points) > 0:
                target = random.choice(probable_and_likely_points)
            # If there are any 2nd-priority targets, choose one at random
            elif len(clean_likely_points) > 0:
                target = random.choice(clean_likely_points)
            # If there are any 3rd-priority targets, choose one at random
            elif len(clean_hit_neighbors) > 0:
                target = random.choice(clean_hit_neighbors)
            # If there are any 6th-priority targets, choose one at random
            elif len(probable_firing_solution_points) > 0:
                target = random.choice(probable_firing_solution_points)
            # If there are any 7th-priority targets, choose one at random
            elif len(firing_solution_z2_clean) > 0:
                target = random.choice(firing_solution_z2_clean)
            # Otherwise, target a random point
            else:
                target = random.choice(self.target_points)

        # Medium AI Difficulty
        elif difficulty >= 2:
            # If there are any 2nd-priority points, choose one at random
            if len(clean_likely_points) > 0:
                target = random.choice(clean_likely_points)
            # If there are any 3rd-priority points, choose one at random
            elif len(clean_hit_neighbors) > 0:
                target = random.choice(clean_hit_neighbors)
            # Otherwise, target a random point
            else:
                target = random.choice(self.target_points)
        
        # Easy AI Difficulty
        elif difficulty >= 1:
            # If there are any 3rd-priority targets, choose one at random
            if len(clean_hit_neighbors) > 0:
                target = random.choice(clean_hit_neighbors)
            # Otherwise, target a random point
            else:
                target = random.choice(self.target_points)

        return target

    # Update the board when a target is chosen
    def fire(self, target):
        print("Turn #" + str(self.counter))
        # Identify if the shot was fired by the user or the computer
        if self.name == player_one_name:
            print("Firing at " + target)
        else:
            print("Enemy firing at " + target)
        # Update the list of available target points
        self.counter += 1
        self.target_points.remove(target)
        # If the target is successfully hit:
        if self.enemy_grid.points_dict[target].is_ship == True:
            print( '\033[1;31m' + "////////////HIT!////////////" + '\033[0m')
            self.hit_point = target
            self.hit_list.append(target)
            self.enemy_grid.points_dict[target].hit()
            # Reduce Ship health
            for ship in self.enemy_grid.all_ships:
                if target in ship.position:
                    ship.damage()
                    self.enemy_grid.total_health += -1
                    if ship.health == 0:
                        ship.sink()
                        if ai_difficulty == 4:
                            self.hit_point = "  "
            # Refresh the Grid
            self.enemy_grid.print_grid()
        # If the target is a miss:
        else:
            print("Miss!")
            # Refresh the Grid
            self.enemy_grid.points_dict[target].miss()
            self.enemy_grid.print_grid()


#/////////////////////////
#       PRESETS
#/////////////////////////

preset1 = Grid("Your Grid:")
preset1_placements = [["D7", "H7"], ["G1", "G4"], ["B2", "B4"], ["C9", "E9"], ["J0", "J1"]]
preset1.place_ship(Ship("Aircraft Carrier", "Player", 5), preset1_placements[0])
preset1.place_ship(Ship("Battleship", "Player", 4), preset1_placements[1])
preset1.place_ship(Ship("Destroyer", "Player", 3), preset1_placements[2])
preset1.place_ship(Ship("Submarine", "Player", 3), preset1_placements[3])
preset1.place_ship(Ship("Patrol Boat", "Player", 2), preset1_placements[4])

preset2 = Grid("Your Grid:")
preset2_placements = [["I3", "I7"], ["A5", "A8"], ["F7", "F9"], ["B0", "D0"], ["C2", "C3"]]
preset2.place_ship(Ship("Aircraft Carrier", "Player", 5), preset2_placements[0])
preset2.place_ship(Ship("Battleship", "Player", 4), preset2_placements[1])
preset2.place_ship(Ship("Destroyer", "Player", 3), preset2_placements[2])
preset2.place_ship(Ship("Submarine", "Player", 3), preset2_placements[3])
preset2.place_ship(Ship("Patrol Boat", "Player", 2), preset2_placements[4])

preset3 = Grid("Your Grid:")
preset3_placements = [["F0", "F4"], ["B5", "B8"], ["H1", "H3"], ["E9", "G9"], ["A2", "B2"]]
preset3.place_ship(Ship("Aircraft Carrier", "Player", 5), preset3_placements[0])
preset3.place_ship(Ship("Battleship", "Player", 4), preset3_placements[1])
preset3.place_ship(Ship("Destroyer", "Player", 3), preset3_placements[2])
preset3.place_ship(Ship("Submarine", "Player", 3), preset3_placements[3])
preset3.place_ship(Ship("Patrol Boat", "Player", 2), preset3_placements[4])

preset4 = Grid("Your Grid:")
preset4_placements = [["E8", "I8"], ["G6", "J6"], ["A5", "C5"], ["C1", "C3"], ["G1", "H1"]]
preset4.place_ship(Ship("Aircraft Carrier", "Player", 5), preset4_placements[0])
preset4.place_ship(Ship("Battleship", "Player", 4), preset4_placements[1])
preset4.place_ship(Ship("Destroyer", "Player", 3), preset4_placements[2])
preset4.place_ship(Ship("Submarine", "Player", 3), preset4_placements[3])
preset4.place_ship(Ship("Patrol Boat", "Player", 2), preset4_placements[4])

preset5 = Grid("Your Grid:")
preset5_placements = [["J2", "J6"], ["I5", "I8"], ["C3", "C5"], ["A0", "A2"], ["C9", "D9"]]
preset5.place_ship(Ship("Aircraft Carrier", "Player", 5), preset5_placements[0])
preset5.place_ship(Ship("Battleship", "Player", 4), preset5_placements[1])
preset5.place_ship(Ship("Destroyer", "Player", 3), preset5_placements[2])
preset5.place_ship(Ship("Submarine", "Player", 3), preset5_placements[3])
preset5.place_ship(Ship("Patrol Boat", "Player", 2), preset5_placements[4])

all_preset_placements = [[], preset1_placements, preset2_placements, preset3_placements, preset4_placements, preset5_placements]


#/////////////////////////
#     PLAYER SETUP
#/////////////////////////
print('''
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

             BBBBBBBBBBB             AAA     TTTTTTTTTTTTTTT TTTTTTTTTTTTTTT  LLL           EEEEEEEEEEE      SSSSSSSS      HHH       HHH   IIIIIIIIIII   PPPPPPPPPP            
            BBB       BBB          AAAAA          TTT             TTT        LLL           EEE            SSS      SSS    HHH       HHH       III       PPP      PPP          
           BBB        BBB        AAA AAA         TTT             TTT        LLL           EEE            SSS             HHH       HHH       III       PPP       PPP         
          BBB       BBB        AAA   AAA        TTT             TTT        LLL           EEE             SSS            HHH       HHH       III       PPP      PPP
         BBBBBBBBBBB         AAA     AAA       TTT             TTT        LLL           EEEEEEEEEEE        SSSSS       HHHHHHHHHHHHH       III       PPPPPPPPPP
        BBB       BBB       AAAAAAAAAAA       TTT             TTT        LLL           EEE                     SSS    HHH       HHH       III       PPP
       BBB        BBB     AAA       AAA      TTT             TTT        LLL           EEE                      SSS   HHH       HHH       III       PPP
      BBB       BBB     AAA         AAA     TTT             TTT        LLL           EEE            SSS      SSS    HHH       HHH       III       PPP
     BBBBBBBBBBB      AAA           AAA    TTT             TTT        LLLLLLLLLLLL  EEEEEEEEEEEE     SSSSSSSS      HHH       HHH   IIIIIIIIIII   PPP

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////         
''')
time.sleep(3)
print("Welcome to Python Battleship!")
print("If you would like to read the manual, please type \'Help\'\n")
player_input = input("Press any key to continue...\n")
if player_input.title() == "Help":
    print('''\n
    To win the game, you must find and sink all 5 enemy ships before the computer finds and sinks all 5 of yours.
    On your turn, you simply need to choose a point on the grid to fire at. If there is a ship there, it will register as a \'Hit\'.
    Otherwise, it will register as a \'Miss\'.
    Try to arrange your ships in a pattern that will make it difficult for the computer to find them.
    
    Have fun!\n''')
    input("Press any key to continue...\n")
# Initialize the Grid
grid1 = Grid("Your Grid:")
player_one_name = input("Please enter player name: ")
# Determine how to arrange the player's Ships
choice = input("\n" + player_one_name + ", would you like to manually place your ships, choose from 10 preset options, or have them placed randomly?"
               + "\nPlease type \'Manual\', \'Preset\', or \'Random\'\n")

if choice.title() != "Manual" and choice.title() != "Preset" and choice.title() != "Random":
    while choice.title() != "Manual" and choice.title() != "Preset" and choice.title() != "Random":
        choice = input("Please type \'Manual\', \'Preset\', or \'Random\'\n")
        if choice.title() == "Manual" or choice.title() == "Preset" or choice.title() == "Random":
            break

# Ask the player to manually place each Ship:
if choice.title() == "Manual":
    grid1.print_grid()
    grid1.place_ship(Ship("Aircraft Carrier", "Player", 5), "Manual")
    print("\n")
    grid1.print_grid()
    grid1.place_ship(Ship("Battleship", "Player", 4), "Manual")
    print("\n")
    grid1.print_grid()
    grid1.place_ship(Ship("Destroyer", "Player", 3), "Manual")
    print("\n")
    grid1.print_grid()
    grid1.place_ship(Ship("Submarine", "Player", 3), "Manual")
    print("\n")
    grid1.print_grid()
    grid1.place_ship(Ship("Patrol Boat", "Player", 2), "Manual") 
    
# Randomly place each Ship:
if choice.title() == "Random":
    grid1.place_ship(Ship("Aircraft Carrier", "Player", 5), "Random")
    grid1.place_ship(Ship("Battleship", "Player", 4), "Random")
    grid1.place_ship(Ship("Destroyer", "Player", 3), "Random")
    grid1.place_ship(Ship("Submarine", "Player", 3), "Random")
    grid1.place_ship(Ship("Patrol Boat", "Player", 2), "Random")
    
# Ask the player to select a preset:
if choice.title() == "Preset":
    print("Here are some preset ship layout options. To select one, just type its number.")
    print("\n   ///Preset (1)///")
    preset1.print_grid()
    time.sleep(2)
    print("\n   ///Preset (2)///")
    preset2.print_grid()
    time.sleep(2)
    print("\n   ///Preset (3)///")
    preset3.print_grid()
    time.sleep(2)
    print("\n   ///Preset (4)///")
    preset4.print_grid()
    time.sleep(2)
    print("\n   ///Preset (5)///")
    preset5.print_grid()
    
    player_preset_choice = input("\nWhich preset would you like to use?\n")

    while True:
        player_preset_choice_number = int(player_preset_choice)
        while int(player_preset_choice) <= 0 or int(player_preset_choice) > (len(all_preset_placements) - 1):
            player_preset_choice = input("Please type the number of the preset you would like to use.\n")
            continue
        break

    chosen_preset_placements = all_preset_placements[player_preset_choice_number]

    print("\nPreset " + str(player_preset_choice_number) + " selected.\n")
    # Place Ships according to selected preset
    grid1.place_ship(Ship("Aircraft Carrier", "Player", 5), chosen_preset_placements[0])
    grid1.place_ship(Ship("Battleship", "Player", 4), chosen_preset_placements[1])
    grid1.place_ship(Ship("Destroyer", "Player", 3), chosen_preset_placements[2])
    grid1.place_ship(Ship("Submarine", "Player", 3), chosen_preset_placements[3])
    grid1.place_ship(Ship("Patrol Boat", "Player", 2), chosen_preset_placements[4])
    

# Initialize the Computer's Grid
grid2 = Grid("Enemy Grid:")

grid2.place_ship(Ship("Aircraft Carrier", "Enemy", 5), "Random")
grid2.place_ship(Ship("Battleship", "Enemy", 4), "Random")
grid2.place_ship(Ship("Destroyer", "Enemy", 3), "Random")
grid2.place_ship(Ship("Submarine", "Enemy", 3), "Random")
grid2.place_ship(Ship("Patrol Boat", "Enemy", 2), "Random")


# Initialize the players
Player1 = Player("Player", player_one_name, grid1, grid2)
Player2 = Player("Enemy", "Computer", grid2, grid1)

# Load the player's Grid
grid1.print_grid()

# Ask the player to select the difficulty of the enemy AI
player_difficulty_selection = input("\nWhat difficulty AI would you like to play against? Please type \'Easy\', \'Medium\', \'Hard\', or \'Extra Hard\'\n")

while player_difficulty_selection.title() != "Easy" and player_difficulty_selection.title() != "Medium" and player_difficulty_selection.title() != "Hard" and player_difficulty_selection.title() != "Extra Hard":
    player_difficulty_selection = input("Please type \'Easy\', \'Medium\', \'Hard\', or \'Extra Hard\'\n")
    if player_difficulty_selection.title() == "Easy" or player_difficulty_selection.title() == "Medium" or player_difficulty_selection.title() == "Hard" or player_difficulty_selection.title() == "Extra Hard":
        break
# Set enemy AI difficulty:
if player_difficulty_selection.title() == "Easy":
    ai_difficulty = 1
if player_difficulty_selection.title() == "Medium":
    ai_difficulty = 2
if player_difficulty_selection.title() == "Hard":
    ai_difficulty = 3
if player_difficulty_selection.title() == "Extra Hard":
    ai_difficulty = 4

# Begin game
print("\n" + player_difficulty_selection.title() + " AI selected.\n")
print("Get ready!\n")
# Continue game until one player runs out of Ships
while grid2.total_health > 0 and grid1.total_health > 0:
    grid2.print_grid()
    player_target = (input("Where would you like to fire? ")).upper()
    # Exit statement to cancel game
    if player_target == "CLEAR" or player_target == "EXIT":
        break
    # Make sure that the player chose a valid target
    while player_target not in Player1.target_points:
        player_target = (input("Where would you like to fire? ")).upper()
        if player_target in Player1.target_points:
            break
    # Fire shots and update the Grid for each turn
    Player1.fire(player_target)
    time.sleep(2)
    grid1.print_grid()
    time.sleep(2)
    Player2.fire(Player2.ai(ai_difficulty))
    time.sleep(2)

# Determine who won the game
if grid1.total_health > 0 and grid2.total_health == 0:
    print("You won! Congratulations!")
if grid2.total_health > 0 and grid1.total_health == 0:
    print("You Lost! Sorry!")
if grid1.total_health == grid2.total_health and grid1.total_health == 0:
    print("Tie!")
else:
    print("Game ended.")