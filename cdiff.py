import math

'''
0.4124 0.3576 0.1805
0.2126 0.7152 0.0722
0.0193 0.1192 0.9505
'''
def rgb_to_srgb(rgb):
  (r,g,b) = rgb
  srgb = (r/255., g/255., b/255.)

  return srgb

def srgb_to_xyz(srgb):
  (r,g,b) = srgb
  X = 0.4124*r + 0.3576*g + 0.1805*b
  Y = 0.2126*r + 0.7152*g + 0.0722*b
  Z = 0.0193*r + 0.1192*g + 0.9505*b
  XYZ = (X,Y,Z)

  return XYZ

def xyz_to_lab(xyz):
  XYZn = (95.047, 100.000, 108.883) #D65
  def f(t):
    if t > (6/29.)**3.:
      r = t**(1/3.)
    else:
      r = (1/3.)*((29./6.)**2)*t + 4/29.
    return r

  Xn,Yn,Zn = XYZn
  X,Y,Z = xyz

  L = 116*f(Y/Yn) - 16
  a = 500*(f(X/Xn) - f(Y/Yn))
  b = 200*(f(Y/Yn) - f(Z/Zn))
  return (L,a,b)

def CIE76(lab1,lab2):
  L1,a1,b1 = lab1
  L2,a2,b2 = lab2

  return math.sqrt((L2-L1)**2 + (a2-a1)**2 + (b2-b1)**2)

def diff_rgb(rgb1,rgb2):
  srgb1 = rgb_to_srgb(rgb1)
  srgb2 = rgb_to_srgb(rgb2)

  xyz1 = srgb_to_xyz(srgb1)
  xyz2 = srgb_to_xyz(srgb2)

  lab1 = xyz_to_lab(xyz1)
  lab2 = xyz_to_lab(xyz2)

  cdiff = CIE76(lab1,lab2)

  return cdiff

