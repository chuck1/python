
class Window:
    def __init__(self, t_0, t_1):
        self.t_0 = t_0
        self.t_1 = t_1

    def __add__(self, t):
        return Window(self.t_0 + t, self.t_1 + t)


