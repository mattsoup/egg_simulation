"""
A Processing (python mode) script to draw a heatmap from the output of
'egg_simulation.py'
"""

add_library('pdf')

# 'beginRecord' will make the pdf output, and 'file' is the input from the
# output of 'egg_simulation.py'.
beginRecord(PDF, "tetchi_min50.pdf")
file = loadStrings("/scratch/1/matt/egg_simulation/tetchi_min50.out")
size(700,600)
background(255)

# The below variables determine how many columns and rows will be in the
# heatmap
num_hodg = 6 # number of hodgkinia lineages
num_cells = 15000 # max number of cells passed on
cell_sampling = 20 # sampling of number of cells -- i.e. every cell sampled, every 10, 20, etc.

# Variables to place the heatmap, size it, etc.
actual_cells = num_cells / cell_sampling
x_start = 100
y_start = 550
total_height = 500
total_width = 500
x_width = float(total_width) / num_hodg
y_height = float(total_height) / (actual_cells)

noStroke()
strokeCap(SQUARE)
# Sets the color of the heatmap
color_0 = 0xFF000000
color_50 = 0xFF2499aa # the main color for the heatmap
color_100 = 0xFFFFFFFF

# Goes through the input file and draws a rectangle corresponding to the
# number of Hodkginia lineages, number of cells, and proporton of viable eggs.
for item in file:
    temp = item.split(" ")
    x_coord = (int(temp[0]) - 1) * x_width
    y_coord = int(((int(temp[1]) * y_height) / (cell_sampling)) + y_height)
    #print y_coord, y_height
    viable = float(temp[2])
    if viable <= 0.5:
        fill_color = lerpColor(color_0, color_50, viable / 0.5)
        fill(fill_color)
        stroke(fill_color)
        rect(x_start + x_coord, y_start - y_coord, x_width, y_height)
    elif viable > 0.5 and viable < 0.98:
        fill_color = lerpColor(color_50, color_100, (viable - 0.5) / 0.5)
        fill(fill_color)
        stroke(fill_color)
        rect(x_start + x_coord, y_start - y_coord, x_width, y_height)

noFill()
stroke(180)
# Draws a box around the heatmap, with tick bars on the bottom.
rect(x_start, y_start - total_height, total_width, total_height)
x_interval = total_width / 5
prev_start = x_interval
for x in range(0, 4):
    line(x_start + prev_start, y_start, x_start + prev_start, y_start + 5)
    prev_start += x_interval

# Writes the number of Hodgkinia lineages along the x-axis
textAlign(CENTER, CENTER)
hodg_text_interval = total_width / 5
hodg_text_scalar = num_hodg / 5
prev_start = hodg_text_interval
for x in range(1, 6):
    fill(0)
    text("%s" % (x * hodg_text_scalar), x_start + prev_start, y_start + 10)
    prev_start += hodg_text_interval

# Draws tick marks along the left side
y_interval = total_height / 5
prev_start = y_interval
for y in range(0, 4):
    line(x_start, y_start - prev_start, x_start - 5, y_start - prev_start)
    line(x_start + total_width + 30, y_start - prev_start, x_start + total_width + 33, y_start - prev_start)
    prev_start += y_interval

# Writes the number of cells along the y-axis.
textAlign(RIGHT, CENTER)
cell_text_interval = total_height / 5
cell_text_scalar = num_cells / 5
prev_start = cell_text_interval
for y in range(1, 6):
    text ("%s" % (y * cell_text_scalar), x_start - 10, y_start - prev_start)
    prev_start += cell_text_interval

# Writes the percents along what will be the scale bar
textAlign(LEFT, CENTER)
percent_text_interval = total_height / 5
percent_text_scalar = 100 / 5
prev_start = 0
for y in range(0, 6):
    text("%s" % (y * percent_text_scalar), x_start + total_width + 40, y_start - prev_start)
    prev_start += percent_text_interval

# Draws the scale bar on the right
strokeWeight(1.5)
for y in range(1, total_height / 2):
    inter = float(y) / (total_height / 2)
    stroke_color = lerpColor(color_0, color_50, inter)
    stroke(stroke_color)
    line(x_start + total_width + 10, y_start - y, x_start + total_width + 30, y_start - y)
for y in range(0, total_height / 2):
    inter = float(y) / (total_height / 2)
    stroke_color = lerpColor(color_50, color_100, inter)
    stroke(stroke_color)
    line(x_start + total_width + 10, y_start - y - (total_height / 2), x_start + total_width + 30, y_start - y - (total_height / 2))


# Labels the axes
textAlign(CENTER, CENTER)
textSize(18)
text("Number of Hodgkinia lineages", x_start + total_width / 2, y_start + 30)
pushMatrix()
translate(x_start - 60, y_start - (total_height / 2))
rotate(-HALF_PI)
text("Number of Hodgkinia cells passed on to each egg", 0, 0)
text("Percent of eggs receiving all Hodgkinia lineages", 0, 0 + 60 + total_width + 70)
popMatrix()

strokeWeight(1)
stroke(180)
noFill()
rect(x_start + total_width + 10, y_start - total_height, 20, total_height)

endRecord()
