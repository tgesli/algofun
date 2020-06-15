from datetime import datetime
from blocku import Blocku
import players


def main():

    stateCount = 0
    dataSetSize = 500000


    while True:
        game = Blocku(players.SmartPlayer(5))
        startTime = datetime.now()
        results = game.run()
        stateCount += results["moves"]

        print("Final score = {}".format(results["score"]))
        print("Total moves = {}".format(results["moves"]))
        print("Start time: {} \nEnd time: {}".format(startTime, datetime.now()))
        print("Elapsed time: {}".format(datetime.now() - startTime))

        if stateCount>dataSetSize:
            return


if __name__ == '__main__':
    main()
