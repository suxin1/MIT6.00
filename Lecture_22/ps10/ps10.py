# Problem Set 10
# Name:
# Collaborators:
# Time:

#Code shared across examples
import pylab, random, string, copy, math


class Point(object):
    def __init__(self, name, originalAttrs, normalizedAttrs = None):
        """normalizedAttrs and originalAttrs are both arrays"""
        self.name = name
        self.unNormalized = originalAttrs
        self.attrs = normalizedAttrs

    def dimensionality(self):
        return len(self.attrs)

    def getAttrs(self):
        return self.attrs

    def getOriginalAttrs(self):
        return self.unNormalized

    def distance(self, other):
        #Euclidean distance metric
        difference = self.attrs - other.attrs
        return sum(difference * difference) ** 0.5

    def getName(self):
        return self.name

    def toStr(self):
        return self.name + str(self.attrs)

    def __str__(self):
        return self.name


class County(Point):
    weights = pylab.array([1.0] * 14)

    def __init__(self, name, originalAttrs, normalizedAttrs, weights):
        Point.__init__(self, name, originalAttrs, normalizedAttrs)

        if weights != None:
            County.weights = weights

    # Override Point.distance to use County.weights to decide the
    # significance of each dimension
    def distance(self, other):
        difference = self.getAttrs() - other.getAttrs()
        return sum(County.weights * difference * difference) ** 0.5


class Cluster(object):
    def __init__(self, points, pointType):
        self.points = points
        self.pointType = pointType
        self.centroid = self.computeCentroid()

    def getCentroid(self):
        return self.centroid

    def computeCentroid(self):
        dim = self.points[0].dimensionality()
        totVals = pylab.array([0.0]*dim)
        for p in self.points:
            totVals += p.getAttrs()
        meanPoint = self.pointType('mean',
                                   totVals/float(len(self.points)),
                                   totVals/float(len(self.points)), None)
        return meanPoint

    def update(self, points):
        oldCentroid = self.centroid
        self.points = points
        if len(points) > 0:
            self.centroid = self.computeCentroid()
            return oldCentroid.distance(self.centroid)
        else:
            return 0.0

    def getNameSet(self):
        nameset = [p.getName() for p in self.points]
        return nameset

    def getPoints(self):
        return self.points

    def contains(self, name):
        for p in self.points:
            if p.getName() == name:
                return True
        return False

    def toStr(self):
        result = ''
        for p in self.points:
            result = result + p.toStr() + ', '
        return result[:-2]

    def __str__(self):
        result = ''
        for p in self.points:
            result = result + str(p) + ', '
        return result[:-2]


def kmeans(points, k, cutoff, pointType, minIters = 3, maxIters = 100, toPrint = False):
    """ Returns (Cluster list, max dist of any point to its cluster) """
    #Uses random initial centroids
    initialCentroids = random.sample(points, k)
    clusters = []
    for p in initialCentroids:
        clusters.append(Cluster([p], pointType))
    numIters = 0
    biggestChange = cutoff

    # Do it enough times to find a good cluster
    while (biggestChange >= cutoff and numIters < maxIters) or numIters < minIters:
        print "Starting iteration " + str(numIters)
        newClusters = []  # A list of list of points
        for c in clusters:
            newClusters.append([])

        for p in points:  # Assign each point to it's nearest cluster
            smallestDistance = p.distance(clusters[0].getCentroid())
            index = 0
            for i in range(len(clusters)):
                distance = p.distance(clusters[i].getCentroid())
                if distance < smallestDistance:
                    smallestDistance = distance
                    index = i
            newClusters[index].append(p)
        biggestChange = 0.0

        # Update clusters which means find it's centroid and return the change of the centroid.
        for i in range(len(clusters)):
            change = clusters[i].update(newClusters[i])
            #print "Cluster " + str(i) + ": " + str(len(clusters[i].points))
            biggestChange = max(biggestChange, change)
        numIters += 1
        if toPrint:
            print 'Iteration count =', numIters

    maxDist = 0.0   # The biggest distance among all the points to centroid of it's own cluster.
    for c in clusters:
        for p in c.getPoints():
            if p.distance(c.getCentroid()) > maxDist:
                maxDist = p.distance(c.getCentroid())
    print 'Total Number of iterations =', numIters, 'Max Diameter =', maxDist
    print biggestChange
    return clusters, maxDist


#US Counties example
def readCountyData(fName, numEntries = 14):
    dataFile = open(fName, 'r')
    dataList = []
    nameList = []
    maxVals = pylab.array([0.0]*numEntries)
    #Build unnormalized feature vector
    for line in dataFile:
        if len(line) == 0 or line[0] == '#':
            continue
        dataLine = string.split(line)
        name = dataLine[0] + dataLine[1]
        features = []
        #Build vector with numEntries features
        for f in dataLine[2:]:
            try:
                f = float(f)
                features.append(f)
                if f > maxVals[len(features)-1]:
                    maxVals[len(features)-1] = f
            except ValueError:
                name = name + f
        if len(features) != numEntries:
            continue
        dataList.append(features)
        nameList.append(name)
    return nameList, dataList, maxVals


def buildCountyPoints(fName, weights):
    """
    Given an input filename, reads County values from the file and returns
    them all in a list.
    """
    nameList, featureList, maxVals = readCountyData(fName)
    points = []
    for i in range(len(nameList)):
        originalAttrs = pylab.array(featureList[i])
        normalizedAttrs = originalAttrs/pylab.array(maxVals)  # Normalized feature's value is between 0 and 1
        points.append(County(nameList[i], originalAttrs, normalizedAttrs, weights))
    return points

def randomPartition(l, p):
    """
    Splits the input list into two partitions, where each element of l is
    in the first partition with probability p and the second one with
    probability (1.0 - p).

    l: The list to split
    p: The probability that an element of l will be in the first partition

    Returns: a tuple of lists, containing the elements of the first and
    second partitions.
    """
    l1 = []
    l2 = []
    for x in l:
        if random.random() < p:
            l1.append(x)
        else:
            l2.append(x)
    return (l1,l2)

def getAveIncome(cluster):
    """
    Given a Cluster object, finds the average income field over the members
    of that cluster.

    cluster: the Cluster object to check

    Returns: a float representing the computed average income value
    """
    tot = 0.0
    numElems = 0
    for c in cluster.getPoints():
        tot += c.getOriginalAttrs()[1]

    return float(tot) / len(cluster.getPoints())


def test(points, k=200, cutoff=0.1):
    """
    A sample function to show you how to do a simple kmeans run and graph
    the results.
    """
    incomes = []
    print ''
    clusters, maxSmallest = kmeans(points, k, cutoff, County)

    for i in range(len(clusters)):
        if len(clusters[i].points) == 0: continue
        incomes.append(getAveIncome(clusters[i]))

    pylab.hist(incomes)
    pylab.xlabel('Ave. Income')
    pylab.ylabel('Number of Clusters')
    pylab.show()


# --------------------------------------------------------
#                          Problem 1
# --------------------------------------------------------

def graphRemovedErr(points, kvals = [25, 50, 75, 100, 125, 150], cutoff = 0.1):
    """
    Should produce graphs of the error in training and holdout point sets, and
    the ratio of the error of the points, after clustering for the given values of k.
    For details see Problem 1.
    """

    # Your Code Here
    l1, l2 = randomPartition(points, 0.8)
    trainingSetE = []
    holdoutSetE = []

    for k in kvals:
        clusters, maxDis = kmeans(l1, k, cutoff, County)

        errorT = 0
        errorHlist = []

        # Total Error for each k where TE = Sum(distance of point to the centroid of its encapsulating cluster)
        for c in clusters:
            for p in c.getPoints():
                dis = p.distance(c.getCentroid())
                errorT += dis ** 2

        # For each point in l2 list find its distance to its nearest cluster
        for p in l2:
            # Find the smallest square distance from point to all the clusters
            smallestDis = p.distance(clusters[0].getCentroid())
            for c in clusters:
                currentDis = p.distance(c.getCentroid())
                if currentDis < smallestDis:
                    smallestDis = currentDis

            errorHlist.append(smallestDis ** 2)

        holdoutSetE.append(sum(errorHlist))
        trainingSetE.append(errorT)

    hrRatio = [holdoutSetE[i]/trainingSetE[i] for i in range(len(kvals))]
    pylab.figure(1)
    pylab.plot(kvals, holdoutSetE, '--r', label="hold out set error")
    pylab.plot(kvals, trainingSetE, '-g', label="training set error")
    pylab.xlabel("K (Number of clusters)")
    pylab.ylabel("Error")
    pylab.legend()

    pylab.figure(2)
    pylab.plot(kvals, hrRatio, '--r')
    pylab.xlabel("K (Number of clusters)")
    pylab.ylabel("HR ratio")
    pylab.show()


# --------------------------------------------------------
#                          Problem 2
# --------------------------------------------------------


# graphRemovedErr(testPoints)

def observeOneCounty(points):
    county = "MNLake"
    print ("Observe county MN Lake")

    # Create file
    file = open("result", "w")
    file.write("Clusters which includes " + county + " in 10 time clustering\n")

    clusterset = []
    clusterOblist = []

    for i in range(10):
        clusters, maxDis = kmeans(points, 50, 0.1, County)
        for i in range(len(clusters)):
            c = clusters[i]

            isFound = False

            for p in c.getPoints():
                if p.getName() == county:
                    clusterset.append(c.getNameSet())
                    clusterOblist.append(c)
                    isFound = True
                    break
            if isFound:
                break

    return clusterset, clusterOblist


def printOut(cluster):
    points = cluster.getPoints()
    for p in points:
        values = [round(attr, 3) for attr in p.getAttrs()]
        print (p.getName(), values)


def analyzeCluster(clusterset):
    numList = []
    rotiolist = []

    for i in range(1, len(clusterset)):
        num = 0
        for p in clusterset[i]:
            if p in clusterset[0]:
                num += 1
            print ("cluster {} point {} {} {}".format(i, p, p in clusterset[0], num))
        rotiolist.append(num/len(clusterset[i]))
        numList.append(len(clusterset[i]))
    print clusterset


    pylab.figure(1)
    pylab.subplot(211)
    pylab.plot(rotiolist, 'bo')
    pylab.ylabel("similarity")
    pylab.xlabel("number of trials")

    pylab.subplot(212)
    pylab.plot(numList, 'ro')
    pylab.ylabel("total number of points in a cluster")
    pylab.xlabel("number of trials")
    pylab.show()


# clusterset, clusters = observeOneCounty(testPoints)
# analyzeCluster(clusterset)


# --------------------------------------------------------
#                          Problem 3
# --------------------------------------------------------

def graphPredictionErr(points, dimension, kvals = [25, 50, 75, 100, 125, 150], cutoff = 0.1):
    """
    Given input points and a dimension to predict, should cluster on the
    appropriate values of k and graph the error in the resulting predictions,
    as described in Problem 3.
    """
    averagePovertys = []
    averageDiff = []

    l1, l2 = randomPartition(points, 0.8)

    for k in kvals:
        clusters, maxDis = kmeans(l1, k, cutoff, County)

        # Total Error for each k where TE = Sum(distance of point to the centroid of its encapsulating cluster)
        for c in clusters:
            points = c.getPoints()
            if len(points) < 1:
                averagePovertys.append(0)
                continue

            povertyValues = [p.getOriginalAttrs()[dimension] for p in points]

            try:
                averagePovertys.append(sum(povertyValues)/len(points))
            except ZeroDivisionError:
                continue

        # For each point in l2 list find its distance to its nearest cluster
        squaredDiff = []
        for p in l2:
            # Find the smallest square distance from point to all the clusters
            smallestDis = p.distance(clusters[0].getCentroid())
            nearestCluster = clusters[0]
            nearestClusterIndex = 0

            for i in range(len(clusters)):
                currentDis = p.distance(clusters[i].getCentroid())
                if currentDis < smallestDis:
                    smallestDis = currentDis
                    nearestCluster = c
                    nearestClusterIndex = i

            squaredDiff.append((p.getOriginalAttrs()[dimension] - averagePovertys[nearestClusterIndex]) ** 2)

        averageDiff.append(sum([sd for sd in squaredDiff]) / len(squaredDiff))



    # pylab.figure(1)
    # pylab.plot(kvals, averageDiff, '-g', label="poverty mean difference")
    # pylab.xlabel("K (Number of clusters)")
    # pylab.ylabel("poverty mean difference")
    # pylab.show()

    return averageDiff


def findBest():
    kvals = [25, 50, 75, 100, 125, 150]
    weightsSet = []
    for i in range(10):
        weights = pylab.array([random.choice([0, 1]) for i in range(14)])
        weights[2] = 0
        weightsSet.append(weights)

    averageDiff = None
    bestWeight = []
    for weights in weightsSet:
        points = buildCountyPoints('counties.txt', weights)
        averageDiffTemp = graphPredictionErr(points, 2)

        if averageDiff == None:
            averageDiff = averageDiffTemp
            bestWeight = weights

        elif max(averageDiffTemp) < max(averageDiff):
            averageDiff = averageDiffTemp
            bestWeight = weights

    print bestWeight
    pylab.figure(1)
    pylab.plot(kvals, averageDiff, '-g', label="poverty mean difference")
    pylab.xlabel("K (Number of clusters)")
    pylab.ylabel("poverty mean difference")
    pylab.show()

findBest()