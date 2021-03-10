from Eventos import Eventos
from LineaBarrido import LineaBarrido
from Evento import Evento
from colorama import Fore as F
from colorama import Style as S

class AlgoritmoBarrido():
  def __init__(self, segmentos):
    self.Q=Eventos()
    self.T=LineaBarrido()
    self.R = []
    for s in segmentos:
      p1,p2= s.puntos
      e = Evento(p1)
      e.I.add(s)
      self.Q.add(e)
      e= Evento(p2)
      e.T.add(s)
      self.Q.add(e)

  def __next__(self):
    try:
       e = next(self.Q)
       self.procesar(e)
       return e
    except StopIteration:
      raise StopIteration()
  def __iter__(self):
    return self
  def procesar(self, evento):
    evento=evento[1]
    if not evento: return 
    print(f"Procesando evento {evento}")
    p = evento.coord
    # Agrega el evento a la solución como una intersección si hay por lo menos
    # dos líneas que participen en el evento.
    if len(evento.I|evento.T|evento.C) > 1:
      self.R+= (p, evento.I|evento.T|evento.C)
    # Eliminamos de la linea de barrido los segmentos que no continuan  
    for s in list(evento.T|evento.C):
      del self.T[s]
    # Agregamos a la linea de barrido los segmentos que inician 
    for s in list(evento.I|evento.C):
      self.T.add(s, p.y)
    # Actualizamos la posición en la linea de barrido de cada uno de los 
    # segmentos que quedaron finalmente
    for s in self.T.segmentos:
      s.calcularX(p.y)
    self.T.ordenar()
    print(f"{F.MAGENTA}Linea de barrido:\n{self.T}{S.RESET_ALL}")
    nuevos = evento.I|evento.C
    print(f"{F.GREEN}Eventos nuevos en la linea: {nuevos}{S.RESET_ALL}")
    if not nuevos:
      si = self.T.izquierda(p.x)
      sd = self.T.derecha(p.x)
      self.encontrarEvento(si,sd,p)
    else:
      nuevos_ordenados = []
      nuevos_ordenados = sorted(list(nuevos), key=lambda s:s.x)
      sp=  nuevos_ordenados[ 0]
      spp= nuevos_ordenados[-1]
      si= self.T.izquierda(sp.x)
      sd= self.T.derecha(spp.x)
      print(f"\t{F.BLUE}"   +f"Elementos nuevos a la izquierda: {sp} y derecha: {spp}"  +f"{S.RESET_ALL}")
      print(f"\t\t{F.CYAN}" +f"Izquierda de {sp} es {si}"                     )
      print(f"\t\t"         +f"Derecha de {sp} es {sd}"      +f"{S.RESET_ALL}")
      self.encontrarEvento(si,sp,p)
      self.encontrarEvento(spp,sd,p)
  def encontrarEvento(self, si, sd, p):
    if not si or not sd: return
    print(f"Comprobar si hay nuevos eventos con {si} y {sd} en {p}")
    interseccion = si.interseccion(sd)
    if not interseccion: return
    if p.y> interseccion.y:
      e = Evento(interseccion)
      e.C.add(si)
      e.C.add(sd)
      self.Q.add(e)
  def barrer(self):
      e = None
      if self.Q.eventos.q:
        e = self.Q.eventos.q.pop(0)
      while e:
        self.procesar(e)
        e = None
        if self.Q.eventos.q:
          e = self.Q.eventos.q.pop(0)

