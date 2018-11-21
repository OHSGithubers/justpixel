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
		self.points = 0
		self.playerMovingSide = None
		self.playerJumped = False

		# Drawing canvas for game
		self.canvas = Canvas(self.tk, width=600, height=600, bd=10, relief=SUNKEN)
		self.canvas.pack()

		# Key handling
		self.tk.bind_all("<KeyPress>", self.keyHandlePress)
		self.tk.bind_all("<KeyRelease>", self.keyHandleRelease)

		# Start game loop
		self.tk.after(10, self.loop)
		self.tk.mainloop()

	def keyHandlePress(self, clck):
		# Handle keys
		if (clck.keysym == "Up") and (not self.playerJumped):
			print("ye")
			self.playerYv = 12
			self.playerJumped = True

		if clck.keysym == "Left":
			self.playerMovingSide = "Left"

		if clck.keysym == "Right":
			self.playerMovingSide = "Right"

	def keyHandleRelease(self, clck):
		# Handle keys
		if clck.keysym == "Left":
			self.playerXv -= 1
			self.playerMovingSide = None

		if clck.keysym == "Right":
			self.playerXv += 1
			self.playerMovingSide = None

	def loop(self):
		# Game loop
		self.canvas.delete("all")

		# Render player
		self.canvas.create_rectangle(self.playerX, self.playerY, self.playerX + 40, self.playerY + 40, fill="Green", outline="black")

		# Update player stats
		self.playerX += self.playerXv
		self.playerY -= self.playerYv
		self.playerYv -= 0.3
		if self.playerMovingSide == "Left":
			self.playerXv -= 0.5
		if self.playerMovingSide == "Right":
			self.playerXv += 0.5

		# Add boundaries
		if self.playerX < 20:
			self.playerX = 20
			self.playerXv = -self.playerXv / 5
		if self.playerX > 560:
			self.playerX = 560
			self.playerXv = -self.playerXv / 5
		if self.playerY < 0:
			self.playerY = 0
			self.playerYv = -self.playerYv / 5
		if self.playerY > 560:
			self.playerY = 560
			self.playerYv = -self.playerYv / 5
			self.playerJumped = False

		self.tk.after(10, self.loop)

if __name__ == '__main__':
	game = Game()
