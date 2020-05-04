import socket
import base64
import matplotlib.image as mpimg
import numpy as np

#############
# ALGORITHM #
#############

def color_id(colors, c):
	""" Map color code to color id """
	if np.array_equal(c, [0, 0, 0]): # black
		return -2
	if np.array_equal(c, [1, 1, 1]): # white
		return -1
	for i, color in enumerate(colors):
		if np.array_equal(c, color):
			return i


def get_color(img, i, j):
	""" Get the color of cell (i, j) """
	return img[i*64+32][j*64+32]


def coord_init(img):
	""" Find the position of beginning and end of the maze """
	h, w = img.shape[0]//64, img.shape[1]//64
	for j in range(2, w-2):
		if img[(h-2)*64+10][j*64+22][0] == 0:
			col_out = j - 2
		elif img[(h-2)*64+30][j*64+22][0] == 0:
			col_in = j - 2
	return col_in, col_out


def find_color_order(img):
	""" Return the available colors in the right order """
	h, w = img.shape[0]//64, img.shape[1]//64
	colors = []
	j = 2
	color = get_color(img, 1, j)
	while not np.array_equal(color, [1, 1, 1]):
		colors.append(color)
		j += 2
		color = get_color(img, 1, j)
	return colors


def make_maze(img):
	""" Construct maze from image data """
	h, w = img.shape[0]//64, img.shape[1]//64
	maze_h, maze_w = h-5, w-4
	maze = [[0]*(maze_w) for i in range(maze_h)]
	colors = find_color_order(img) # WHITE: -1 // BLACK: -2
	for i in range(maze_h-1):
		for j in range(maze_w):
			maze[i][j] = color_id(colors, get_color(img, i+4, j+2))
	col_in, col_out = coord_init(img)
	for j in range(maze_w):
		if j == col_in or j == col_out:
			maze[-1][j] = -1
		else:
			maze[-1][j] = -2
	return maze, col_in, col_out, len(colors)


def flood_fill(maze, i, j, c, visited, prec, nb_colors):
	""" Path finding algorithm """
	maze_h, maze_w = len(maze), len(maze[0])
	visited[i][j][c] = True
	for di, dj in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
		if 0 <= i+di < maze_h and 0 <= j+dj < maze_w:
			new_color = maze[i+di][j+dj]
			if new_color == -1:
				if not visited[i+di][j+dj][c]:
					prec[i+di][j+dj][c] = (i, j, c)
					flood_fill(maze, i+di, j+dj, c, visited, prec, nb_colors)
			elif new_color == c:
				if not visited[i+2*di][j+2*dj][(c+1)%nb_colors]:
					prec[i+2*di][j+2*dj][(c+1)%nb_colors] = (i, j, c)
					flood_fill(maze, i+2*di, j+2*dj, (c+1)%nb_colors, visited, prec, nb_colors)


def find_path(maze, col_in, col_out, nb_colors):
	""" Main function """
	maze_h, maze_w = len(maze), len(maze[0])
	visited = [[[False]*nb_colors for j in range(maze_w)] for i in range(maze_h)]
	prec = [[[0]*nb_colors for j in range(maze_w)] for i in range(maze_h)]
	color_in = maze[maze_h-2][col_in]
	color_out = maze[maze_h-2][col_out]

	flood_fill(maze, maze_h-1, col_in, color_in, visited, prec, nb_colors)

	i, j = maze_h-1, col_out
	c = (color_out+1)%nb_colors
	path = []
	while (i, j) != (maze_h-1, col_in):
		(i2, j2, c2) = prec[i][j][c]
		if i2 > i:
			path.append('N')
		elif i2 < i:
			path.append('S')
		elif j2 > j:
			path.append('W')
		else:
			path.append('E')
		(i, j, c) = (i2, j2, c2)

	return "".join(reversed(path))



##############
# CONNECTION #
##############

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("challenges2.france-cybersecurity-challenge.fr", 6002))

rep = sock.recv(4000)
msg = rep
while rep.find(b"Press a key when you are ready...") == -1:
	rep = sock.recv(4000)
	msg += rep
sock.sendall(b"\n")

for i in range(100): # assuming there are less than 100 mazes
	rep = sock.recv(4000)
	msg = rep
	print(msg.decode("utf-8")) # so that we get the flag at the end :)
	while rep.find(b"Now enter your solution:") == -1:
		rep = sock.recv(4000)
		msg += rep
	
	img_begin = msg.find(b"------------------------ BEGIN MAZE ------------------------") + 60
	img_end = msg.find(b"------------------------- END MAZE -------------------------")
	
	g = open("out" + str(i) + ".png", "wb")
	g.write(base64.decodestring(msg[img_begin:img_end]))
	g.close()
	
	img = mpimg.imread("out" + str(i) + ".png")

	res = find_path(*make_maze(img)) + '\n'
	print(res)
	sock.sendall(res.encode("utf-8"))
