import pygame

from pygame.locals import *




Resolution = 100



c = 0

b = 0

t = 0



ControlPoints = []

class ControlPoint:

    def __init__(self,pos):

        self.pos = pos


def DrawCurve():

    global t,b,c

    tans = []

    tand = []

    for x in xrange(len(ControlPoints)-2):

        tans.append([])

        tand.append([])



    cona = (1-t)*(1+b)*(1-c)*0.5

    conb = (1-t)*(1-b)*(1+c)*0.5

    conc = (1-t)*(1+b)*(1+c)*0.5

    cond = (1-t)*(1-b)*(1-c)*0.5



    i = 1

    while i < len(ControlPoints)-1:

        pa = ControlPoints[i-1]

        pb = ControlPoints[i]

        pc = ControlPoints[i+1]

                

        x1 = pb.pos[0] - pa.pos[0]

        y1 = pb.pos[1] - pa.pos[1]

        #z1 = pb.pos[2] - pa.pos[2]

        x2 = pc.pos[0] - pb.pos[0]

        y2 = pc.pos[1] - pb.pos[1]

        #z2 = pc.pos[2] - pb.pos[2]

                

        tans[i-1] = (cona*x1+conb*x2, cona*y1+conb*y2) #cona*z1+conb*z2

        tand[i-1] = (conc*x1+cond*x2, conc*y1+cond*y2) #conc*z1+cond*z2

        

        i += 1



    #render spline (Your camera part)

    t_inc = 0.1

    i = 1
    
    finalLines = []

    while i < len(ControlPoints)-2:

        p0 = ControlPoints[i]

        p1 = ControlPoints[i+1]

        m0 = tand[i-1]

        m1 = tans[i]

        #draw curve from p0 to p1

        Lines = [(p0.pos[0],p0.pos[1])]

        t_iter = t_inc

        while t_iter < 1.0:

            h00 = ( 2*(t_iter**3)) - ( 3*(t_iter**2)) + 1

            h10 = ( 1*(t_iter**3)) - ( 2*(t_iter**2)) + t_iter

            h01 = (-2*(t_iter**3)) + ( 3*(t_iter**2))

            h11 = ( 1*(t_iter**3)) - ( 1*(t_iter**2))

            px = h00*p0.pos[0] + h10*m0[0] + h01*p1.pos[0] + h11*m1[0]

            py = h00*p0.pos[1] + h10*m0[1] + h01*p1.pos[1] + h11*m1[1]

            #pz = h00*p0.pos[2] + h10*m0[2] + h01*p1.pos[2] + h11*m1[2]

            Lines.append((px,py))

            t_iter += t_inc

        Lines.append((p1.pos[0],p1.pos[1]))

        Lines2 = []

        for p in Lines:

            Lines2.append((int(round(p[0])),int(round(p[1]))))

        #pygame.draw.aalines(Surface,(255,255,255),False,Lines2)
        finalLines.append(Lines2)

        i += 1
    return finalLines
