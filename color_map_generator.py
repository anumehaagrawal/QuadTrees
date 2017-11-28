#SURFACE MAPPPER
#Outputs 2d color map and color range bar of a surface to represent changes in data values
#Input:- Either through function mapping or induvidual data readings.

from PIL import Image
import matplotlib.pyplot as plt
import matplotlib as mpl

# List for containing hex values
rgbtub=()
rgbhex=[]

# Converting the rgb value tuple to hex value for the colour
def rgb_to_hex(rgbtup):

    hexval='#%02x%02x%02x' % rgbtup
    rgbhex.append(hexval)

# Displaying the colour bar range according to hexvalues using matplotlib
def range_bar(maximum,minimum):

    ran=maximum-minimum
    mini=minimum
    # Setting font size and font name of the text in the bar
    mpl.rcParams.update({'font.size': 5})
    hfont = {'fontname':'Calibri'}
    # Setting figure object dimensions
    fig=plt.figure(figsize=(8,3))
    ax=fig.add_subplot(111)
    # values displayed at for each interval of colour range
    vals=[]
    vals.append(minimum)
    i=10
    # Creating a list of hexvalues
    while i>0:
        mini=mini+(ran/10)
        vals.append(int(mini))
        rgblist=data_to_rgb(mini,maximum,minimum)
        rgblist=[int(x) for x in rgblist]
        rgbtuple=tuple((rgblist))
        rgb_to_hex(rgbtuple)
        i-=1
    # ListColorMap object containing information of colours we want to display
    cmap = mpl.colors.ListedColormap(rgbhex)
    norm = mpl.colors.BoundaryNorm(vals, cmap.N)
    # Creating the color bar with interval values
    cb = mpl.colorbar.ColorbarBase(ax, cmap=cmap,norm=norm,spacing='uniform',orientation='horizontal',extend='neither',ticks=vals) #wtf
    cb.set_label('Color map', **hfont)
    ax.set_position((0.1, 0.45, 0.8, 0.1))
    #plt.savefig("./colourbar.png", dpi=300, transparent=True)
    plt.show()

#Given list of pixels(nodes)=tree reconstructs image at compression level=level
def disp(tree, level):
    start = 0
    size=len(tree)

    # Calculate position of starting node of height
    for i in range(0, level):
        start = 4 * start + 1
    # Checking if valid height
    if (start > size):
        print('Invalid level; Please enter a lower compression level.')
        return
    # Create a new image with the dimensions 512*512
    img = Image.new("RGB", (512,512), "black")
    pixels = img.load()
    # Move from starting to last node on given height
    for i in tree[start : 4 * start]:
        x1 = i.topLeft.x
        y1 = i.topLeft.y
        x2 = i.bottomRight.x
        y2 = i.bottomRight.y
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                # Set colour
                pixels[x, y] = (int(i.R), int(i.G), int(i.B))

    # Display image
    img.show();
    # Saving the image in the current directory
    img.save('output_image.png')

#Input function, reads data from input list generated in main.h=height,w=width of data set in 2D array
def input_data(datal,h,w):

    #calculates the nearest power of four to convert to a 4^n x 4^n grid
    dimension=nearest_four(max(h,w))
    data_list=[[None for j in range(0,dimension)] for i in range(0,dimension)]
    #initializing max and min values
    maximum=-9999999999999
    minimum=9999999999999
    #Adding data to new 4^n x 4^n grid while obtaining max and min data values
    for i in range(0,h):
        for j in range(0,w):
            data_list[i][j]=datal[i][j]
            if datal[i][j]>maximum:
                maximum=datal[i][j]
            if datal[i][j]<minimum:
                minimum=datal[i][j]
    #Setting color as black for pixels outside range of input data in grid
    for i in range(h,dimension):
        for j in range(w,dimension):
            data_list[i][j]=Pixel()
    #Setting rgb values for pixels using corresponding data values
    for i in range(0,h):
        for j in range(0,w):
            data_list[i][j]=Pixel(color=data_to_rgb(data_list[i][j],maximum,minimum))
    #printing range bar for colors displayed on colour map
    range_bar(maximum,minimum)
    return data_list

#Calculating nearest 4^n value greater than an integer
def nearest_four(value):
    if (value > 0) and ((value & (value - 1)) == 0) and ((value & 0x55555555)):
        return value
    answer=0
    while value!=0:
        value=value>>2
        answer+=1
    return 4**answer

#Simple iterative code to convert tree node form of quad tree to list
def tree_to_list(root):

    output=[]
    #Using list as queue to ensure updation in correct order
    queue=[]
    current=root
    #appending node to output and pushing its children to the queue
    while current is not None:
        output.append(current)
        queue.append(current.child_1)
        queue.append(current.child_2)
        queue.append(current.child_3)
        queue.append(current.child_4)
        output.append(current)
        if len(queue)!=0:
            current=queue.pop(0)
        else:
            current=None
    return output

#Converts data in a range between min_data to max_data to rgb ,returns [r,g,b]
def data_to_rgb(data,max_data,min_data):
    ran= max_data-min_data
    data=data-min_data
    if 0<=data<=(0.125*ran):
        r=0
        g=0
        b=(4/ran)*data+0.5
    elif (0.125*ran)<data<=(0.375*ran):
        r=0
        g=(4/ran)*data-0.5
        b=1
    elif (0.375*ran)<data<=(0.652*ran):
        r=(4/ran)*data-1.5
        g=1
        b=2.5-(4/ran)*data
    elif (0.625*ran)<data<=(0.875*ran):
        r=1
        g=3.5-(4/ran)*data
        b=0
    elif (ran*0.875)<data<=ran:
        r=4.5-(4/ran)*data
        g=0
        b=0
    else:
        r=0
        g=0
        b=0
    return [r*255,g*255,b*255]

# Defining the coordinates in 2D space
class Point:

	def __init__(self,x,y):
		self.x=x
		self.y=y

#Defining attributes of a pixel in an image
class Pixel:

    def __init__(self,color=[0,0,0],topLeft=Point(0,0),bottomRight=Point(0,0)):
        self.topLeft=topLeft
        self.bottomRight=bottomRight
        self.parent=None
        #RGB values
        self.R=color[0]
        self.G=color[1]
        self.B=color[2]
        #Children
        self.child_1=None
        self.child_3=None
        self.child_2=None
        self.child_4=None
    def isLeaf(self):
        if(self.child_1 is None or self.child_3 is None or self.child_2 is None or self.child_4 is None):
            return True
        return False

#Defining a matrix class to process nodes and assign locations in 2D space to each pixel
class Matrix:
    def __init__(self,m):
        self.m=m
        self.y=0
        self.count=0
        #Assigning topLeft and bottomRight corner coordinates to every pixel
        for p in range(len(self.m)):
            self.x=0
            for q in range(len(self.m[0])):
                self.m[p][q].topLeft=Point(self.x,self.y)
                self.m[p][q].bottomRight=Point(self.x+1,self.y+1)
                self.x+=1
            self.y+=1

#Builds a Quad tree out of leaf pixel nodes generated by Matrix class processing
def build(arr):

    count=1
    #Loop to process pixels and assign parents. Ends when input list has only one element which will be the root
    #Building Quad tree from bottom up
    while not(len(arr)==1 and len(arr[0])==1):
        #division by 2 each time to account for reducing number of nodes at each level
        output=[[0 for i in range(0,len(arr)//2)] for i in range(0,len(arr)//2)]
        j=0
        while j<len(arr):
            i=0
            while i<len(arr[0]):
                Node=Pixel()

                arr[j][i].parent=Node
                Node.child_1=arr[j][i]

                arr[j+1][i].parent=Node
                Node.child_2=arr[j+1][i]

                arr[j][i+1].parent=Node
                Node.child_3=arr[j][i+1]

                arr[j+1][i+1].parent=Node
                Node.child_4=arr[j+1][i+1]

                Node.topLeft=Node.child_1.topLeft
                Node.bottomRight=Node.child_4.bottomRight

                if not Node.isLeaf():
                    Node.R=(Node.child_1.R+Node.child_3.R+Node.child_2.R+Node.child_4.R)/4
                    Node.G=(Node.child_1.G+Node.child_3.G+Node.child_2.G+Node.child_4.G)/4
                    Node.B=(Node.child_1.B+Node.child_3.B+Node.child_2.B+Node.child_4.B)/4

                output[j//2][i//2]=Node

                if i+2<len(arr[0]):
                    i=i+2
                else:
                    break

            if j+2<len(arr):
                j=j+2
            else:
                break

        arr=output
    return [arr[0][0],count]

def main():
    #data input list
    datal=[[None for i in range(0,256)] for j in range(0,256)]
    #assigning f(i,j) as data value at (i,j)
    for i in range(-128,128):
        for j in range(-128,128):
            #f(i,j) function coded here
            datal[i][j]=((i*(j**2))/4+(j*(i**2))/4)

    l1=input_data(datal,256,256)
    m1=Matrix(l1)
    ret=build(m1.m)
    #display output at set compression level
    disp(tree_to_list(ret[0]),6)

if __name__=="__main__":
    main()
