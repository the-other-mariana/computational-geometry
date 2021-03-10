from Cola import Cola
from Evento import Evento

class Eventos:
  def __init__(self):
    self.eventos=Cola()
  def add(self, evento=Evento()):
    if evento.coord in self.eventos: 
        self.eventos[evento.coord]+=evento
        return self.eventos[evento.coord]
    else: 
        self.eventos[evento.coord] = evento
        return evento
  def __bool__(self):
    return bool(self.eventos)    
  def __hash__(self):
    return hash(self.eventos)
  def __repr__(self): 
    return repr(self.eventos)
  def __next__(self):
    try:
      return next(self.eventos)
    except StopIteration:
      raise StopIteration()
  def __iter__(self):
    return self

