import random
import time


class Point:

    def __init__(self, xcoord, ycoord):
        self.xcoord = str(xcoord)
        self.ycoord = str(ycoord)
        self.position = self.xcoord + self.ycoord
        self.value = "-"
        self.is_ship = False
        self.probability = 0.0
        
    
    
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
        self.value = "X"
    
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

        

    
    def place_ship(self, ship):

        available_ship_positions = []
        for position in ship.all_positions:
            if position in self.all_positions_on_grid:
                available_ship_positions.append(position)



        ship.position = random.choice(available_ship_positions)
        


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
        self.previous_target = "A0"
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

        

    def ai(self, difficulty=1):



        if difficulty == 3:

            available_enemy_positions = []
            for position in self.all_enemy_positions:
                point_list = []
                for point in position:
                    if point in self.target_points:
                        point_list.append(point)
                if point_list == position:
                    available_enemy_positions.append(position)

            
            


































        if difficulty == 2:
            target = random.choice(self.target_points)
            likely_points = []

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


                clean_likely_points = []
                for point in likely_points:
                    if point in self.target_points:
                        clean_likely_points.append(point)
                for point in clean_likely_points:
                    if clean_likely_points.count(point) > 1:
                        while clean_likely_points.count(point) > 1:
                            clean_likely_points.remove(point)
                print("Likely points: ", clean_likely_points)
                
                hit_neighbors = self.enemy_grid.points_dict[self.hit_point].neighbors()
                clean_hit_neighbors = []
                for point in hit_neighbors:
                    if point in self.target_points:
                        clean_hit_neighbors.append(point)
                print("Hit neighbors", clean_hit_neighbors)

                if len(clean_likely_points) > 0:
                    target = random.choice(clean_likely_points)

                elif len(clean_hit_neighbors) > 0:
                    target = random.choice(clean_hit_neighbors)

                else:
                    self.hit_point = "  "
            
            return target   



        if difficulty == 1:
            target = random.choice(self.target_points)

            if self.hit_point != "  ":

                hit_neighbors = self.enemy_grid.points_dict[self.hit_point].neighbors()
                clean_hit_neighbors = []
                for point in hit_neighbors:
                    if point in self.target_points:
                        clean_hit_neighbors.append(point)
                print(clean_hit_neighbors)
                if len(clean_hit_neighbors) > 0:
                    target = random.choice(clean_hit_neighbors)
                else:
                    self.hit_point = "  "
            
            return target   








    def fire(self, target):
        time.sleep(3)
        print("Turn #" + str(self.counter))
        print("Firing at " + target)
        self.counter += 1
        self.target_points.remove(target)
        self.previous_target = target
        if self.enemy_grid.points_dict[target].is_ship == True:
            print("Hit!")
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

    
            
        


        












grid1 = Grid("Your Grid:")
grid2 = Grid("Enemy Grid:")

grid1.place_ship(Ship("Destroyer", "Player", 3))
grid1.place_ship(Ship("Carrier", "Player", 5))
grid1.place_ship(Ship("Submarine", "Player", 3))
grid1.place_ship(Ship("Patrol Boat", "Player", 2))
grid1.place_ship(Ship("Battleship", "Player", 4))

grid2.place_ship(Ship("Destroyer", "Enemy", 3))
grid2.place_ship(Ship("Carrier", "Enemy", 5))
grid2.place_ship(Ship("Submarine", "Enemy", 3))
grid2.place_ship(Ship("Patrol Boat", "Enemy", 2))
grid2.place_ship(Ship("Battleship", "Enemy", 4))




Player1 = Player("Player", "Diego", grid1, grid2)
Player2 = Player("Enemy", "Computer", grid2, grid1)



grid1.print_grid()
grid2.reveal_ships()


'''for x in range(0,10):
    grid2.print_grid()
    Player1.fire(input("Where would you like to fire? "))
    grid1.print_grid()
    Player2.fire(random.choice(grid1.points_list))'''
    
while grid2.total_health > 0:
    Player1.fire(Player1.ai(3))


