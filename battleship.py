

class Point:

    def __init__(self, xcoord, ycoord):
        self.xcoord = str(xcoord)
        self.ycoord = str(ycoord)
        self.position = self.xcoord + self.ycoord
        self.value = "-"
        
    
    def __repr__(self):
        return self.position
        
    

class Grid:

    def __init__(self, name):
        self.name = name

    #Defining the Points:
        abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        row1 = [Point(x, "1 ") for x in abc]
        row2 = [Point(x, "2 ") for x in abc]
        row3 = [Point(x, "3 ") for x in abc]
        row4 = [Point(x, "4 ") for x in abc]
        row5 = [Point(x, "5 ") for x in abc]
        row6 = [Point(x, "6 ") for x in abc]
        row7 = [Point(x, "7 ") for x in abc]
        row8 = [Point(x, "8 ") for x in abc]
        row9 = [Point(x, "9 ") for x in abc]
        row10 = [Point(x, "10") for x in abc]
        rows = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10]

        
        
    #Printing the Grid:
        print(self.name)
        print("   A B C D E F G H I J")
        for row in rows:
            num = row[0].ycoord
            symbolA = row[0].value
            symbolB = row[1].value
            symbolC = row[2].value
            symbolD = row[3].value
            symbolE = row[4].value
            symbolF = row[5].value
            symbolG = row[6].value
            symbolH = row[7].value
            symbolI = row[8].value
            symbolJ = row[9].value
            print("{} {} {} {} {} {} {} {} {} {} {}".format(num, symbolA, symbolB, symbolC, symbolD, symbolE, symbolF, symbolG, symbolH, symbolI, symbolJ))
        

grid1 = Grid("Grid #1")
grid1.fire("C3")
