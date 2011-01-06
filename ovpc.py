#!/usr/bin/env python
#
#    One Velociraptor per Child
#
#    Copyright 2009 Joel Stanley <joel@jms.id.au>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

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

raptor_static = pyglet.resource.image('raptor1.png')

pack = []
child = pyglet.sprite.Sprite(pyglet.resource.image('child.png'), batch=batch)

raptor_eating = -1

@child.event
def on_animation_end():
	global pack, raptor_eating
	if raptor_eating != -1:
		pack[raptor_eating].image = raptor_anim
		raptor_eating = -1

score = 0

t = pyglet.text.Label("Score: %.1f" % score, color=(255,0,0,255), batch=batch, font_size=16)
t.x = 10
t.y = window.height-40

def update(dt):
	global child, raptor_eating, score, t

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

	if keys[key.ENTER] and child.image is child_death:
		score = 0
		child.image = pyglet.resource.image('child.png')
		child.x = child.y = 0
		if raptor_eating != -1:
			pack[raptor_eating].image = raptor_anim
			raptor_eating = -1

	if keys[key.UP] and child.image is not child_death:
		child.y += dt * 100
	if keys[key.DOWN] and child.image is not child_death:
		child.y -= dt * 100
	if keys[key.LEFT] and child.image is not child_death:
		child.x -= dt * 100
	if keys[key.RIGHT] and child.image is not child_death:
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
			if raptor_eating == i:
				raptor.x += dt * 150

			if child.image is child_death:
				continue

			score = "You died! Score: %.1f" % score
			child.image = child_death
			raptor.image = raptor_static
			raptor_eating = i


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
