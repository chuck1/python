
class PipeSize(object):
    def __init__(self, nomialSize):
        self.nomialSize = nomialSize

    def __eq__(self, other):
        if not isinstance(other, PipeSize): return False

        if self.nomialSize != other.nomialSize: return False

        return True

class PipeConnection(object):
    def __init__(self, pipeSize, connectionType):
        self.pipeSize = pipeSize
        self.connectionType = connectionType

    def __eq__(self, other):
        print "PipeConnection.__eq__"

        if not isinstance(other, PipeConnection): return False

        if not(self.pipeSize == other.pipeSize): return False
        if not(self.connectionType == other.connectionType): return False

        return True


