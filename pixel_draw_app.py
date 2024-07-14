from tkinter import *
import numpy as np
from PIL import ImageGrab,ImageTk,ImageShow
from pickle import *
from tkinter.simpledialog import askstring


class DrawFrame():
    def __init__(self,windows) -> None:
        self.checkVar=IntVar()
        windows.attributes("-fullscreen",True)
        for column in range(7):
            windows.columnconfigure(column,minsize=windows.winfo_screenwidth()//7)
        for row in range(10):
            windows.rowconfigure(row,minsize=windows.winfo_screenheight()//10)
        self.canvasDraw=Canvas(windows,height=0,width=0)
        self.pen=10
        self.color="yellow"
    
        self.dimXLabel=Label(windows,text="DimX")
        self.dimYLabel=Label(windows,text="DimY")

        self.dimXLabel.grid(column=5,row=0)
        self.dimYLabel.grid(column=5,row=1)

        self.dimXEntry=Entry(windows)
        self.dimYEntry=Entry(windows)

        self.dimXEntry.grid(column=6,row=0)
        self.dimYEntry.grid(column=6,row=1)

        self.dimButton=Button(windows,text="dim",command=lambda :self.generateCanvas(windows))
        self.quitButton=Button(windows,text="quit",command=lambda : quit(windows))
        self.saveButton=Button(windows,text="save",command=lambda : self.save(windows,self.canvasDraw))
        #self.loadButton=Button(windows,text="load",command=lambda :self.load())

        self.dimButton.grid(column=5,row=2,columnspan=2,sticky=NSEW)
        self.quitButton.grid(column=5,row=9,columnspan=2,sticky=NSEW)
        self.saveButton.grid(column=5,row=3,sticky=NSEW)
        #self.loadButton.grid(column=6,row=3,sticky=NSEW)

        self.onePxButton=Button(windows,text="10px",command=lambda:self.penPoint(10))
        self.fivePxButton=Button(windows,text="20px",command=lambda:self.penPoint(20))
        self.tenPxButton=Button(windows,text="30px",command=lambda:self.penPoint(30))
        self.twentyPxButton=Button(windows,text="40px",command=lambda:self.penPoint(40))
        self.fiftyButton=Button(windows,text="50px",command=lambda:self.penPoint(50))

        self.onePxButton.grid(column=0,row=9,sticky=NSEW)
        self.fivePxButton.grid(column=1,row=9,sticky=NSEW)
        self.tenPxButton.grid(column=2,row=9,sticky=NSEW)
        self.twentyPxButton.grid(column=3,row=9,sticky=NSEW)
        self.fiftyButton.grid(column=4,row=9,sticky=NSEW)

        self.eraseButton=Button(windows,bg="white",command=lambda :self.erase("white"))
        self.blueButton=Button(windows,bg="blue",command=lambda : self.penColor("blue"))
        self.greenButton=Button(windows,bg="green",command=lambda : self.penColor("green"))
        self.violetButton=Button(windows,bg="violet",command=lambda : self.penColor("violet"))
        self.redButton=Button(windows,bg="red",command=lambda : self.penColor("red"))
        self.yellowButton=Button(windows,bg="yellow",command=lambda : self.penColor("yellow"))
        self.blackButton=Button(windows,bg="black",command=lambda : self.penColor("black"))
        self.brownButton=Button(windows,bg="brown",command=lambda : self.penColor("brown"))
        self.pinkButton=Button(windows,bg="pink",command=lambda : self.penColor("pink"))

        self.eraseButton.grid(column=5,row=4,sticky=NSEW)
        self.blueButton.grid(column=5,row=5,sticky=NSEW)
        self.greenButton.grid(column=5,row=6,sticky=NSEW)
        self.violetButton.grid(column=5,row=7,sticky=NSEW)
        self.redButton.grid(column=5,row=8,sticky=NSEW)
        self.yellowButton.grid(column=6,row=5,sticky=NSEW)
        self.blackButton.grid(column=6,row=6,sticky=NSEW)
        self.brownButton.grid(column=6,row=7,sticky=NSEW)
        self.pinkButton.grid(column=6,row=8,sticky=NSEW)

        self.gridCheckButton=Checkbutton(windows,text="Show grid",variable=self.checkVar,command=lambda : self.showGrid())

        self.gridCheckButton.grid(column=6,row=4,sticky=NSEW)


        """self.drawGridButton=Button(windows,text="drawGrid",command=self.generateGrid)

        self.drawGridButton.grid(column=1,row=2,columnspan=2,sticky=EW)"""
    def penPoint(self,dim):
        self.pen=dim

    def erase(self,color):
        self.color=color

    def penColor(self,color):
        self.color=color

    def save(self,windows,draw):
        name=askstring("Name","File name ?")
        name=name+".png"
        for i in range(len(Grid.instance)):
            self.canvasDraw.delete(Grid.instance[i].line)
        del Grid.instance[:]
        x=windows.winfo_rootx()+draw.winfo_x()
        y=windows.winfo_rooty()+draw.winfo_y()
        x1=x+draw.winfo_width()
        y1=y+draw.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save(name)
    
    """def load(self):
        image=ImageTk.PhotoImage(file="path/first.png")
        self.canvasDraw.create_image(0,0,image=image)
        ImageShow.show(image)"""
    
    def showGrid(self):
        if(self.checkVar.get()==1):
            self.generateGrid()
        elif(self.checkVar.get()==0):
            for i in range(len(Grid.instance)):
                self.canvasDraw.delete(Grid.instance[i].line)
            del Grid.instance[:]


    
    
    def generateCanvas(self,windows):
        self.canvasDraw.destroy()
        self.canvasDraw=Canvas(windows,height=strToInt(self.dimYEntry.get()),width=strToInt(self.dimXEntry.get()),bg="white")
        self.canvasDraw.grid(column=0,row=0,rowspan=9,columnspan=5)
        self.canvasDraw.bind('<Button-1>',self.drawPixel)
        self.generateMatrix()



    def generateMatrix(self):
        nbColumn=strToInt(self.dimXEntry.get())//10
        nbRow=strToInt(self.dimYEntry.get())//10
        self.caseMatrix=np.zeros((nbColumn,nbRow,2),dtype=int)
        for i in range(nbRow):
            for j in range(nbColumn):
                self.caseMatrix[j,i,0]=i*10
                self.caseMatrix[j,i,1]=j*10
                

    def generateGrid(self):
        nbColumn=strToInt(self.dimXEntry.get())//10
        nbRow=strToInt(self.dimYEntry.get())//10
        for i in range(nbColumn):
            #self.canvasDraw.create_line(i*10,0,i*10,strToInt(self.dimYEntry.get()),fill="gray")
            Grid(self,i*10,0,i*10,strToInt(self.dimYEntry.get()),fill="gray")
        for j in range(nbRow):
            #self.canvasDraw.create_line(0,j*10,strToInt(self.dimXEntry.get()),j*10,fill="gray")
            Grid(self,0,j*10,strToInt(self.dimXEntry.get()),j*10,fill="gray")
    
    def drawPixel(self,event):
        nbColumn=strToInt(self.dimXEntry.get())//10
        nbRow=strToInt(self.dimYEntry.get())//10
        for i in range(nbRow):
            for j in range(nbColumn):
                if((event.x>=self.caseMatrix[j,i,0] and event.x<self.caseMatrix[j,i,0]+10) and (event.y>=self.caseMatrix[j,i,1] and event.y<self.caseMatrix[j,i,1]+10) ):
                    self.canvasDraw.create_rectangle(self.caseMatrix[j,i,0],self.caseMatrix[j,i,1],self.caseMatrix[j,i,0]+self.pen,self.caseMatrix[j,i,1]+self.pen,fill=self.color,outline=self.color)
                    if(self.checkVar.get()==1):
                        self.generateGrid()

        #self.canvasDraw.create_rectangle(event.x-10,event.y-10,event.x+10,event.y+10,fill="yellow")

class Grid():
    instance=list()
    
    def __init__(self,draw,x0,x1,y0,y1,fill):
        Grid.instance.append(self)
        self.line=draw.canvasDraw.create_line(x0,x1,y0,y1,fill=fill)

    


def strToInt(number):
    intNumber=0
    for letter in number:
        intNumber=intNumber*10+ord(letter)-ord("0")
    return intNumber

def quit(windows):
    windows.quit()

fen=Tk()

draw=DrawFrame(fen)


fen.mainloop()
