

class Point:

    def __init__(self, xcoord, ycoord):
        self.xcoord = str(xcoord)
        self.ycoord = str(ycoord)
        self.position = self.xcoord + self.ycoord
        self.value = "-"
        
    
    def __repr__(self):
        return self.position
    
    def change(self, new_value):
        self.value = new_value
        
    

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

        points_list = []
        for row in self.rows:
            for point in row:
                points_list.append(point)

        self.points_dict = {point:Point(point[0], point[-1]) for point in points_list}

    
    def place_ship(self, ship_type, location):
        print(location)
        for pt in location:
            self.points_dict[pt].change(ship_type[0])
        
        


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
        

grid1 = Grid("Enemy Grid:")

grid1.place_ship("Destroyer", ["A1", "B1", "C1"])
grid1.print_grid()
