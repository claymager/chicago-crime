import pandas as pd
import numpy as np

methods = {
    "bin": lambda x:
        x // 3,
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
    if type(temp) == tuple:
        return pd.DataFrame(np.column_stack(temp))
    elif type(temp[0]) in [int, np.int64, str]:
        return pd.get_dummies(temp, drop_first=True)
    else:
        return pd.DataFrame(temp)

def process_features(Xs, hour_method="bin", month_method="bin"):
    """
    Main feature engineering function
    Takes a DataFrame
    Returns a DataFrame ready for partitioning and StandardScalar

    *_methods: accept callable or str={"bin", "id", "mcyclic", "hcyclic"}
        warning: callables returning str, int, int64 make dummies. Careful with size.
    """
    hours = Xs["datetime"].transform(lambda x: x.hour)
    hours_df = process_cyclic(hours, hour_method)

    months = Xs["datetime"].transform(lambda x: x.month-1)
    months_df =  process_cyclic(months, month_method)
 
    business_days = Xs["datetime"].transform(np.is_busday)
    business_df = pd.DataFrame(business_days)

    out_df = hours_df\
            .join( months_df, rsuffix="m" )\
            .join( business_df, rsuffix = "b" )

    str_fields = [ c for c in Xs.columns if type( Xs[c][0] )==str ]
    for field in str_fields:
        dummies = pd.get_dummies(Xs[field], drop_first = True)
        out_df = out_df.join( dummies, rsuffix=field )

    return out_df
