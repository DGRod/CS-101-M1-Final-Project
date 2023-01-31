import random
import time



class Point:

    def __init__(self, xcoord, ycoord):
        self.xcoord = str(xcoord)
        self.ycoord = str(ycoord)
        self.position = self.xcoord + self.ycoord
        self.value = "-"
        self.is_ship = False
        self.probability = 0
        
    
    
    def __repr__(self):
        return self.position


    def slicer(self, other_point):
        numbers = [str(x) for x in range(0, 10)]
        abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        if self.xcoord == other_point.xcoord:
            sliced_numbers = numbers[int(self.ycoord):int(other_point.ycoord) + 1]
            result = []
            for number in sliced_numbers:
                result.append(self.xcoord + number)
            return result
        if self.ycoord == other_point.ycoord:
            sliced_letters = abc[abc.index(self.xcoord):abc.index(other_point.xcoord) + 1]
            result = []
            for letter in sliced_letters:
                result.append(letter + self.ycoord)
            return result
    
    def neighbors(self):
        numbers = [str(x) for x in range(0, 10)]
        abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        neighbors = []
        
        if self.ycoord != "9":
            neighbors.append(self.xcoord + numbers[numbers.index(self.ycoord) + 1])

        if self.ycoord != "0":
            neighbors.append(self.xcoord + numbers[numbers.index(self.ycoord) - 1])
        
        if self.xcoord != "J":
            neighbors.append(abc[abc.index(self.xcoord) + 1] + self.ycoord) 
        
        if self.xcoord != "A":
            neighbors.append(abc[abc.index(self.xcoord) - 1] + self.ycoord)
        
        return neighbors


    def hit(self):
        self.value = '\033[1;31m' + "X" + '\033[0m'
    
    def miss(self):
        self.value = "O"
    
    def make_ship(self, new_value):
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
        self.all_points = []
        abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        numbers = [str(x) for x in range(0, 10)]
        for letter in abc:
            for number in range(0,10):
                self.all_points.append(letter + str(number))
        self.all_points_dict = {point:Point(point[0], point[-1]) for point in self.all_points}
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
        

    #Defining the Points:
        numbers = [str(x) for x in range(0, 10)]
        abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
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

        self.points_list = []
        for row in self.rows:
            for point in row:
                self.points_list.append(point)

        self.points_dict = {point:Point(point[0], point[-1]) for point in self.points_list}

        self.all_positions_on_grid = []
        for letter in abc:
            for possible_length in range(2,6):
                for x in range(0, 11 - possible_length):
                    self.all_positions_on_grid.append(self.points_dict[(letter + str(x))].slicer(self.points_dict[(letter + str(x + possible_length - 1))]))
        for number in numbers:
            for possible_length in range(2,6):
                for x in range(0, 11 - possible_length):
                    self.all_positions_on_grid.append(self.points_dict[abc[x] + number].slicer(self.points_dict[(abc[x + possible_length - 1] + number)]))
        
        for position in self.all_positions_on_grid:
            while self.all_positions_on_grid.count(position) > 1:
                self.all_positions_on_grid.remove(position)

        

    
    def place_ship(self, ship, condition):

        available_ship_positions = []
        for position in ship.all_positions:
            if position in self.all_positions_on_grid:
                available_ship_positions.append(position)
        

        if condition == "Manual":
            player_choice = input("Where would you like to place your " + ship.name + "?\nPlease type the first and last coordinates (separated by a comma) of the position where you would like to place it.\n")
            for i in range(1, 78):
                try:
                    player_choice_a = player_choice[:2]
                    player_choice_b = player_choice[-2:]
                    point_a = self.points_dict[player_choice_a]
                    point_b = self.points_dict[player_choice_b]
                    player_chosen_position = point_a.slicer(point_b)
                    
                    for position in available_ship_positions:
                        if player_chosen_position == position:
                            ship.position = position
                            break
                        else:
                            continue
                except:
                    player_choice = input("\nPlease type the first and last coordinates (separated by a comma) of the position where you would like to place your ship.\n")
                    continue
            
                    
        
        if condition == "Random":
            ship.position = random.choice(available_ship_positions)
        
        if type(condition) == list:
            point_a = self.points_dict[condition[0]]
            point_b = self.points_dict[condition[-1]]
            preset_position = point_a.slicer(point_b)
            ship.position = preset_position

        


        taken_points = []
        bad_positions = []

        for point in ship.position:
            if ship.team == "Player":
                self.points_dict[point].make_ship(ship.name[0])
            if ship.team == "Enemy":
                self.points_dict[point].make_ship("-")
            taken_points.append(point)

        for point in taken_points:
            for position in self.all_positions_on_grid:
                if point in position:
                    bad_positions.append(position)
        
        for position in bad_positions:
            if bad_positions.count(position) > 1:
                while bad_positions.count(position) > 1:
                    bad_positions.remove(position)

        for position in bad_positions:
            if position in self.all_positions_on_grid:
                self.all_positions_on_grid.remove(position)

        self.all_ships.append(ship)
        self.total_health += ship.health
        


    def print_grid(self):
        print(self.name)
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

    
    def reveal_ships(self):
        for ship in self.all_ships:
            for point in ship.position:
                self.points_dict[point].value = '#'



        


class Player:

    def __init__(self, team, name, grid, enemy_grid):
        self.team = team
        self.name = name
        self.grid = grid
        self.enemy_grid = enemy_grid
        self.ships = self.grid.all_ships
        self.target_points = self.enemy_grid.points_list
        self.hit_point = "  "
        self.hit_list = []
        self.most_probable_points = []
        self.counter = 1

        numbers = [str(x) for x in range(0, 10)]
        abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        
        self.all_enemy_positions = []
        for letter in abc:
            for possible_length in range(2,6):
                for x in range(0, 11 - possible_length):
                    self.all_enemy_positions.append(self.enemy_grid.points_dict[(letter + str(x))].slicer(self.enemy_grid.points_dict[(letter + str(x + possible_length - 1))]))
        for number in numbers:
            for possible_length in range(2,6):
                for x in range(0, 11 - possible_length):
                    self.all_enemy_positions.append(self.enemy_grid.points_dict[abc[x] + number].slicer(self.enemy_grid.points_dict[(abc[x + possible_length - 1] + number)]))
        
        for position in self.all_enemy_positions:
            while self.all_enemy_positions.count(position) > 1:
                self.all_enemy_positions.remove(position)


        self.firing_solution_z2 = []
        for number in numbers:
            if int(number) % 2 == 0:
                for letter in ["A", "C", "E", "G", "I"]:
                    self.firing_solution_z2.append(letter + str(number))
            else:
                for letter in ["B", "D", "F", "H", "J"]:
                    self.firing_solution_z2.append(letter + str(number))



    def search(self, target):
        target = self.enemy_grid.points_dict[target]
        numbers = [str(x) for x in range(0, 10)]
        abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        vert_borders = []
        for point in self.enemy_grid.points_list:
            if point[0] == "A":
                vert_borders.append(point)
            if point[0] == "J":
                vert_borders.append(point)
        horz_borders = []
        for point in self.enemy_grid.points_list:
            if point[1] == "0":
                horz_borders.append(point)
            if point[1] == "9":
                horz_borders.append(point)
        
        vert_border_points = [self.enemy_grid.points_dict[item] for item in vert_borders]
        horz_border_points = [self.enemy_grid.points_dict[item] for item in horz_borders]

        left = target
        right = target
        up = target
        down = target

        if target.xcoord != "A":
            var = 1
            left = self.enemy_grid.points_dict[abc[abc.index(target.xcoord) - var] + target.ycoord]
            while left.value != '\033[1;31m' + "X" + '\033[0m' and left.value != "O" and left not in vert_border_points:
                var += 1
                left = self.enemy_grid.points_dict[abc[abc.index(target.xcoord) - var] + target.ycoord]
            if left.value == '\033[1;31m' + "X" + '\033[0m' or left.value == "O":
                left = self.enemy_grid.points_dict[abc[abc.index(target.xcoord) - var + 1] + target.ycoord]
        
        if target.xcoord != "J":
            var = 1
            right = self.enemy_grid.points_dict[abc[abc.index(target.xcoord) + var] + target.ycoord]
            while right.value != '\033[1;31m' + "X" + '\033[0m' and right.value != "O" and right not in vert_border_points:
                var += 1
                right = self.enemy_grid.points_dict[abc[abc.index(target.xcoord) + var] + target.ycoord]
            if right.value == '\033[1;31m' + "X" + '\033[0m' or right.value == "O":
                right = self.enemy_grid.points_dict[abc[abc.index(target.xcoord) + var - 1] + target.ycoord]

        if target.ycoord != "0":
            var = 1
            up = self.enemy_grid.points_dict[target.xcoord + numbers[numbers.index(target.ycoord) - var]]
            while up.value != '\033[1;31m' + '\033[1;31m' + "X" + '\033[0m' + '\033[0m' and up.value != "O" and up not in horz_border_points:
                var += 1
                up = self.enemy_grid.points_dict[target.xcoord + numbers[numbers.index(target.ycoord) - var]]
            if up.value == '\033[1;31m' + "X" + '\033[0m' or up.value == "O":
                up = self.enemy_grid.points_dict[target.xcoord + numbers[numbers.index(target.ycoord) - var + 1]]
                
        if target.ycoord != "9":
            var = 1
            down = self.enemy_grid.points_dict[target.xcoord + numbers[numbers.index(target.ycoord) + var]]
            while down.value != '\033[1;31m' + "X" + '\033[0m' and down.value != "O" and down not in horz_border_points:
                var += 1
                down = self.enemy_grid.points_dict[target.xcoord + numbers[numbers.index(target.ycoord) + var]]
            if down.value == '\033[1;31m' + "X" + '\033[0m' or down.value == "O":
                down = self.enemy_grid.points_dict[target.xcoord + numbers[numbers.index(target.ycoord) + var - 1]]
        
        return [left, right, up, down]



        

    def ai(self, difficulty=1):

        firing_solution_z2_clean = []
        for point in self.firing_solution_z2:     
            if point in self.target_points:
                firing_solution_z2_clean.append(point)

        #print("Firing solution: ", firing_solution_z2_clean)
        


        #=================================================================================================================================
        #4th choice: Probable Points 
        #=================================================================================================================================
        probable_points = []
        probable_target_points = []
            

        for point in self.target_points:
            left = self.search(point)[0]
            right = self.search(point)[1]
            up = self.search(point)[2]
            down = self.search(point)[3]

            horz_slice = left.slicer(right)
            vert_slice = up.slicer(down)


            
            point_probability = 0

            if len(horz_slice) >= 5:
                point_probability += 1
            if len(horz_slice) >= 4:
                point_probability += 1
            if len(horz_slice) >= 3:
                point_probability += 2
            if len(horz_slice) >= 2:
                point_probability += 1

            if len(vert_slice) >= 5:
                point_probability += 1
            if len(vert_slice) >= 4:
                point_probability += 1
            if len(vert_slice) >= 3:
                point_probability += 2
            if len(vert_slice) >= 2:
                point_probability += 1

            self.enemy_grid.points_dict[point].probability = point_probability

        proto_dict = {}
        for (key, value) in self.enemy_grid.points_dict.items():
            if key in self.target_points:
                proto_dict[key] = value
            
        prob_dict = {point.position:point.probability for point in proto_dict.values()}
            
        max_prob = max(prob_dict.values())
        #print("max prob: " + str(max_prob))

        for point in prob_dict.keys():
            #print(point, prob_dict[point])
            if prob_dict[point] == max_prob:
                probable_points.append(point)

            
        for point in probable_points:
                
            if point in self.target_points:
                probable_target_points.append(point)
        #print(probable_target_points)
        #print("Length of probable target points: " + str(len(probable_target_points)))


        probable_firing_solution_points = []
        for point in probable_target_points:
            if point in firing_solution_z2_clean:
                probable_firing_solution_points.append(point)

        #print(probable_firing_solution_points)
                

        #=================================================================================================================================
        #3rd choice: Hit Neighbors
        #=================================================================================================================================
        clean_hit_neighbors = []

        if self.hit_point != "  ":

            hit_neighbors = self.enemy_grid.points_dict[self.hit_point].neighbors()
            
            for point in hit_neighbors:
                if point in self.target_points:
                    clean_hit_neighbors.append(point)
            #print("Clean hit neighbors: " + str(clean_hit_neighbors))

        #=================================================================================================================================
        #2nd choice: Likely Points
        #=================================================================================================================================
        likely_points = []
        clean_likely_points = []

        numbers = [str(x) for x in range(0, 10)]
        abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

        if self.hit_point != "  ":
            if len(self.hit_list) >= 2:
                for point in self.hit_list:
                    other_points = []
                    for pt in self.hit_list:
                        if pt != point:
                            other_points.append(pt)
                    for other_point in other_points:
                        if other_point in self.enemy_grid.points_dict[point].neighbors():
                            if point[0] == other_point[0]:
                                if point[1] < other_point[1]: 
                                    if point[1] != "0":
                                        likely_points.append(point[0] + str(int(point[1]) - 1))
                                    if other_point[1] != "9":
                                        likely_points.append(other_point[0] + str(int(other_point[1]) + 1))
                                if point[1] > other_point[1]:
                                    if point[1] != "9":
                                        likely_points.append(point[0] + str(int(point[1]) + 1))
                                    if other_point[1] != "0":
                                        likely_points.append(other_point[0] + str(int(other_point[1]) - 1))
                            if point[1] == other_point[1]:
                                if abc.index(point[0]) < abc.index(other_point[0]):
                                    if abc.index(point[0]) != 0:
                                        likely_points.append(abc[abc.index(point[0]) - 1] + point[1])
                                    if abc.index(other_point[0]) != 9:
                                        likely_points.append(abc[abc.index(other_point[0]) + 1] + other_point[1])
                                if abc.index(point[0]) > abc.index(other_point[0]):
                                    if abc.index(point[0]) != 9:
                                        likely_points.append(abc[abc.index(point[0]) + 1] + point[1])
                                    if abc.index(other_point[0]) != 0:
                                        likely_points.append(abc[abc.index(other_point[0]) - 1] + other_point[1])


                
            for point in likely_points:
                if point in self.target_points:
                    clean_likely_points.append(point)
            for point in clean_likely_points:
                if clean_likely_points.count(point) > 1:
                    while clean_likely_points.count(point) > 1:
                        clean_likely_points.remove(point)
            #print("Likely points: ", clean_likely_points)

        #=================================================================================================================================
        #1st choice: Probable and Likely Points
        #=================================================================================================================================
        probable_and_likely_points = []

        for point in clean_likely_points:
            if point in probable_target_points:
                probable_and_likely_points.append(point)
        

        if difficulty >= 3:

            if len(probable_and_likely_points) > 0:
                target = random.choice(probable_and_likely_points)
            
            elif len(clean_likely_points) > 0:
                target = random.choice(clean_likely_points)
            
            elif len(clean_hit_neighbors) > 0:
                target = random.choice(clean_hit_neighbors)

            elif len(probable_firing_solution_points) > 0:
                target = random.choice(probable_firing_solution_points)

                '''elif len(probable_target_points) > 0:
                print("Probable points")
                target = random.choice(probable_target_points)'''

            elif len(firing_solution_z2_clean) > 0:
                target = random.choice(firing_solution_z2_clean)
            
            else:
                target = random.choice(self.target_points)

        
        elif difficulty >= 2:

            if len(clean_likely_points) > 0:
                target = random.choice(clean_likely_points)
            
            elif len(clean_hit_neighbors) > 0:
                target = random.choice(clean_hit_neighbors)
              
            else:
                target = random.choice(self.target_points)
        

        elif difficulty >= 1:

            if len(clean_hit_neighbors) > 0:
                target = random.choice(clean_hit_neighbors)
              
            else:
                target = random.choice(self.target_points)

        return target









    def fire(self, target):
        print("Turn #" + str(self.counter))

        if self.name == player_one_name:
            print("Firing at " + target)
        else:
            print("Enemy firing at " + target)

        self.counter += 1
        self.target_points.remove(target)
        if self.enemy_grid.points_dict[target].is_ship == True:
            print( '\033[1;31m' + "////////////HIT!////////////" + '\033[0m')
            self.hit_point = target
            self.hit_list.append(target)
            self.enemy_grid.points_dict[target].hit()
            for ship in self.enemy_grid.all_ships:
                if target in ship.position:
                    ship.damage()
                    self.enemy_grid.total_health += -1
                    if ship.health == 0:
                        ship.sink()
            
            self.enemy_grid.print_grid()
        else:
            print("Miss!")
            self.enemy_grid.points_dict[target].miss()
            self.enemy_grid.print_grid()

    
            




 
#Presets

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



all_preset_placements = [[], preset1_placements, preset2_placements]




#Player Setup

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
         BBBBBBBBBBB      AAA           AAA    TTT             TTT        LLLLLLLLLLLL  EEEEEEEEEEE      SSSSSSSS      HHH       HHH   IIIIIIIIIII   PPP

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

grid1 = Grid("Your Grid:")

player_one_name = input("Please enter player name: ")

choice = input("\n" + player_one_name + ", would you like to manually place your ships, choose from 10 preset options, or have them placed randomly? Please type \'Manual\', \'Preset\', or \'Random\'\n")


if choice.title() != "Manual" and choice.title() != "Preset" and choice.title() != "Random":
    while choice.title() != "Manual" and choice.title() != "Preset" and choice.title() != "Random":
        choice = input("Please type \'Manual\', \'Preset\', or \'Random\'\n")
        if choice.title() == "Manual" or choice.title() == "Preset" or choice.title() == "Random":
            break



if choice.title() == "Manual":
    print("\n")
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
    

if choice.title() == "Random":
    grid1.place_ship(Ship("Aircraft Carrier", "Player", 5), "Random")
    grid1.place_ship(Ship("Battleship", "Player", 4), "Random")
    grid1.place_ship(Ship("Destroyer", "Player", 3), "Random")
    grid1.place_ship(Ship("Submarine", "Player", 3), "Random")
    grid1.place_ship(Ship("Patrol Boat", "Player", 2), "Random")
    

if choice.title() == "Preset":
    print("Here are some preset ship layout options. To select one, just type its number.")
    print("\n   ///Preset (1)///")
    preset1.print_grid()
    print("\n   ///Preset (2)///")
    preset2.print_grid()
    
    player_preset_choice = input("\nWhich preset would you like to use?\n")

    for i in range(1, 78):
        try:
            player_preset_choice_number = int(player_preset_choice)
            if int(player_preset_choice) <= 0 or int(player_preset_choice) > (len(all_preset_placements) - 1):
                while int(player_preset_choice) <= 0 or int(player_preset_choice) > (len(all_preset_placements) - 1):
                    player_preset_choice = input("Please type the number of the preset you would like to use.\n")
                    continue
            break
        except:
            player_preset_choice = input("Please type the number of the preset you would like to use.\n")
            continue


    

    chosen_preset_placements = all_preset_placements[player_preset_choice_number]

    print("\nPreset " + str(player_preset_choice_number) + " selected.\n")
    
    grid1.place_ship(Ship("Aircraft Carrier", "Player", 5), chosen_preset_placements[0])
    grid1.place_ship(Ship("Battleship", "Player", 4), chosen_preset_placements[1])
    grid1.place_ship(Ship("Destroyer", "Player", 3), chosen_preset_placements[2])
    grid1.place_ship(Ship("Submarine", "Player", 3), chosen_preset_placements[3])
    grid1.place_ship(Ship("Patrol Boat", "Player", 2), chosen_preset_placements[4])
    

    

#Enemy Grid
grid2 = Grid("Enemy Grid:")

grid2.place_ship(Ship("Aircraft Carrier", "Enemy", 5), "Random")
grid2.place_ship(Ship("Battleship", "Enemy", 4), "Random")
grid2.place_ship(Ship("Destroyer", "Enemy", 3), "Random")
grid2.place_ship(Ship("Submarine", "Enemy", 3), "Random")
grid2.place_ship(Ship("Patrol Boat", "Enemy", 2), "Random")



Player1 = Player("Player", player_one_name, grid1, grid2)
Player2 = Player("Enemy", "Computer", grid2, grid1)



grid1.print_grid()

player_difficulty_selection = input("\nWhat difficulty AI would you like to play against? Please type \'Easy\', \'Medium\', or \'Hard\'\n")

if player_difficulty_selection.title() != "Easy" and player_difficulty_selection.title() != "Medium" and player_difficulty_selection.title() != "Hard":
    while player_difficulty_selection.title() != "Easy" and player_difficulty_selection.title() != "Medium" and player_difficulty_selection.title() != "Hard":
        player_difficulty_selection = input("Please type \'Easy\', \'Medium\', or \'Hard\'\n")
        if player_difficulty_selection.title() == "Easy" or player_difficulty_selection.title() == "Medium" or player_difficulty_selection.title() == "Hard":
            break

if player_difficulty_selection.title() == "Easy":
    ai_difficulty = 1
if player_difficulty_selection.title() == "Medium":
    ai_difficulty = 2
if player_difficulty_selection.title() == "Hard":
    ai_difficulty = 3

print("\n" + player_difficulty_selection.title() + " AI selected.\n")
print("Get ready!\n")

'''while grid2.total_health > 0 and grid1.total_health > 0:
    grid2.print_grid()
    Player1.fire(input("Where would you like to fire? "))
    time.sleep(2)
    grid1.print_grid()
    time.sleep(2)
    Player2.fire(Player2.ai(ai_difficulty))
    time.sleep(2)'''


while grid1.total_health > 0:
    Player2.fire(Player2.ai(3))


if grid1.total_health > 0:
    print("You won! Congratulations!")
if grid2.total_health > 0:
    print("You Lost! Sorry!")
else:
    print("Tie!")


