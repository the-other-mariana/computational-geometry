from Segmento import Segmento
from Punto import Punto

s1 = Segmento(Punto(0,0),Punto(10,10))
s2 = Segmento(Punto(0,10),Punto(10,0))

print(f"Intersección encontrada en: {s1.interseccion(s2)}")
