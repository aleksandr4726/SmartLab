import math
def avg(array):
    avg =sum(array)/ len(array)
    x = [(i - avg) ** 2 for i in array]
    y=sum(x)
    z=math.sqrt(y / (len(array) * (len(array) - 1)))
  #  return(avg,z)
    return (["{:.5g}".format(avg),"{:.3g}".format(z)])
print(avg([0.0001,0.0001,0.0001,0.0001,0.0001,0.0001]))