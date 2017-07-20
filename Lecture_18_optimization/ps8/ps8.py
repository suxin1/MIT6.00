# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:



import numpy
import random
import pylab
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    def isResistantToAll(self, drugs):
        for drug in drugs:
            if not self.isResistantTo(drug):
                return False
        return True

    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if drug not in self.resistances:
            self.resistances[drug] = False
            return False

        return self.resistances[drug]


    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        isResistant = True
        # If this virus not resistant to any one of the drug applied to the patient.
        # Then this virus considered can't reproducing
        for drug in activeDrugs:
            if not self.resistances[drug]:
                isResistant = False
                raise NoChildException

        birthProb = self.maxBirthProb * (1 - popDensity)

        if random.random() < birthProb:

            childResistances = {}
            for drug in self.resistances:
                if random.random() < self.mutProb:
                    childResistances[drug] = not self.resistances[drug]
                else:
                    childResistances[drug] = self.resistances[drug]
            return ResistantVirus(self.maxBirthProb, self.clearProb, childResistances, self.mutProb)

        else:
            raise NoChildException


class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        SimplePatient.__init__(self, viruses, maxPop)
        self.drugs = []

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        # should not allow one drug being added to the list multiple time
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)

    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.drugs

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        resistPop = 0
        for virus in self.viruses:
            if virus.isResistantToAll(drugResist):
                resistPop += 1

        return resistPop

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        survivedViruses = []
        append = survivedViruses.append

        for virus in self.viruses:
            if not virus.doesClear():
                append(virus)

        popDensity = float(len(survivedViruses))/self.maxPop

        childrenViruses = []
        append = childrenViruses.append
        for virus in survivedViruses:
            append(virus)

        for virus in survivedViruses:
            try:
                child = virus.reproduce(popDensity, self.drugs)
                append(child)
            except NoChildException:
                continue

        self.viruses = childrenViruses
        return len(childrenViruses)

#
# PROBLEM 2
#


def simulationWithDrug(resistances, drugs, mutProb=0.005, maxBirthProb=0.1, clearProb=0.05):
    """
    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """

    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for i in range(100)]
    patient = Patient(viruses, 1000)

    resistantPops = []
    totalPops = []

    # For performance concern
    addToRsist = resistantPops.append
    addTototal = totalPops.append

    try:
        delay = max(drugs)
    except:
        delay = 300

    for i in range(delay + 150):
        if i in drugs.keys():
            patient.addPrescription(drugs[i])
        currentPop = patient.update()
        addToRsist(patient.getResistPop(["guttagonol"]))
        addTototal(currentPop)

    # pylab.figure(1)
    # line1, = pylab.plot(resistantPops, 'r-', label="resistant population")
    # line2, =pylab.plot(totalPops, 'g--', label="total population")
    # pylab.xlabel("time steps")
    # pylab.ylabel("population")

    # line1legend = pylab.legend(handles=[line1], loc=1)
    # pylab.gca().add_artist(line1legend)
    # line2legend = pylab.legend(handles=[line2], loc=2)
    # pylab.show()

    return (resistantPops, totalPops)

# simulationWithDrug({"guttagonol": False}, {150: "guttagonol"})


#
# PROBLEM 3
#

def simulationDelayedTreatment():
    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).
    """
    finalData = []
    steps = [0, 75, 150, 300]
    for step in steps:
        data = []
        for i in range(30):
            result = simulationWithDrug({"guttagonol": False}, {step: "guttagonol"})
            data.append(result[1][len(result[1])-1])

        finalData.append(data)

    pylab.figure(1)
    pylab.title("The Effect of Delaying Treatment")
    xRange = None
    for i in range(4):
        subplot = "22" + str(i+1)

        pylab.subplot(int(subplot))
        xRange = makeHist(finalData[i], "Delay " + str(steps[i]) + "steps", "final total viruses", "number", (0, 550))

    pylab.show()


def makeHist(data, title, xlabel, ylabel, xrange=None):
    print data
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)
    if xrange:
        pylab.xlim(xrange[0], xrange[1])
    pylab.title(title)
    pylab.hist(data, 20, facecolor="g")

    return pylab.xlim()

# simulationDelayedTreatment()
#
# PROBLEM 4
#


def simulationTwoDrugsDelayedTreatment(resistances, drugs, mutProb=0.005, maxBirthProb=0.1, clearProb=0.05):
    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for i in range(100)]
    patient = Patient(viruses, 1000)

    resistantPops = []
    totalPops = []

    # For performance concern
    addToRsist = resistantPops.append
    addTototal = totalPops.append


    for i in range(300 + 150):
        if i in drugs.keys():
            patient.addPrescription(drugs[i])
        currentPop = patient.update()
        addToRsist(patient.getResistPop(["guttagonol"]))
        addTototal(currentPop)

    pylab.figure(1)

    line1, = pylab.plot(resistantPops, 'r-', label="resistant population")
    line2, =pylab.plot(totalPops, 'g--', label="total population")
    pylab.xlabel("time steps")
    pylab.ylabel("population")

    line1legend = pylab.legend(handles=[line1], loc=1)
    pylab.gca().add_artist(line1legend)
    line2legend = pylab.legend(handles=[line2], loc=2)
    pylab.show()

simulationTwoDrugsDelayedTreatment({"guttagonol": False, "grimpex": False}, {150: "guttagonol", 200: "grimpex"})


#
# PROBLEM 5
#

def simulationTwoDrugsVirusPopulations():

    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.
    """
    #TODO



