import random
import pylab

def rollFiveDice():
    diceList = [random.choice([1, 2, 3, 4, 5, 6]) for i in range(5) ]
    return diceList


def rollSimulate(numTrial=100):
    sameNum = 0

    for i in range(numTrial):
        resultList = rollFiveDice()

        first = resultList[0]
        isSame = True
        for r in resultList:
            if r != first:
                isSame = False
                break
        if isSame:
            sameNum += 1

    return float(sameNum)/numTrial


def runSimulate(numTrial=100):
    """
    From the mathematical view, the probability of rolling five twos is
    (1/6) * 5 = 1/7776. Since there are a total of six different number
    the probability of rolling the same is about (1/6) * 5 * 6 = 1/1295 = 0.08%.
    :param numTrial:
    :return:
    """
    result = []
    for i in range(numTrial):
        result.append(rollSimulate(20000))
    print len(result)
    pylab.figure(1)
    n, bins, patches = pylab.hist(result, 10, facecolor='g', alpha=0.75)
    pylab.show()

runSimulate()