#!/usr/bin/env python

import pyglet
from pyglet.window import key

window = pyglet.window.Window(caption='OVPC')

batch = pyglet.graphics.Batch()

raptor = pyglet.sprite.Sprite(pyglet.resource.image('raptor.png'), batch=batch)
child = pyglet.sprite.Sprite(pyglet.resource.image('child.png'), batch=batch)

@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.UP:
		pass
	elif symbol == key.DOWN:
		pass
	elif symbol == key.LEFT:
		pass
	elif symbol == key.RIGHT:
		pass
	elif symbol == key.ESCAPE:
		import sys
		sys.exit(0)

@window.event
def on_draw():
	window.clear()
	batch.draw()

pyglet.app.run()
