#!/usr/bin/env python

import pyglet
from pyglet.window import key
from random import randrange, random
import math
from pyglet.gl import *

window = pyglet.window.Window(800, 400, caption='OVPC')
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

batch = pyglet.graphics.Batch()

raptors = [
		pyglet.sprite.Sprite(pyglet.resource.image('raptor.png'), batch=batch),
		pyglet.sprite.Sprite(pyglet.resource.image('raptor.png'), batch=batch),
		pyglet.sprite.Sprite(pyglet.resource.image('raptor.png'), batch=batch),
		pyglet.sprite.Sprite(pyglet.resource.image('raptor.png'), batch=batch),
		pyglet.sprite.Sprite(pyglet.resource.image('raptor.png'), batch=batch)]
child = pyglet.sprite.Sprite(pyglet.resource.image('child.png'), batch=batch)

def update(dt):
	if keys[key.ESCAPE]:
		import sys
		sys.exit(0)

	if keys[key.UP]:
		child.y += dt * 100
	if keys[key.DOWN]:
		child.y -= dt * 100
	if keys[key.LEFT]:
		child.x -= dt * 100
	if keys[key.RIGHT]:
		child.x += dt * 100

	if child.x > window.width:
		child.x = window.width
	if child.x < 0:
		child.x = 0

	if child.y > window.height - child.height:
		child.y = window.height - child.height
	if child.y < 0:
		child.y = 0

	for raptor in raptors:
		if raptor.x < (0 - raptor.width):
			reset_enemy(raptor)

		raptor.x -= dt * 100
		raptor.y += dt * randrange(-10, 10)

@window.event
def on_draw():
	window.clear()
	glClearColor(1,1,1,1)
	batch.draw()

def reset_enemy(raptor):
	raptor.x = window.width
	raptor.y = window.height * random()
	
for raptor in raptors:
	raptor.scale = 0.5
	reset_enemy(raptor)

child.scale = 0.5
pyglet.clock.schedule(update)
pyglet.app.run()
