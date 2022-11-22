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

    def __init__(self, name, team, position):
        self.name = name
        self.team = team
        self.position = position
        self.sunk = False
        self.health = len(position)
        self.all_points = []
        abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        numbers = [str(x) for x in range(0, 10)]
        for letter in abc:
            for number in range(0,10):
                self.all_points.append(letter + str(number))
        self.all_points_dict = {point:Point(point[0], point[-1]) for point in self.all_points}
        self.all_positions = []
        for letter in abc:
            for x in range(0, 11 - len(self.position)):
                self.all_positions.append(self.all_points_dict[(letter + str(x))].slicer(self.all_points_dict[(letter + str(x + len(self.position) - 1))]))
        for number in numbers:
            for x in range(0, 11 - len(self.position)):
                print(self.all_points_dict[abc[x] + number].slicer(self.all_points_dict[(abc[x + len(self.position) - 1] + number)]))
                self.all_positions.append(self.all_points_dict[abc[x] + number].slicer(self.all_points_dict[(abc[x + len(self.position) - 1] + number)]))


        print(self.all_positions)
                

    
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

    
    def place_ship(self, ship):

        for pt in ship.position:
            self.points_dict[pt].make_ship(ship.name[0])
        
        


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

grid1.place_ship(Ship("Destroyer", "Player", input("Please enter the coordinates where you would like your destroyer: ").split()))

for x in range(0,3):
    grid2.print_grid()
    grid2.fire(input("Where would you like to fire? "))
    grid1.print_grid()
    grid1.fire(random.choice(grid1.points_list))
    