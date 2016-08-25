import math
class Constants(object):
    def __init__(self):
        self.set_normal()
        self.scale16()
    def scale16(self):
        self.map_scale = 16.0
    
    def scale08(self):
        self.map_scale = 8.0
        
    def set_normal(self):
        self.dist = 980.0
        self.time = 1.80

    def set_overlight(self):
        self.dist = 2078.0
        self.time = 3.60

    def set_bftp(self):
        self.dist = 1171.0 # ?
        self.time = 2.0    # ?

constants = Constants()

def angle_hor(c1,c2):
  vec1 = (c2[0] - c1[0], c2[1] - c1[1])
  vec2 = (1,0) 

  dot = vec1[0]
  ab = math.sqrt(vec1[0]**2 + vec1[1]**2)
  if ab == 0:
    return 0
  costh = dot/float(ab)

  th = math.acos(costh)
  return math.degrees(th)

def angle_to_xy(x,y,s,t):
  v=v0 = f_v0(s,t)
  g = f_g(s,t)
  root_term = v**4 - g*(g*x**2 + 2*y*v**2)
  if root_term < 0:
    return False
  else:
    root = float(math.sqrt(root_term))


  try:
    th1 = (v**2 + root)/(g*x)
    th1 = math.atan(th1)
    ang1 = round(math.degrees(th1), 2)
  except ZeroDivisionError:
    ang1= 90
  try:
    th2 = (v**2 - root)/(g*x)
    th2 = math.atan(th2)
    ang2 = round(math.degrees(th2), 2)
  except ZeroDivisionError:
    ang2 = 90

  return abs(ang1),abs(ang2)

def f_v0(s,t):
	return (2.0*s)/t

def f_g(s,t):
	v0 = f_v0(s,t)
	return float(-v0)/t

