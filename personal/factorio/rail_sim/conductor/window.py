
class Window:
    def __init__(self, point, t_0, t_1, edge0, edge1):
        if t_0 > t_1:
            raise RuntimeError()
        
        self.point = point
        self.edge0 = edge0
        self.edge1 = edge1
        
        self.t_0 = t_0
        self.t_1 = t_1

    def __add__(self, t):
        return Window(self.t_0 + t, self.t_1 + t)


