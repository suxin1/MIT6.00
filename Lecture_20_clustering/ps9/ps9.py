# 6.00 Problem Set 9
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.


    # TODO: Instead of printing each line, modify the above to parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).

    tempDic = {}

    with open(filename) as file:
        for line in file:
            items = line.split(',')
            if len(items) > 2:
                # Remove the \r\n from the last string item
                print items
                items[2] = items[2].split('\r')[0]
                tempDic[items[0]] = (int(items[1]), int(items[2]))

    return tempDic

# print(loadSubjects("subjects.txt"))

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    # TODO...

    return subInfo1[VALUE] > subInfo2[VALUE]

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    # TODO...
    return subInfo1[WORK] < subInfo2[WORK]

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    # TODO...
    return (float(subInfo1[VALUE])/subInfo1[WORK]) > (float(subInfo2[VALUE])/subInfo2[WORK])


def dicSort(dic, comparator):
    """
    Sort a dictionary
    :param dic: dictionary object
    :param comparator: function
    :return: list
    """
    keys = dic.keys()
    for i in range(len(keys)):
        for j in range(len(keys) - 1):
            if not comparator(dic[keys[j]], dic[keys[j + 1]]):
                temp = keys[j]
                keys[j] = keys[j + 1]
                keys[j + 1] = temp
    return keys



def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    # TODO...
    tempCopy = dicSort(subjects, comparator)
    result = {}
    totalValue = 0
    totalWork = 0

    for key in tempCopy:
        if totalWork + subjects[key][1] < maxWork:
            totalWork += subjects[key][1]
            totalValue += subjects[key][0]
            result[key] = subjects[key]
    return result


#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    # TODO...
    keys = subjects.keys()
    strategylist = generateBin(len(keys))

    itemsSet = genItemsSet(keys, strategylist)

    print ("Object length: " + str(len(subjects)))
    print ("Possible option: " + str(len(itemsSet)))
    bestValue = 0
    bestOption = []
    finalSet = {}

    for items in itemsSet:
        totalValue = 0.0
        totalWork = 0.0
        for item in items:
            totalValue += subjects[item][VALUE]
            totalWork += subjects[item][WORK]
        if totalValue > bestValue and totalWork <= maxWork:
            bestValue = totalValue
            bestOption = items

    for key in bestOption:
        finalSet[key] = subjects[key]

    return finalSet

def genItemsSet(keys, strategylist):
    """
    Generate a list of item list based on a binary list
    :param keys:
    :param strategylist: list e.g [0,1,0,0,0,1]
    :return: list [[items], [items], [items]]
    """
    itemsSet = []
    for strategy in strategylist:
        itemsSet.append(getItems(keys, strategy))

    return itemsSet


def getItems(keys, strategy):
    items = []
    for i in range(len(strategy)):
        if (strategy[i]):
            items.append(keys[i])
    return items


def generateBin(num):
    """
    Generate a set of binary list from 0 to num**2
    :param num: int
    :return: list of list
    """
    assert type(num) is int
    result = []
    for i in range(2**num):
        bin = int2bin(i)
        if not len(bin) == num:
            [bin.insert(0, 0) for i in range(num - len(bin))]

        result.append(bin)
    return result


def int2bin(num):
    """
    Convert a int number to binary
    :param num: int
    :return: list e.g [1,0,1,0]
    """

    bin = []
    while num > 0:
        bit = num % 2
        bin.insert(0, bit)
        num = num // 2
    return bin

shortenedSubjects = {'12.02': (5, 5), '12.03': (2, 1), '12.04': (7, 1), '12.07': (6, 3), '12.06': (2, 5), '12.08': (2, 4), '12.09': (8, 2), '12.15': (10, 7)}
print bruteForceAdvisor(loadSubjects("shortened_subjects.txt"), 7)