import numpy as np


""" profile class """
class Profile:
    """ constructor
        name   name of profile file
        names  name of variables
        data   ndarray of data with variables stored along first dimension
    """
    def __init__(self, filename, name, names, data):
        self.filename = filename
        self.name = name
        self.names = names
        self.data = data

    """ write to file """
    def write(self):

        m = np.shape(self.data)[0]
        n = self.data[0].size
        
        text = "(({0} point {1})\n".format(self.name, n)
        
        for name,i in zip(self.names,range(m)):
            text += "(" + name + "\n"
            temp = self.data[i].flatten()
            k = 0
            for j in range(n):
                text += "{0:16e} ".format(temp[j])
                k += 1
                if k == 5:
                    k = 0
                    text += "\n"
            text += ")\n"
 
        text += ")\n"
        
        with open(self.filename, 'w') as f:
            f.write(text)
