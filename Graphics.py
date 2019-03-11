#! /usr/bin/python3
import math
from matrix import *

bgcolor=[255,255,255]
def generate(width,height):
    return [[bgcolor[:] for i in range(width)] for j in range(height)]

def output(fileName, img):
    out="P3\n"+str(len(img[0]))+" "+str(len(img))+"\n255\n"
    for row in img:
        for pixel in row:
            for color in pixel:
                out+=str(color)+" "
            out+=" "
        out+="\n"
    f=open(fileName,"w")
    f.write(out)
    f.close()

def clear(img):
    for i in range(len(img)):
        for j in range(len(img[i])):
            img[i][j]=bgcolor[:]

def fadeRing(img,minRad,maxRad,centerX,centerY,color):
    centerRow=len(img)-centerY
    centerCol=centerX
    for rad in range(minRad,maxRad):
        for row in range(len(img)):
            if(rad**2-(row-centerRow)**2)>=0:
                if(int(round(math.sqrt(rad**2-(row-centerRow)**2)+centerCol))<len(img[row]))and(int(round(math.sqrt(rad**2-(row-centerRow)**2)+centerCol))>=0):
                    img[row][int(round(math.sqrt(rad**2-(row-centerRow)**2)+centerCol))]=color[:]
                if(int(round(-math.sqrt(rad**2-(row-centerRow)**2)+centerCol))<len(img[row]))and(int(round(-math.sqrt(rad**2-(row-centerRow)**2)+centerCol))>=0):
                    img[row][int(round(-math.sqrt(rad**2-(row-centerRow)**2)+centerCol))]=color[:]
    return img

def ring(img,minRad,maxRad,centerX,centerY,color):
    centerRow=len(img)-centerY
    centerCol=centerX
    for row in range(len(img)):
        for col in range(len(img[row])):
            if (row-centerRow)**2+(col-centerCol)**2>=minRad**2 and (row-centerRow)**2+(col-centerCol)**2<=maxRad**2:
                img[row][col]=color[:]
    return img
    
def rect(img,width,height,TLX,TLY,color):
    TLrow=len(img)-TLY
    TLcol=TLX
    for row in range(height):
        for col in range(width):
            if TLrow+row<len(img) and TLcol+col<len(img[0]):
                img[TLrow+row][TLcol+col]=color[:]
    return img

def line(img,x0,y0,x1,y1,color):
    r0=len(img)-y0
    r1=len(img)-y1
    c0=x0
    c1=x1
    if r0>r1:
        start=[r1,c1]
        end=[r0,c0]
    elif r0<r1:
        start=[r0,c0]
        end=[r1,c1]
    elif c0>c1:
        start=[r1,c1]
        end=[r0,c0]
    else:
        start=[r0,c0]
        end=[r1,c1]
    drow=end[0]-start[0]
    dcol=end[1]-start[1]
    if drow==0:
        col=start[1]
        row=start[0]
        while col<end[1]:
            if row>=0 and row<len(img) and col>=0 and col<len(img[row]):
                img[row][col]=color[:]
            col+=1
    else:
        slope=dcol/drow
        if slope>=0 and slope<=1:
            row=start[0]
            col=start[1]
            d=2*dcol-drow
            drow*=2
            dcol*=2
            while(row<=end[0]):
                if row>=0 and row<len(img) and col>=0 and col<len(img[row]): 
                    img[row][col]=color[:]
                #c=((c1-c0)/(r1-r0))(r-r0)+c0
                if d>0:
                    col+=1
                    d-=drow
                row+=1
                d+=dcol
        elif slope>1:
            row=start[0]
            col=start[1]
            d=dcol-2*drow
            drow*=2
            dcol*=2
            while(col<=end[1]):
                if row>=0 and row<len(img) and col>=0 and col<len(img[row]):
                    img[row][col]=color[:]
                #c=((c1-c0)/(r1-r0))(r-r0)+c0
                if d<0:
                    row+=1
                    d+=dcol
                col+=1
                d-=drow
        elif slope<0 and slope>=-1:
            row=start[0]
            col=start[1]
            d=2*dcol+drow
            drow*=2
            dcol*=2
            while(row<=end[0]):
                if row>=0 and row<len(img) and col>=0 and col<len(img[row]):
                    img[row][col]=color[:]
                #c=((c1-c0)/(r1-r0))(r-r0)+c0
                if d<0:
                    col-=1
                    d+=drow
                row+=1
                d+=dcol
        elif slope<-1:
            row=start[0]
            col=start[1]
            d=dcol+2*drow
            drow*=2
            dcol*=2
            while(col>=end[1]):
                if row>=0 and row<len(img) and col>=0 and col<len(img[row]):
                    img[row][col]=color[:]
                #c=((c1-c0)/(r1-r0))(r-r0)+c0
                if d>0:
                    row+=1
                    d+=dcol
                col-=1
                d+=drow
    return img

def addPoint(edges,x,y,z):
    edges[0].append(x)
    edges[1].append(y)
    edges[2].append(z)
    edges[3].append(1)
def addEdge(edges,x0,y0,z0,x1,y1,z1):
    addPoint(edges,x0,y0,z0)
    addPoint(edges,x1,y1,z1)
def drawLines(img, edges, color):
    for col in range(0,len(edges[0])-1,2):
        line(img,int(edges[0][col]),int(edges[1][col]),int(edges[0][col+1]),int(edges[1][col+1]),color[:])

def translate(dx,dy,dz):
    M=I(4)
    M[0][3]=dx
    M[1][3]=dy
    M[2][3]=dz
    return M

def scale(dx,dy,dz):
    M=I(4)
    M[0][0]=dx
    M[1][1]=dy
    M[2][2]=dz
    return M

def rotate(axis,theta):
    theta=math.radians(theta)
    M=I(4)
    if axis=="x":
        M[1][1]=math.cos(theta)
        M[1][2]=-math.sin(theta)
        M[2][1]=math.sin(theta)
        M[2][2]=math.cos(theta)
    elif axis=="y":
        M[2][2]=math.cos(theta)
        M[2][0]=-math.sin(theta)
        M[0][2]=math.sin(theta)
        M[0][0]=math.cos(theta)
    elif axis=="z":
        M[0][0]=math.cos(theta)
        M[0][1]=-math.sin(theta)
        M[1][0]=math.sin(theta)
        M[1][1]=math.cos(theta)
    return M

def circle(edges,cx,cy,cz,r,step=0.01):
    prevX=cx+r*math.cos(0)
    prevY=cy+r*math.sin(0)
    t=step
    while t<=1:
        x=cx+r*math.cos(t*2*math.pi)
        y=cy+r*math.sin(t*2*math.pi)
        addEdge(edges,prevX,prevY,cz,x,y,cz)
        prevX=x
        prevY=y
        t+=step

def hermite(edges,x0,y0,x1,y1,rx0,ry0,rx1,ry1,step=0.01):
    given=[[x0,y0],[x1,y1],[rx0,ry0],[rx1,ry1]]
    M=[[2,-2,1,1],[-3,3,-2,-1],[0,0,1,0],[1,0,0,0]]
    coeffs=multMatrix(M,given)
    t=step
    prevX=x0
    prevY=y0
    while t<=1:
        tMat=[[t*t*t,t*t,t,1]]
        point=multMatrix(tMat,coeffs)
        addEdge(edges,prevX,prevY,0,point[0][0],point[0][1],0)
        prevX=point[0][0]
        prevY=point[0][1]
        t+=step

def bezier(edges,x0,y0,x1,y1,x2,y2,x3,y3,step=0.01):
    given=[[x0,y0],[x1,y1],[x2,y2],[x3,y3]]
    M=[[-1,3,-3,1],[3,-6,3,0],[-3,3,0,0],[1,0,0,0]]
    coeffs=multMatrix(M,given)
    t=step
    prevX=x0
    prevY=y0
    while t<=1:
        tMat=[[t*t*t,t*t,t,1]]
        point=multMatrix(tMat,coeffs)
        addEdge(edges,prevX,prevY,0,point[0][0],point[0][1],0)
        prevX=point[0][0]
        prevY=point[0][1]
        t+=step



    
