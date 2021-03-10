class Cola:
  def __init__(self):
    self.q = []
  def __setitem__(self, punto, evento):
    self.q.append((punto, evento))
    self.q = sorted(self.q, key=lambda x: x[0])
  def __getitem__(self, punto):
    for i in self.q:
      if i[0]==punto: return i[1]
  def __contains__(self, punto):
    for i in self.q:      
      if i[0]== punto: return True
    return False  
  def __repr__(self):
    return repr(self.q)
  def __bool__(self):
    return bool(self.q)
  def __next__(self):
      if self.q:
          return self.q.pop(0)  
      else:
          raise StopIteration()
  def __iter__(self):
      return self
