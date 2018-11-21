from tkinter import *
import math
import random
import threading
import time
import copy


class Game:
	def __init__(self):
		# Game Class init
		self.tk = Tk()
		self.tk.title("Just Pixel")
		self.tk.resizable(0, 0)
		self.dead = False

		# Drawing canvas for game
		self.canvas = Canvas(self.tk, width=600, height=600, bd=10, relief=SUNKEN)
		self.canvas.pack()

		# Game player model components
		self.gravdir = "Down"
		self.player = self.canvas.create_rectangle(280, 560, 320, 600, fill="Green", outline="black")
		self.playerXv = 0
		self.playerYv = 0
		self.points = 0
		self.pointsd = self.canvas.create_text(300, 30, text="Points: 0", font=("Helvetica", 20, "bold"))
		self.playerMovingSide = None
		self.playerJumped = False
		self.playerSmashed = False

		# Game dands model components
		self.dands = []

		# Game difficulty data
		self.difficulty = 1

		# Dands generation
		self.dandgenerating = threading.Thread(target=self.dandGenerate)
		self.dandgenerating.daemon = True
		self.dandgenerating.start()

		# Key handling
		self.tk.bind_all("<KeyPress>", self.keyHandlePress)
		self.tk.bind_all("<KeyRelease>", self.keyHandleRelease)

		# Start game loop
		self.tk.after(10, self.loop)
		self.tk.mainloop()

	def restartGame(self, clck):
		self.tk.destroy()

	def keyHandlePress(self, clck):
		# Handle keys
		if (clck.keysym == "Up") and (not self.playerJumped):
			self.playerYv = 12
			self.playerJumped = True

		if clck.keysym == "Left":
			self.playerMovingSide = "Left"

		if clck.keysym == "Right":
			self.playerMovingSide = "Right"

	def keyHandleRelease(self, clck):
		# Handle keys
		if clck.keysym == "Left":
			self.playerMovingSide = None

		if (clck.keysym == "Down") and (not self.playerSmashed) and (not (self.canvas.coords(self.player)[1] >= 550)):
			self.playerYv = -12
			self.playerSmashed = True

		if clck.keysym == "Right":
			self.playerMovingSide = None

	def loop(self):
		# Game loop

		# Display points
		self.canvas.itemconfig(self.pointsd, text="Points: " + str(self.points))

		# Render player
		self.canvas.move(self.player, self.playerXv, -self.playerYv)

		# Update player stats
		self.playerYv -= 0.3
		if self.playerMovingSide == "Left":
			self.playerXv -= 0.5
		if self.playerMovingSide == "Right":
			self.playerXv += 0.5

		# Add boundaries
		playerX = copy.copy(self.canvas.coords(self.player)[0])
		playerY = copy.copy(self.canvas.coords(self.player)[1])
		if playerX < 20:
			playerX = 20
			self.playerXv = -self.playerXv / 3
		if playerX > 560:
			playerX = 560
			self.playerXv = -self.playerXv / 3
		if playerY < 0:
			playerY = 0
			self.playerYv = -self.playerYv / 3
		if playerY > 560:
			playerY = 560
			if self.playerSmashed:
				self.playerYv = -self.playerYv / 1.5
			else:
				self.playerYv = -self.playerYv / 3
			self.playerJumped = False
			self.playerSmashed = False
		self.canvas.move(self.player, playerX - self.canvas.coords(self.player)[0], playerY - self.canvas.coords(self.player)[1])

		# Render dands and update dands
		for dand in self.dands:
			# Rendering dand
			self.canvas.move(dand["object"], dand["xvel"], -dand["yvel"])
			# Handle points and death
			pcoords = self.canvas.coords(self.player)
			if dand["object"] in self.canvas.find_overlapping(pcoords[0], pcoords[1], pcoords[2], pcoords[3]):
				self.tk.bell()
				if self.playerYv > 0 or self.playerSmashed:
					self.points += 1
					self.canvas.delete(dand["object"])
					self.dands.remove(dand)
					self.difficulty += 0.1
				else:
					self.dead = True
					self.canvas.create_text(300, 300, text="You died!\nTap to restart", font=("Helvetica", 20, "bold"))
					self.tk.bind_all("<Button-1>", self.restartGame)
					return
			dand["yvel"] -= 0.3

		self.tk.after(10, self.loop)

	def dandGenerate(self):
		while True:
			x, y = random.randint(40, 520), random.randint(20, 100)
			self.dands.append({
				"yvel": 0,
				"xvel": random.randint(-5, 5),
				"object": self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="Red", outline="black")
				})
			time.sleep(random.random() * (1 / self.difficulty))

if __name__ == '__main__':
	while True:
		game = Game()
		if not game.dead:
			break
