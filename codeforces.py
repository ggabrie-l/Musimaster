'''
players = list(input())
maxscore = list(input())

count = 0

for i in maxscore:
    if int(i) > int(players[0]) or int(i) > int(players[1]):
        count += 1

print(count)
'''

'''
sizeY = int(input())
sizeX = int(input())

count = 0

for i in range(1, sizeY * sizeX, 2):
    count += 1


print(count)
'''