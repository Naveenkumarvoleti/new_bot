from itertools import combinations
from itertools import chain
import itertools
import time
teams = ["name", "name1" , "name3" , "name4"]

for game in combinations(teams,2):
    print(game)

for name in itertools.zip_longest('abcd','wxyz'):
##    time.sleep(0.3)
    print(name)
