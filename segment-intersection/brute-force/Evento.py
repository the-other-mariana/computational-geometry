from Punto import Punto

class Evento:
  def __init__(self, c=Punto(0,0)):
    self.coord = c 
    self.I = set() #Inician en c
    self.T = set() #Terminan en c
    self.C = set() #Se intersecan en c
  def __iadd__(self, otro):
    self.I |= otro.I #union
    self.T |= otro.T #union
    self.C |= otro.C #union
  def __hash__(self):
    return hash(self.coord)
  def __repr__(self):
    return f"--{self.coord}:: I:{self.I}, T:{self.T}, C:{self.C}"
