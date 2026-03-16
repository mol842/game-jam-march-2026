from Game import *
import asyncio

async def main():
    print("STARTING")
    game = Game()
    while not game.stopped:
        game.update()
        game.draw()
        await asyncio.sleep(0)
        

if __name__ == "__main__":
    asyncio.run(main())