import pandas as pd

date_methods = {
        }

hour = {
        "bin": lambda x: (x+1)//3
        "linear": lambda x: x
        "cyclic": lambda x: ( np.sin(x*np.pi/12), np.cos(x*np.pi/12) ) 
        }

for n in
