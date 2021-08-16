from PIL import Image
import random
from opensimplex import OpenSimplex

def save_rgb(rgb_data, width, height, filename):
    """Saves an a 3D list with RGB data as a png"""
    # Converting RGB list into something pillow can use to save an image.
    colors = bytes(rgb_data)
    img = Image.frombytes('RGB', (width, height), colors)
    img.save(f'{filename}.png')
    # Letting user know the image is saved.
    print(f'{filename}.png Saved')

def process_array(input_array, filename, color_key):
    """Processes 2D array to RGB data."""
    colors = []
    width = len(input_array[0])
    height = len(input_array)
    # Goes through 2D array and process it into RGB values.
    for Y in range(height):
        for X in range(width):
            #if input_array[X][Y] > 255:
            #    input_array[X][Y] = 255
            #elif input_array[X][Y] < 0:
            #    input_array[X][Y] = 0

            colors.extend(color_key[input_array[X][Y]])
    # Passing RGB values to save function
    save_rgb(colors, width, height, filename)

def scale(Noise, Width, Height):
    '''Scales an array up.'''
    temp_Noise = []
    Ori_Width = len(Noise[0]) / Width
    Ori_Height = len(Noise) / Height

    for Y in range(Height):
        temp_Noise.append([])
        for X in range(Width):
            Noise_Val = Noise[int(X * Ori_Width)][int(Y * Ori_Height)]
            temp_Noise[Y].append(Noise_Val)
    return temp_Noise

def stalagmite(x, y, type, do_not_override):
    '''Generates a stalagmite with a base at x, y'''
    global WIDTH, HEIGHT, Stalagmite_Min_Len, Stalagmite_Max_Len, Stalagmite_Chance
    # Length of Stalagmite
    stal_len = random.randint(Stalagmite_Min_Len, Stalagmite_Max_Len)
    # Stalagmite Base
    stal_base = stal_len // 2
    stal_side = random.randint(0, 1)
    # Stalagmite Generation
    for length in range(stal_len):
        if (x - stal_len - 1 >= 0) and (x - stal_len - 1 < HEIGHT):
            if Temp_Noise[x - length - 1][y] != do_not_override:
                Temp_Noise[x - length - 1][y] = type
            # Stalagmite Base Generation
            if length < stal_base:
                # Bounds Check and side of Stalagmite to generate base on.
                if stal_side == 0 and y + 1 < WIDTH and x + length + 1 < HEIGHT:
                    if Temp_Noise[x + length + 1][y + 1] != do_not_override:
                        Temp_Noise[x + length + 1][y + 1] = type
                    if Temp_Noise[x][y + 1] != do_not_override:
                        Temp_Noise[x][y + 1] = type  # Prevents hanging edges
                elif Y - 1 >= 0 and x + length + 1 < HEIGHT:
                    if Temp_Noise[x + length + 1][y - 1] != do_not_override:
                        Temp_Noise[x + length + 1][y - 1] = type
                    if Temp_Noise[x][y - 1] != do_not_override:
                        Temp_Noise[x][y - 1] = type  # Prevents hanging edges

def stalactite(x, y, type, do_not_override):
    '''Generates a stalactite with a base at x, y'''
    global Stalactite_Min_Len, Stalactite_Max_Len, Stalactite_Chance
    # Length of Stalactite
    stal_len = random.randint(Stalactite_Min_Len, Stalactite_Max_Len)
    # Stalactite Base
    stal_base = stal_len // 2
    stal_side = random.randint(0, 1)
    # Stalactite Generation
    for length in range(stal_len):
        if (x + stal_len + 1 >= 0) and (x + stal_len + 1 < HEIGHT):
            if Temp_Noise[x + length + 1][y] != do_not_override:
                Temp_Noise[x + length + 1][y] = type
            # Base Generation
            if length < stal_base:
                # Bounds Check and side of Stalactite to generate base on.
                if stal_side == 0 and y + 1 < WIDTH:
                    if Temp_Noise[x + length + 1][y + 1] != do_not_override:
                        Temp_Noise[x + length + 1][y + 1] = type
                    if Temp_Noise[x][y + 1] != do_not_override:
                        Temp_Noise[x][y + 1] = type  # Prevents hanging edges
                elif Y - 1 >= 0:
                    if Temp_Noise[x + length + 1][y - 1] != do_not_override:
                        Temp_Noise[x + length + 1][y - 1] = type
                    if Temp_Noise[x][y - 1] != do_not_override:
                        Temp_Noise[x][y - 1] = type  # Prevents hanging edges

def cell_check(x, y, crystal_formation):
    '''Generates BG edges, and Stalagmites/Stalactites'''
    global Noise, WIDTH, HEIGHT, Radius, BG_Gradient, BG_Wall
    if crystal_formation:
        type = 0
        if Noise[x][y] == 2:
            type = 2
        elif Noise[x][y] >= BG_Wall:
            type = 1
        if type != 0:
            # Stalagmite
            if X - 1 < HEIGHT and random.randint(0, 100) > 100 - Stalagmite_Chance:
                if type == 1:
                    if Noise[X - 1][Y] >= BG_Wall:
                        stalagmite(x, y, type, 2)
                elif Noise[X - 1][Y] != type:
                    stalagmite(x, y, type, 2)
            # Stalactite
            elif X + 1 < HEIGHT and random.randint(0,100) > 100 - Stalactite_Chance:
                if type == 1:
                    if Noise[X + 1][Y] >= BG_Wall:
                        stalactite(x, y, type, 2)
                elif Noise[X + 1][Y] != type:
                    stalactite(x, y, type, 2)
    else:
        # Background Border along Foreground Tiles
        for y_dis in range(Radius * 2 + 1):
            for x_dis in range(Radius * 2 + 1):
                x_val = x - Radius + x_dis
                y_val = y - Radius + y_dis
                if not (x_val < 0 or x_val >= WIDTH or y_val < 0 or y_val >= HEIGHT) and Noise[x_val][y_val] == 2:
                    return BG_Gradient
        return 0

# Image Colors.
Color_Key = {
    0 : [128,255,255], # Sky
    1 : [219,112,147], # Background
    2 : [199,21,133] # Foreground
}

random.seed(100)

WIDTH = 256
HEIGHT = 256
Noise = []
# Simplex Variables
FG_Wall = 0
BG_Wall = 0
FG_Scale = 25
BG_Scale = 20
# Background edges on Foreground Walls
BG_Gradient = 0.3
Radius = 2
# Stalactite, Stalagmites
Stalagmite_Min_Len = 1
Stalagmite_Max_Len = 4
Stalagmite_Chance = 15
Stalactite_Min_Len = 1
Stalactite_Max_Len = 7
Stalactite_Chance = 15
# Simplex
tmp = OpenSimplex(random.randint(0,100000))
# Foreground
for Y in range(HEIGHT):
    Noise.append([])
    for X in range(WIDTH):
        temp = tmp.noise2d(X/FG_Scale, Y/FG_Scale)
        if temp < FG_Wall:
            Noise[Y].append(2)
        else:
            Noise[Y].append(-1)
# Background
for Y in range(HEIGHT):
    for X in range(WIDTH):
        if Noise[X][Y] != 2:
            temp = tmp.noise2d(X/BG_Scale, Y/BG_Scale)
            if temp + cell_check(X, Y, False) > 1:
                Noise[X][Y] = 1
            elif temp + cell_check(X, Y, False) > 2:
                Noise[X][Y] = 2
            else:
                Noise[X][Y] = temp + cell_check(X, Y, False)


# Stalagmites and Stalactites.
Temp_Noise = list(map(list, Noise))
for Y in range(HEIGHT):
    for X in range(WIDTH):
        cell_check(X, Y, True)
Noise = Temp_Noise

# Process to color_key values
for Y in range(HEIGHT):
    for X in range(WIDTH):
        if Noise[X][Y] == 2:
            Noise[X][Y] = 2 # Foreground
        elif Noise[X][Y] < BG_Wall:
            Noise[X][Y] = 0 # Sky
        else:
            Noise[X][Y] = 1 # Background

Noise = scale(Noise, 512, 512)

process_array(Noise, "Crystal Caves", Color_Key)