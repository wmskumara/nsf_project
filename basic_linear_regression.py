def basic_linear_regression(x,y):
  # basic required calculations
  length = len(x)
  sum_x = sum(x)
  sum_y = sum(y)
  
  # (Ex^2), and (Exy) respectively.
  sum_x_squared = sum(map(lambda a: a * a, x))
  sum_of_products = sum([x[i] * y[i] for i in range(length)])
  #intercept
  a = (sum_of_products - (sum_x * sum_y) / length) / (sum_x_squared - ((sum_x ** 2) / length))
  #slope
  b = (sum_y - a * sum_x) / length
  return a, b
  
  
  
# readings from csv and create lists for x and y  
x = [0,1,2,3,4,5,6,7,8,9,10]
y = [77.5,77.4,77.3,77.2,77.1,77,69.9,69.8,69.7,69.6,69.5]
# return slope and intercept
a1 = basic_linear_regression(list1,list2)
print(a1)
