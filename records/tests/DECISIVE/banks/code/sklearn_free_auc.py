import numpy as np
from scipy.stats import rankdata
def auc(y,s):
    y=np.asarray(y); r=rankdata(s); n1=y.sum(); n0=len(y)-n1
    return (r[y==1].sum()-n1*(n1+1)/2)/(n1*n0)
