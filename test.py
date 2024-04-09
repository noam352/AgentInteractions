import random

x = {"1", "2", "3"}
# u, v = random.sample(list(x), 2)
delta_walk = random.choice([(0,1),(1,0),(0,-1),(-1,0)])
# print(u, v)
print(delta_walk)