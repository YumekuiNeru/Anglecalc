from PIL import Image
from sys import platform
import os
import time
import cdiff

try:
    from PIL import ImageGrab
except ImportError:
    pass

def screenshot_lin():
    """requires scrot for screenshots"""
    filepath = os.path.join('img', 'gwindowtemp.png')
    cmd = 'scrot ' + filepath
    os.system(cmd)
    time.sleep(0.1)

    img = Image.open(filepath)
    return img
                  
def screenshot(bbox=None):
    '''bbox: [x,y,w,h]'''
    if not os.path.exists('img'):
        os.mkdir('img')

 
    if platform == 'darwin' or platform.startswith('win'):
        img = ImageGrab.grab(bbox=bbox)
    elif platform.startswith('linux'):
        img = screenshot_lin()
        if bbox:
            img = img.crop(bbox)
    else:
        raise Exception('Unsupported platform')
    return img

def pixelloop(start,end,step=1):
  if type(start) is int: y0,x0 = start,start
  else: x0,y0 = start

  if type(end) is int: yn,xn = end,end
  else: xn,yn = end

  if type(step) is int: dy,dx = step,step
  else: dx,dy = step

  for h in range(y0,yn,dy):
    for w in range(x0,xn,dx):
      yield w,h

def eq(c1,c2,*args):
  return c1[:3] == c2[:3]

def cmp_c(mc,cx,maxdiff,d):
  mc = mc[:3]
  cx = cx[:3]
  key = (mc,cx)
  if key in d:
    diff = d[key]
  else:
    diff = cdiff.diff_rgb(mc,cx)
    d[key] = diff
  return diff <= maxdiff


def _check_match(xy0, gimg, limg, cmp=eq, cmpargs=()):
  '''check for limg in gimg starting at xy0 in gimg
     return coord of upper left corner if found
  '''
  def find_starts():
    '''find possible topleft coord of pix2 in pix1 around xy0'''
    x0 = max(0, xy0[0] - limg.size[0])
    xn = min(gimg.size[0], xy0[0] + limg.size[0])

    y0 = max(0, xy0[1] - limg.size[1])
    yn = min(gimg.size[1], xy0[1] + limg.size[1])
    for x,y in pixelloop((x0,y0), (xn,yn)):
      if cmp(gpix[x,y], lpix[0,0], *cmpargs):
        yield (x,y)

  def check_starts(x0,y0):
    ly,lx = 0,0
    xn = min(gimg.size[0], xy0[0] + limg.size[0])
    yn = min(gimg.size[1], xy0[1] + limg.size[1])
    for x,y in pixelloop((x0,y0), (x0+limg.size[0], y0+limg.size[1])):
      if not cmp(gpix[x,y], lpix[x-x0, y-y0], *cmpargs):
        return False
    return True

  gpix = gimg.load()
  lpix = limg.load()

  for start in find_starts():
    r = check_starts(*start)
    if not r:
      continue
    return start


def find_exact_image(localimg,globalimg=None,sshot_bbox=None):
  """find exact coords of a local image within a global image"""
  if not globalimg:
    gimg = screenshot(sshot_bbox)
  else:
    gimg = globalimg
  gpix = gimg.load()

  limg = localimg
  lpix = limg.load()
  lcolours = {lpix[x,y][:3] for y in range(limg.size[1]) for x in range(limg.size[0])}
  for gx,gy in pixelloop(0, gimg.size, limg.size):
    if gy > gimg.size[1] or gx > gimg.size[0]:
      continue
    if gpix[gx,gy][:3] in lcolours:
        r = _check_match(xy0=(gx,gy), gimg=gimg, limg=limg, cmp=eq)
        if not r:
          continue
        yield r

def find_solid_cdiff(gimg, colour, lsize, maxdiff=3.0):
    """find exact coords of a given colour rectangle in a global image 
     with at most maxdiff DeltaE"""

    gpix = gimg.load()
    d = {}
    for gx,gy in pixelloop(0, gimg.size, lsize):
      cx = gpix[gx,gy][:3]
      key = (colour,cx)
      if key in d:
        diff = d[key]
      else:
        diff = cdiff.diff_rgb(colour, cx)
        d[key] = diff
      if diff <= maxdiff:
        limg = Image.new('RGB', lsize, cx[:3])
        args = (maxdiff,d)
        r = _check_match(xy0=(gx,gy),
                         gimg=gimg,
                         limg=limg,
                         cmp=cmp_c,
                         cmpargs=args)
        if r:
          yield r
        else:
          continue
      else:
        continue
    return

def find_window():
    #file = 'imgrec/window/corner.png'
    file = os.path.join('imgrec', 'window', 'corner.png')
    limg = Image.open(file)
    for coord in find_exact_image(limg):
        yield (coord[0], coord[1], coord[0]+640, coord[1]+480)

def find_map(gbbox):
  gimg = screenshot(gbbox)
  #limg = Image.open('imgrec/map/corner.png')
  limg = Image.open(os.path.join('imgrec', 'map', 'corner.png'))
  for cpos in find_exact_image(limg, gimg):
    mappos = (cpos[0] + 4, cpos[1] + 4)
    return mappos  
  
def iter_map(gbbox):
  img = screenshot(gbbox)
  mappos = find_map(gbbox)
  #scale_dw = phys.constants.map_
  #windowed minimap, all(?) maps except AC
  #resizable map is scaled down by 8 rather than 16
  map = img.crop([mappos[0], mappos[1], mappos[0]+120, mappos[1]+60])
  pix = map.load()
  for x,y in pixelloop(0, map.size):
    yield (x,y),pix[x,y][:3]

def rgb2hex(rgb):
  return '#{:02x}{:02x}{:02x}'.format(*rgb)
