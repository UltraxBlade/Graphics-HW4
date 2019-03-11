from Graphics import *
from matrix import *
from display import *

homeTest=False

def parse(filename,edges,transform,img,color):
    f=open(filename,"r")
    script=f.read().split("\n")
    f.close()
    i=0
    while i<len(script):
        if script[i]=="line":
            coords=script[i+1].split(" ")
            for k in range(len(coords)):
                coords[k]=int(coords[k])
            addEdge(edges,coords[0],coords[1],coords[2],coords[3],coords[4],coords[5])
            i+=1
        elif script[i]=="ident":
            transform=I(4)
        elif script[i]=="apply":
            edges=multMatrix(transform,edges)
        elif script[i]=="quit":
            return
        elif script[i]=="move":
            coords=script[i+1].split(" ")
            for k in range(len(coords)):
                coords[k]=int(coords[k])
            transform=multMatrix(translate(coords[0],coords[1],coords[2]),transform)
            i+=1
        elif script[i]=="scale":
            coords=script[i+1].split(" ")
            for k in range(len(coords)):
                coords[k]=float(coords[k])
            transform=multMatrix(scale(coords[0],coords[1],coords[2]),transform)
            i+=1
        elif script[i]=="rotate":
            coords=script[i+1].split(" ")
            transform=multMatrix(rotate(coords[0],float(coords[1])),transform)
            i+=1
        elif script[i]=="save":
            clear(img)
            drawLines(img,edges,color)
            if homeTest:
                save_ppm(img,script[i+1])
            else:
                save_extension(img,script[i+1])
            i+=1
        elif script[i]=="circle":
            coords=script[i+1].split(" ")
            for k in range(len(coords)):
                coords[k]=int(coords[k])
            circle(edges,coords[0],coords[1],coords[2],coords[3])
            i+=1
        elif script[i]=="hermite":
            coords=script[i+1].split(" ")
            for k in range(len(coords)):
                coords[k]=int(coords[k])
            hermite(edges,coords[0],coords[1],coords[2],coords[3],coords[4],coords[5],coords[6],coords[7])
            i+=1
        elif script[i]=="bezier":
            coords=script[i+1].split(" ")
            for k in range(len(coords)):
                coords[k]=int(coords[k])
            bezier(edges,coords[0],coords[1],coords[2],coords[3],coords[4],coords[5],coords[6],coords[7])
            i+=1
        elif script[i]=="display" and not homeTest:
            clear(img)
            drawLines(img,edges,color)
            display(img)
        i+=1

img=generate(501,501)
edges=[[],[],[],[]]
transform=I(4)
parse("script",edges,transform,img,[0,0,0])
