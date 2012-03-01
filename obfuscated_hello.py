import random
MAGIC = [9659, 535161, 1013229, 1808381, 147283, 421756]  # Numbers from Harry Potter
hello = lambda x: ''.join([chr(int(str(randn)[2:8][:3]))+chr(int(str(randn)[2:8][3:])) for randn in [random.random() for m in MAGIC if random.seed(m) is None]])+x
print(hello('!'))
