#!/usr/bin/env python

import pyglet
from pyglet.window import key
from random import random
import math

window = pyglet.window.Window(800, 400, caption='OVPC')
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

batch = pyglet.graphics.Batch()

raptor = pyglet.sprite.Sprite(pyglet.resource.image('raptor.png'), batch=batch)
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

	raptor.x -= dt * 100
	raptor.y += dt * random() * 10

@window.event
def on_draw():
	window.clear()
	batch.draw()

raptor.x = window.width
raptor.y = window.height * random()
pyglet.clock.schedule(update)
pyglet.app.run()
