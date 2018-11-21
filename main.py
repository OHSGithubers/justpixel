from tkinter import *
import math


class Game:
	def __init__(self):
		# Game Class init
		self.tk = Tk()

		# Game model components
		self.gravdir = "Down"
		self.playerX = 280
		self.playerY = 560
		self.playerXv = 0
		self.playerYv = 0

		# Drawing canvas for game
		self.canvas = Canvas(self.tk, width=600, height=600)
		self.canvas.pack()

		# Key handling
		self.tk.bind_all("<Key>", self.keyHandle)

		# Start game loop
		self.tk.after(10, self.loop)
		self.tk.mainloop()

	def keyHandle(self, clck):
		# Handle keys
		if clck.keysym == "Up":
			self.playerYv = 8

		if clck.keysym == "Left":
			self.playerXv -= 1

		if clck.keysym == "Right":
			self.playerXv += 1

	def loop(self):
		# Game loop
		self.canvas.delete("all")
		self.tk.after(10, self.loop)

if __name__ == '__main__':
	game = Game()
