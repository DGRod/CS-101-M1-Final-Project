import random


class Point:

    def __init__(self, xcoord, ycoord):
        self.xcoord = str(xcoord)
        self.ycoord = str(ycoord)
        self.position = self.xcoord + self.ycoord
        self.value = "-"
        self.is_ship = False
        
    
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
        return self.name + "has " + str(self.health) + " health."

    def damage(self):
        self.health += -1
        
    
    def sink(self):
        if self.health == 0:
            self.sunk = True
            if self.team == "Enemy":
                return "You sunk the enemy " + self.name + "!"
            else:
                return "Your " + self.name + " has been sunk!"

        
    

class Grid:

    def __init__(self, name):
        self.name = name

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
            self.points_dict[point].make_ship(ship.name[0])
            taken_points.append(point)

        for point in taken_points:
            for position in self.all_positions_on_grid:
                if point in position:
                    bad_positions.append(position)
        
        for position in bad_positions:
            if bad_positions.count(position) > 1:
                while bad_positions.count(position) > 1:
                    bad_positions.remove(position)

        print(bad_positions)

        for position in self.all_positions_on_grid:
            if position in bad_positions:
                self.all_positions_on_grid.remove(position)
        print("self.all_positions_on_grid")
        print(self.all_positions_on_grid)

            #Why does this not eliminate every position in self.all_positions_on_grid that contains any point from ship.position

        


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



    def fire(self, target):
        print("Firing at " + target)
        if self.points_dict[target].is_ship == True:
            print("Hit!")
            self.points_dict[target].hit()
            self.print_grid()
        else:
            print("Miss!")
            self.points_dict[target].miss()
            self.print_grid()
        

grid1 = Grid("Your Grid:")
grid2 = Grid("Enemy Grid:")

grid1.place_ship(Ship("Destroyer", "Player", 3))
grid1.place_ship(Ship("Carrier", "Player", 5))
grid1.place_ship(Ship("Submarine", "Player", 3))
grid1.place_ship(Ship("Patrol Boat", "Player", 2))
grid1.place_ship(Ship("Battleship", "Player", 4))

grid1.print_grid()

'''for x in range(0,3):
    grid2.print_grid()
    grid2.fire(input("Where would you like to fire? "))
    grid1.print_grid()
    grid1.fire(random.choice(grid1.points_list))'''
    