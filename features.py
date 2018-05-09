import pkandas as pd
import numpy as np

methods = {
    "bin": lambda x:
        (x-1) // 3,
    "id": lambda x:
        x,
    "mcyclic": lambda x: 
        ( np.sin(x*np.pi/6), np.cos(x*np.pi/6) ),
    "hcyclic": lambda x:
        ( np.sin(x*np.pi/12), np.cos(x*np.pi/12) ) 
    }

def process_cyclic(arr, method):
    """
    Takes:  np.array(Num)
            String or callable :: Num -> (Discrete t)
                -   creates dummies from Ints, Strs
                -   returns float as is
    Returns:
            pd.DataFrame
    """
    if type(method) == str:
        func = methods[method]
    else:
        func = method
    vector_func = np.vectorize(func)
    temp = vector_func(arr)
    if type(temp[0]) == tuple:
        return temp.apply(pd.Series)
    elif type(term[0]) in [int, np.int64, str]:
        return pd.get_dummies(temp, drop_first=True)
    else:
        return pd.DataFrame(temp)
        
def process_features(Xs, hour_method="bin", month_method="bin"):
    """
    Main feature engineering function
    Takes a DataFrame
    Returns a DataFrame ready for partitioning and StandardScalar

    *_methods: accept callable or str={"bin", "id", "cyclic", "cyclic"}
        warning: callables returning str, int, int64 make dummies. Careful with size.
    """
    new_df = pd.DataFrame()
    hours = Xs["datetime"].transform(lambda x: x.hour)
    new_df.join( process_cyclic(hours, hour_method), rsuffix="h", in_place=True )

    months = Xs["datetime"].transform(lambda x: x.month)
    new_df.join( process_cyclic(months, month_method), rsuffix="m", in_place=True )
    
    new_df["is_busday"] = Xs.["datetime"].transform(np.is_busday)
    

    Xs.join(temp_h, rsuffix="h", in_place=True)
