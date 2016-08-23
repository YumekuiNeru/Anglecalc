import phys
import improc

try:
  import Tkinter as TK
except ImportError:
  import tkinter as TK

class buttonframe(object):
  def __init__(self, root, toplabel, size, pos, f, bg='white', funclabel=False):
    frame = TK.Frame(root, width=size[0], height=size[1], background=bg,bd=1,relief=TK.GROOVE)
    frame.grid_propagate(False)
    frame.grid(row=pos[0], column=pos[1])
    frame.bind('<Button-1>', f)

    frame.grid_columnconfigure(0, weight=1)
    
    if funclabel:
        label = TK.Label(frame, text=funclabel, width=10, height=2)
    else:
        label = TK.Label(frame, text=f.__name__,width=10,height=2)
    label.grid(row=0)
    
    infotext = TK.StringVar()
    infolabel = TK.Label(frame, textvariable=infotext, justify=TK.CENTER)
    infolabel.grid(row=1)
    
    infolabel.bind('<Button-1>', f)
    label.bind('<Button-1>', f)
    
    self.toplabel = label
    self.infotext = infotext
    self.frame = frame

    self.set_text('0')
  def set_text(self, text):
    self.infotext.set(text)

class infoframe(object):
  def __init__(self, root, size, pos, bg='white'):
    frame = TK.Frame(root, width=size[0], height=size[1], background=bg, bd=1, relief=TK.GROOVE)
    frame.grid(row=pos[0], column=pos[1])
    frame.grid_propagate(False)
    frame.grid_columnconfigure(1, weight=1)

    d = {}
    self.d = d
    d['tar_angle'] = self.make_label(frame, 'tar_angle', 0)
    d['space1'] = self.make_label(frame, '', 1)
    d['src_pos'] = self.make_label(frame, 'src_pos', 2, width=10)
    d['dst_pos'] = self.make_label(frame, 'dst_pos', 3, width=10)
    
    self.set_text('space1', '')

  def make_label(self, root, label, row, column=0, width=None):
    left = TK.Label(root, text=label, justify=TK.LEFT, anchor=TK.W)
    textvar = TK.StringVar()
    if width:
      right = TK.Label(root, textvar=textvar, justify=TK.LEFT, anchor=TK.W,width=width)
    else:
      right = TK.Label(root, textvar=textvar, justify=TK.LEFT)

    left.grid(row=row, column=column)
    right.grid(row=row, column=column+1)

    return textvar
  def set_text(self, name, text):
    self.d[name].set(text)

class GUI(object):
  def __init__(self):
    self.buttons = []
    self.gamepos = False
    
    self.postoggle = False
    self.src = (-1,-1)
    self.dst = (-1,-1)
  def main(self):
    master = TK.Tk()
    scale=8

    mf = TK.Frame(master, width=120*scale, height=20*scale)
    mf.grid_propagate(False)
    mf.grid(row=0,column=0,rowspan=3)

    info = infoframe(mf, (30*scale,20*scale), (0,0))
    
    spellframe = TK.Frame(mf, width=30*scale,height=20*scale)
    spellframe.grid(row=0,column=1,rowspan=3)
    
    mapframe = TK.Frame(mf, width=30*scale, height=20*scale)
    #mapframe.grid(row=0,column=3,rowspan=2,columnspan=2)
    mapframe.grid(row=0,column=3,rowspan=1,columnspan=1)
    
    self.bso = buttonframe(spellframe, 'ol', (30*scale,20*scale//3), (0,0), lambda *event: self.spells('o', event), funclabel='ol')
    self.bsn = buttonframe(spellframe, 'normal', (30*scale,20*scale//3), (1,0), lambda *event: self.spells('n', event), funclabel='normal')
    self.bsb = buttonframe(spellframe, 'bftp', (30*scale,20*scale//3), (2,0), lambda *event: self.spells('b', event), funclabel='bftp')
    self.bsn.set_text('1')
    
    self.b_g = buttonframe(mf, 'find_game', (30*scale,20*scale), (0,2), self.find_game)
    #self.b_m = buttonframe(mapframe, 'update_map', (30*scale,10*scale), (0,3), self.update_map)
    self.b_m = buttonframe(mapframe, 'update_map', (30*scale,20*scale), (0,3), self.update_map)

    #self.b16 = buttonframe(mapframe, 's16', (15*scale,10*scale), (1,1), lambda *event: phys.constants.scale16(), funclabel='scale 16')
    #self.b08 = buttonframe(mapframe, 's08', (15*scale,10*scale), (1,1), lambda *event: phys.constants.scale08(), funclabel='scale 08')
    
    w = TK.Canvas(master, width=120*scale, height=(60)*scale)
    w.grid(row=4,column=0)
    w.bind('<Button-1>', self.set_coord)
    
    self.info = info
    self.canvas = w
    self.scale = scale
    self.master = master
    self.mf = mf
    
    TK.mainloop()
  def spells(self, spell, event):
    self.bso.set_text('0')
    self.bsn.set_text('0')
    self.bsb.set_text('0')
    if spell == 'o':
        self.bso.set_text('1')
        phys.constants.set_overlight()
    elif spell == 'n':
        self.bsn.set_text('1')
        phys.constants.set_normal()
    elif spell == 'b':
        self.bsb.set_text('1')
        phys.constants.set_bftp()
    self.update_angle()
  def find_game(self, *event):
    wc=False
    for wc in improc.find_window():
      self.gamepos = wc
      self.b_g.set_text('[{}, {}, {}, {}]'.format(*wc))
      return wc
    if not wc:
      return False

  def update_map(self, *event):
    r = False
    if not self.gamepos:
      r = self.find_game()
      self.gamepos = r
    else:
      r = self.gamepos

    if not r:
      return False
    for (w,h),rgb in improc.iter_map(r):
      x0,y0 = w*self.scale, h*self.scale
      xn,yn = (w+1)*self.scale, (h+1)*self.scale
      c = improc.rgb2hex(rgb)
      self.canvas.create_rectangle(x0,y0,xn,yn, fill=c)
  def set_coord(self, *event):
    event = event[0]
    x,y = event.x//self.scale, event.y//self.scale
    if not self.postoggle:
      self.src = x,y
      self.info.set_text('src_pos', '({}, {})'.format(*self.src))
      self.info.set_text('dst_pos', '({}, {})<--'.format(*self.dst))
    else:
      self.dst = x,y
      self.info.set_text('dst_pos', '({}, {})'.format(*self.dst))
      self.info.set_text('src_pos', '({}, {})<--'.format(*self.src))
    self.postoggle = not self.postoggle
    if self.src and self.dst:
        self.update_angle()

  def update_angle(self):
      dx = self.dst[0] - self.src[0]
      dy = self.dst[1] - self.src[1]

      map_scale = phys.constants.map_scale
      s = phys.constants.dist
      t = phys.constants.time
      ang = phys.angle_to_xy(dx*map_scale, dy*map_scale, s=s, t=t)
      if ang == 0:
        ang = 'N/A','N/A'
      self.info.set_text('tar_angle', '{},  {}'.format(*ang))


GUI().main()


