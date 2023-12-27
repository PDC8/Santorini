import sys
from game import Game

valid_args = [['human', 'heuristic', 'random'], ['human', 'heuristic', 'random'], ['on', 'off'], ['on', 'off']]
args = ["human", "human", "off", "off"]

for x in range(1, len(sys.argv)):
    if(sys.argv[x] in valid_args[x - 1]):
        args[x - 1] = sys.argv[x]
    else:
        print("Invalid Argument")

if(args[0] != 'human' and args[1] != 'human'):
    args[2] = 'off'

p1 = args[0] 
p2 = args[1]
enable_undo = False if args[2] == "off" else True
enable_score = False if args[3] == "off" else True


while True:
    game = Game(p1, p2, enable_undo, enable_score)
    game.play_game()
    print("Play again?")
    response = input()
    if response != "yes":
        break

