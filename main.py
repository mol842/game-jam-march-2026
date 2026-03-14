from Game import *

def main():
    print("STARTING")
    game = Game()
    while not game.stopped:
        game.update()
        game.draw()
        

if __name__ == "__main__":
    main()