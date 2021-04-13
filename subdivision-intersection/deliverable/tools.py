
class Tools:
    @staticmethod
    def getEdges(s, eMap):
        for key, value in eMap.items():
            if value.origin.pos == s.puntos[0] and value.next.origin.pos == s.puntos[1]:
                return value, value.mate
        return None, None

    @staticmethod
    def getIncident(p, eMap):
        for key, value in eMap.items():
            if value.origin.pos == p:
                return value
        return None

    @staticmethod
    def getMapValue(data, objMap):
        if "[" in data:
            data = data[1:(len(data) - 1)].split(',')
            return [objMap[d] for d in data]
        elif data.rstrip("\n") != 'None':
            return objMap[data]
        else:
            return None

    @staticmethod
    def getValidName(mapVal):
        if mapVal != None:
            return mapVal.name
        else:
            return "None"

    @staticmethod
    def writeFile(ext, content, LAYERS):
        outName = "output/files/layer0{n}.{e}".format(n=LAYERS + 1, e=ext)
        outFile = open(outName, "w")
        outFile.write(content)