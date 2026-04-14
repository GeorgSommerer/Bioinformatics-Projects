import math
import numpy as np

m = 509000//2 - 1

res = m + 2*m*(m+1) + 2*m*(m+1)*(2*m+1)/3
print(res)