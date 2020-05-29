from vpython import *


small_size = 4
large_size = 5
L = 3

press_indicator = label(pos = vector(1.5 * small_size, 2.5 * small_size, 0))
press_indicator.text = "Choose magnet location"
top=sphere(pos=vector(0,0,0), radius=0.01)

chooser = box(pos = vector(2.2 * small_size,1.2 * small_size, 0), size = vector(2 * small_size, 2 * small_size, 0.1), color = color.green)
color_indicator = box(pos = vector(0.8 * small_size, 1.2 * small_size, 0), size = vector(1, 1, 0.1), color = color.blue)

theta=30*pi/180

wall = box(pos = vector(0,-1 * (L + 0.5), 0), size = vector(2 * large_size, 0.1, 2 * large_size), color = color.green)
balls = []
balls.append(sphere(pos=L*vector(sin(theta), -cos(theta),0.05), radius=0.3, color=color.cyan))
balls[0].p = vector(0,0,0)
balls[0].m = .05
springs = []
springs.append(cylinder(pos=top.pos, axis=(balls[0].pos-top.pos), radius=0.05))

g_force = 9.8 * balls[0].m
g =vector(0,-1 * g_force,0)

max_factor = 3
factor = 0.2
k=500
t=0
dt=0.001

start_y = 1.4 * small_size
x_c = -2 * small_size
mag_force_text = label(pos = vector(x_c,start_y, 0), height = 12)
mag_force_text.text = "Net Magnetic force (in terms of g's): "
width = 4 * small_size
mag_line = box(pos = vector(x_c, start_y - 0.3 * large_size, 0), size = vector(width, 0.2 , 0.1 ), color = color.white)
mag_indicator = box(pos = vector(x_c + (factor - 0.5) * width, start_y - 0.3 * large_size, 0), size = vector (0.4, 1.0, 0.1), color = color.blue)
start_x = -0.5 * width
end_x = 0.5 * width
while(start_x <= end_x):
  number = round(max_factor * (start_x/(width) + 0.5),1)
  text_indicator = label(pos = vector(x_c + start_x, start_y - 0.5 * large_size, 0), height = 8)
  text_indicator.text = str(number)
  start_x += 0.1 * width
  
magnets = [ ]

def keyInput(evt):
  string = str(evt.key).lower()
  if 'c' in string:
    if(color_indicator.color == color.blue):
      color_indicator.color = color.red #Negative
    else:
      color_indicator.color = color.blue #Positive
  if 'r' in string:
    color_indicator.color = color.green
    press_indicator.text = "Choose magnet to remove"
  if 'q' in string:
    color_indicator.color = color.cyan

def get_distance(vector_1, vector_2):
  dif = vector_1 - vector_2
  return dif.mag

def remove_magnet(to_remove):
  end = -1
  distance = 1000
  for index in range(len(magnets)):
    current = get_distance(to_remove, magnets[index][0].pos)
    if(current <= distance):
      end = index
      distance = current
  if(end >= 0):
    magnet_data = magnets.pop(end)
    magnet_data[0].visible = False
    magnet_data[1].visible = False
    press_indicator.text = "Removed magnet from " + str(magnet_data[0].pos)
    del magnet_data[0]
    del magnet_data[1]
rep_size = 0.2

def adjust_factor(position):
  global factor
  x_coord = position.x - x_c
  if(abs(x_coord) < width/2):
    factor = round(max_factor * (0.5 + x_coord/width), 3)
    press_indicator.text = "Set factor to " + str(factor)
    mag_indicator.pos.x = position.x

def mousePress(evt):
  position = evt.pos
  press_indicator.text = str(position)
  if(position.x < 1.0):
    adjust_factor(position)
    return None
  delta_x = (position.x - chooser.pos.x)/small_size
  delta_z = (chooser.pos.y - position.y)/small_size
  if (abs(delta_x) > 1 or abs(delta_z) > 1):
    press_indicator.text = "Invalid position"
    return None 
  ball_x = delta_x * large_size
  ball_z = delta_z * large_size
  ball_y = -1 * (L + 0.3)
  if (color_indicator.color == color.green):
    remove_magnet(vector(ball_x, ball_y, ball_z))
    return None
  sign = 1
  if(color_indicator.color == color.red):
    sign = -1
  magnet = sphere(pos = vector(ball_x, ball_y, ball_z), radius = 0.2, color = color_indicator.color)
  representation = sphere(pos = vector(position.x, position.y, rep_size), radius = rep_size, color = color_indicator.color)
  data = [magnet, representation, sign]
  magnets.append(data)
  press_indicator.text = "Added magnet to " + str(magnet.pos)
  
def get_unit_magnet_direction(ball):
  net = vector(0, 0, 0)
  for magnet_data in magnets:
    temp = magnet_data[2] * (norm(balls[0].pos - magnet_data[0].pos))/(mag(balls[0].pos - magnet_data[0].pos) ** 3)
    net += temp
  return net

scene.bind('keydown', keyInput)
scene.bind('click', mousePress)

while (color_indicator.color != color.cyan):
  if(len(balls) > 0 and len(springs) > 0):
    rate(1000)
    r=balls[0].pos-top.pos
    magnetic_force = g_force * factor
    forcemag_current = get_unit_magnet_direction(balls[0]) * magnetic_force
    F= g + k*(L-mag(r))*norm(r) + forcemag_current  
    balls[0].p=balls[0].p+F*dt
    balls[0].pos=balls[0].pos+balls[0].p*dt/balls[0].m
    springs[0].axis=balls[0].pos - top.pos
    t=t+dt

print("Ended program")
