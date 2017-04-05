#!/usr/bin/env python

import argparse
import sys
import functools, operator
import Image

import glob
import numpy as np

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

def Square():
    glBegin(GL_QUADS)
    for vertex in verticies[0:4]:
        glVertex3fv(vertex)
    glEnd()


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def Sphere(r):
    glutSolidSphere(r,10,10)

def Cube2():
    glutSolidCube(1)

def init():
    glShadeModel(GL_SMOOTH) 
    #glEnable(GL_CULL_FACE)
    #glEnable(GL_DEPTH_TEST)
    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)


    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, [0.,0.,0.,1.])
    #gluLookAt(0,0,-10,
    #    0,0,0,
    #    0,1,0)

def screenshot(filename):
	width = 800
	height = 600
	glReadBuffer(GL_FRONT)
	pixels = glReadPixels(0,0,width,height,GL_RGB,GL_UNSIGNED_BYTE)
	
	image = Image.fromstring("RGB", (width, height), pixels)
	image = image.transpose( Image.FLIP_TOP_BOTTOM)
	image.save(filename)

def main(args):

    glutInit()

    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    init()

    f = 0

    gluPerspective(45, (display[0]/display[1]), 0.1, 5000.0)

    while True:
        for event in pygame.event.get():
	    if event.type == pygame.KEYDOWN:
		print event.key
		if event.key == 27:
                    pygame.quit()
                    quit()
		elif event.key == 44:
		    interval = max(interval - 1, 1)
		    pass
		elif event.key == 46:
                    pass
             
	    elif event.type == pygame.MOUSEBUTTONDOWN:
                print event.button
                if event.button == 4: # wheel up
		    pass
                elif event.button == 5: # wheel down
                    pass
     	    elif event.type == pygame.QUIT:
                pygame.quit()
                quit()


	#print t
	
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #glMatrixMode(GL_MODELVIEW)
	#glLoadIdentity()

	eye = np.array([0,0,-10])
	center = np.array([0,0,0])
	
        glPushMatrix()
	gluLookAt(eye[0], eye[1], eye[2],
              center[0],center[1],center[2],
              0,1,0)

	#print frame.bodies[0].x

        glPushMatrix()
        #draw_frame(frame)
	Square()

        glPopMatrix()
        glPopMatrix()

        pygame.display.flip()

	if args.capture:
            screenshot("capture/frame_{}.png".format(f))
            f += 1

        pygame.time.wait(10)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("--capture", action="store_true")
	args = parser.parse_args()	

	
	main(args)






