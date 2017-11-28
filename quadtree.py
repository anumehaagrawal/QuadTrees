# Holds details of the node

class Node:
    def __init__(self,data=None,pos=None):
        self.data=data
        self.pos=pos

# Holds details of coordinates of the point

class Point:
    def __init__(self,x=None,y=None):
        self.x=x
        self.y=y

class Quad:
    def __init__(self,topLeft=None,botRight=None):
        # Coordinates of the topleft point and bottomRight point of quadtree

        self.topLeft=topLeft
        self.botRight=botRight
        if self.topLeft is None:
            self.topLeft=Point(0,0)
        if self.botRight is None:
            self.botRight=Point(0,0)
        self.n=None

        # contains details of the node in the quad
        self.contains=[]

        #Initial four children of the QuadTree
        self.topLeftTree=None
        self.topRightTree=None
        self.botRightTree=None
        self.botLeftTree=None

    # Checks if the point of the node lies within the boundary of the Quad tree
    def isBoundary(self,point):
        return (point.x>=self.topLeft.x and point.x<=self.botRight.x and point.y>=self.topLeft.y and point.y<=self.botRight.y)

    # Inserting a node in the Quad Tree
    def insert(self,node):
        # Checks if node is none

        if node is None:
            return
        # Checks if the node lies within boundary conditions

        if not self.isBoundary(node.pos):
            return
        #Checks if the quad is of unit area and cannot be subdivided

        if (abs(self.topLeft.x - self.botRight.x) <= 1 and abs(self.topLeft.y - self.botRight.y) <= 1):
    
            if (self.n is None):
                self.n = node
            return
        # Checking in which of the four quarters of a quad the node belongs to
    
        # Checking if node belongs to left half

        if((self.topLeft.x+self.botRight.x)/2 >= node.pos.x):

            # checking of node belongs to top left half

            if((self.topLeft.y+self.botRight.y)/2 >= node.pos.y):

                # checking if the topleftTree is empty or not

                if self.topLeftTree is None:
                    # If its not empty then it becomes child of this topleft half depending on its coordinates location

                    self.topLeftTree=Quad(Point(self.topLeft.x,self.topLeft.y),Point((self.topLeft.x+self.botRight.x)/2,(self.topLeft.y+self.botRight.y/2)))
                    self.topLeftTree.contains.append(node.data)
                else:
                    self.topLeftTree.insert(node)
            # checking of node belongs to bottom left half
       
            else:
                # checking if the bottomleftTree is empty or not 
                if self.botLeftTree is None:
                    # If its not empty then it becomes child of this bottomleft half depending on its coordinates location

                    self.botLeftTree=Quad(Point(self.topLeft.x,(self.topLeft.y+self.botRight.y)/2),Point((self.topLeft.x+self.botRight.x)/2,self.botRight.y))
                    self.botLeftTree.contains.append(node.data)
                else:
                    self.botLeftTree.insert(node)
         # Checking if node belongs to right half

        else:
            # checking of node belongs to top right half

            if((self.topLeft.y+self.botRight.y)/2 >= node.pos.y):
                if self.topRightTree is None:
                    self.topRightTree=Quad(Point((self.topLeft.x+self.botRight.x)/2,self.topLeft.y),Point(self.botRight.x,(self.botRight.y+self.topLeft.y)/2))
                    self.topRightTree.contains.append(node.data)
                else:
                    self.topRightTree.insert(node)
            # checking of node belongs to bottom right half       
            else:

                if self.botRightTree is None:
                    self.botRightTree=Quad(Point((self.topLeft.x+self.botRight.x)/2,(self.topLeft.y+self.botRight.y)/2),Point(self.botRight.x,self.botRight.y))
                    self.botRightTree.contains.append(node.data)
                else:
                    self.botRightTree.insert(node)

    #Find a node in a quadtree

    def search(self,p,data):
        # Point is out of Boundary range
        if not self.isBoundary(p):
            return None

        if self.n is not None:
            return self.n
        # Checking if the node is supposed to belong to top  half (if node is present) depending on location

        if ((self.topLeft.x + self.botRight.x) / 2 >= p.x):
            if ((self.topLeft.y + self.botRight.y) / 2 >= p.y):
        
                if (self.topLeftTree is None):
                    return None
                else:
                    
                    if data==self.topLeftTree.contains[0]:
                        return True
                    else:
                        return self.topLeftTree.search(p,data);
                    

            else:
        
                if (self.botLeftTree is None):
                    return None
                else:
                    if data==self.botLeftTree.contains[0]:
                        return True
                    else:
                        return self.botLeftTree.search(p,data);

        # Checking if the node is supposed to belong to bottom half (if node is present) depending on location

        else:
  
            if ((self.topLeft.y + self.botRight.y) / 2 >= p.y):
        
                if (self.topRightTree is None):
                    return None
                else:
                    if data==self.topRightTree.contains[0]:
                        return True
                    else:
                        return self.topRightTree.search(p,data);
   
            
            else:
        
                if (self.botRightTree is None):
                    return None
                else:
                    if data==self.botRightTree.contains[0]:
                        return True
                    else:
                        return self.botRightTree.search(p,data);
        
# Defining the main class

def main():

    # Defining original points
    p1=Point(0,0)
    p2=Point(9,9)
    Q=Quad(p1,p2) 
    # Creating nodes for quad tree
    
    n=int(input("Enter number of nodes you want to insert"))
    for i in range(n):
        a=int(input("Enter data of node"))
        x=int(input("Enter x coordinate of node"))
        y=int(input("Enter y coordinate of node"))
        Q.insert(Node(a,Point(x,y)))
    data=int(input("Enter data of node to be searched"))
    xsearch=int(input("Enter x coordinate of node"))
    ysearch=int(input("Enter y coordinate of node"))
    c=Q.search(Point(xsearch,ysearch),data)
    print(c)



main()

