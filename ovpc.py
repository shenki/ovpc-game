#!/usr/bin/env python

import sys
sys.path.insert(0, '.')

import pyglet

from pyglet.window import key
from random import randrange, random
import math
import time
import glob
from pyglet.gl import *

window = pyglet.window.Window(800, 400, caption='OVPC')
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

batch = pyglet.graphics.Batch()

pyglet.resource.path = ['res']
pyglet.resource.reindex()

window.set_icon(pyglet.resource.image("ovpc.png"))

child_death_files = glob.glob1("res", "child-death[012]*.png")
child_death_files.sort()
child_death = pyglet.image.Animation.from_image_sequence(
	[pyglet.resource.image(x) for x in child_death_files],
	0.1, False)

raptor_anim_files = glob.glob1("res", "raptor[123].png")
raptor_anim_files.sort()
raptor_anim = pyglet.image.Animation.from_image_sequence(
	[pyglet.resource.image(x) for x in raptor_anim_files],
	0.1, True)

pack = []
child = pyglet.sprite.Sprite(pyglet.resource.image('child.png'), batch=batch)

score = 0

t = pyglet.text.Label("Score: %.1f" % score, color=(255,0,0,255), batch=batch, font_size=16)
t.x = 10
t.y = window.height-40

def update(dt):
	global child, score, t

	t.begin_update()
	if type(score) in (int, float, long):
		if len(pack)-2 < score:
			pack.append(pyglet.sprite.Sprite(raptor_anim, batch=batch))
			reset_enemy(pack[-1])

		score += dt
		t.text = "Score: %.1f" % score
	else:
		t.text = score
	t.end_update()


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

	for i, raptor in enumerate(pack):
		if raptor.x < (0 - raptor.width):
			reset_enemy(raptor)

		raptor.x -= dt * 150
		raptor.y += dt * randrange(-100, 100)

		if raptor.x < child.x:
			continue

		if raptor.y+raptor.height*0.5 < child.y:
			continue

		if raptor.y-raptor.height*0.5 > child.y+child.height*0.5:
			continue

		if (raptor.x-child.x) < (child.width+raptor.width)*0.5-10:
			raptor.x += dt * 150

			if child.image is child_death:
				continue

			score = "You died! Score: %.1f" % score
			child.image = child_death

@window.event
def on_draw():
	window.clear()
	glClearColor(1,1,1,1)
	batch.draw()

def reset_enemy(raptor):
	raptor.scale = 0.5
	raptor.x = window.width + randrange(0,window.width*2)
	raptor.y = window.height * random()

child.scale = 0.5
pyglet.clock.schedule(update)
pyglet.app.run()
