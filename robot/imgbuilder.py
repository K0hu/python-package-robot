from PIL import Image

def img_grid(grid, img):
    f = Image.open(img).convert("RGB")
    width, height = f.size

    activation_values = []

    brightness_threshold = 128


    for y in range(height):
        for x in range(width):
            r, g, b = f.getpixel((x, y))
            brightness = (r + g + b) // 3
            activation = brightness > brightness_threshold
            activation = str(activation)
            activation_values.append(activation)
    row = []
    liste = []
    for _ in range(0, height):
        liste.append(activation_values[:width])
        del activation_values[:width]
        
    def ausgabe(img):
        for i in range(0, len(img)):
            for i2 in range(0, len(img[i])):
                img[i][i2] = str(img[i][i2])

        for i in range(0, len(img)):
            print(' '.join(img[i]))  

    for y in range(0, len(liste)):
        for x in range(0, len(liste[y])):
            if liste[y][x] == 'False':
                liste[y][x] = '#'
                grid.walls.append([y, x])
            elif liste[y][x] == 'True':
                liste[y][x] = '.'
        
    grid.grid = liste
    grid.width = width
    grid.height = height
