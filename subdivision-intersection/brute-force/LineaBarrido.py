class LineaBarrido:
  def __init__(self):
    self.segmentos=[]
  def __repr__(self):
    r=[]
    for s in self.segmentos:
      r.append( str((s.x, s)))
    return "\n".join(r)
  def __delitem__(self, key):
    if key in self.segmentos:
      self.segmentos.pop(self.segmentos.index(key))
  def add(self, segmento,y):
    self.segmentos.append(segmento)
  def ordenar(self):
    self.segmentos.sort(key=lambda s: s.x)
  def izquierda(self, x):
    try:   
      for i in range(len(self.segmentos)):
        if self.segmentos[i].x >= x:
          if i==0: return None
          return self.segmentos[i-1]
      return self.segmentos[-1]
    except IndexError:
      return None
  def derecha(self, x):
    try:   
      for i in range(len(self.segmentos)):
        if self.segmentos[i].x > x:
          return self.segmentos[i]
      return None
    except IndexError:
      return None
