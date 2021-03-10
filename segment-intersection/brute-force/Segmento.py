from Punto import Punto
from math import inf
from colorama import Fore as F
from colorama import Style as S

class Segmento:
  def __init__(self, p1=Punto(),p2=Punto()):
    self.puntos = sorted([p1,p2])
    self.x = p1.x
  def __repr__(self):
    return f"[{self.puntos[0]}, {self.puntos[1]}]"
  def __hash__(self):
    return hash(tuple(self.puntos))
  def calcularX(self, y):
    y-=0.01
    x1,y1 = self.puntos[0].x, self.puntos[0].y
    x2,y2 = self.puntos[1].x, self.puntos[1].y

    try:
      x= (x2-x1)/(y2-y1)*(y-y1)+x1
    except ZeroDivisionError:
      x= inf
    self.x = x
    return x
  def interseccion(self, otro):
    x1,y1= self.puntos[0].x, self.puntos[0].y
    x2,y2= self.puntos[1].x, self.puntos[1].y
    x3,y3= otro.puntos[0].x, otro.puntos[0].y
    x4,y4= otro.puntos[1].x, otro.puntos[1].y
    try:
      m1= (y2-y1)/(x2-x1)
      print(f"\t{F.YELLOW}Pendiente de {self} es {m1}{S.RESET_ALL}")
    except ZeroDivisionError:
      m1= 999999
    try:
      m2= (y4-y3)/(x4-x3)
      print(f"\t{F.YELLOW}Pendiente de {otro} es {m2}{S.RESET_ALL}")
    except ZeroDivisionError:
      m2= 999999
    try:
      x= ((m1*x1-y1)-(m2*x3-y3))/(m1-m2)
      y= (m1*(m2*x3-y3)-m2*(m1*x1-y1))/(m2-m1)
      print(f"\t{F.YELLOW}Posible intersección en ({x},{y}){S.RESET_ALL}")
    except ZeroDivisionError:
      return None
    if min(y1,y2)<= y<= max(y1,y2) and\
        min(y3,y4)<= y <= max(y3,y4) and\
        min(x1,x2)<= x <= max(x1,x2) and\
        min(x3,x4)<= x <= max(x3,x4):
          print(f"\t{F.YELLOW}Intersección válida{S.RESET_ALL}")
          return Punto(x,y)
    else:
      return None
