from Constantes import eps

class Punto:
  def __init__(self, x=0, y=0):
    self.x = x
    self.y = y
  def __eq__(self, otro):
     if abs(self.x-otro.x)<eps and abs(self.y-otro.y)<eps: return True 
     return False 
  def __lt__(self, otro):
    if self.y> otro.y: return True
    if self.y< otro.y: return False
    if self.x< otro.x: return True
    return False
  def __repr__(self):
    return f"({self.x},{self.y})"
  def __hash__(self):
    return self.x<<8 + self.y
