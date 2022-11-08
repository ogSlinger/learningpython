import sys
import time

def main(args):
    startTime = time.perf_counter()
    results = sortStringAsListOfNumbers(sys.argv[1])
    endTime = time.perf_counter()
    print("Start - ", startTime)
    print("End - ", endTime)
    print("Time took to run method - ", (endTime - startTime))
    print(str(results))

def sortStringAsListOfNumbers (stringOfNumbers, separator = ' '):
    unsortedList = stringOfNumbers.split(separator)
    listLength = len(unsortedList)
    
    #Casting the list elements into ints
    for i in range(listLength):
        unsortedList[i] = int(unsortedList[i])

    rank = 0
    recentNumberCount = 0
    sortedList = [0] * listLength

# python test.py "1 3 2 5 4 5 4 3 2 5 7 67 66 666 56 344 1 3 2 5 4 5 4 3 2 5 7 67 66 666 56 344 1 3 2 5 4 5 4 3 2 5 7 67 66 666 56 344 1 3 2 5 4 5 4 3 2 5 7 67 66 666 56 344 1 3 2 5 4 5 4 3 2 5 7 67 66 666 56 344"

    #Start -  790518.2010933
    #End -  790518.2011182
    #Time took to run method -  2.489995677024126e-05
#    sortedList = unsortedList.sort()


    #Start -  790348.8306152
    #End -  790348.8308046
    #Time took to run method -  0.00018940004520118237
#    index = 1
#    sortedList[0] = unsortedList[0]
#    for i in range(1, listLength):
#        currentNumber = unsortedList[i]
#        for ii in range(index + 1):
#            sortedNumber = sortedList[ii]
#            if (ii == index):
#                sortedList[index] = currentNumber
#            elif (currentNumber < sortedNumber):
#                for iii in range(index - ii):
#                    sortedList[index - iii] = sortedList[index - iii - 1]
#                sortedList[ii] = currentNumber
#                break
#        index += 1


    #Start -  790326.5212354
    #End -  790326.5216115
    #Time took to run method -  0.0003760999534279108
    #compares each element to every element in the list
    for i in range(listLength):
        currentNumber = unsortedList[i]
        for ii in range(listLength):
            el = unsortedList[ii]
            
            #recentNumberCount is how many times the number appears on the list
            #rank is the index of where the number will be written on new list
            if currentNumber < el:
                None
            elif currentNumber == el:
                recentNumberCount += 1
            elif currentNumber > el:
                rank += 1

        #Write the number down starting at rank position and going left-to-right writing for every
        #instance of the number
        while recentNumberCount > 0:
            sortedList[rank] = currentNumber
            recentNumberCount -= 1
            rank += 1

        #Reset for the next number to be compared
        rank = 0
        recentNumberCount = 0

    #Weakness to this is the entire list gets compared to itself. So, the more there are duplicate
    #numbers in the list, the less efficient the code becomes.

    return sortedList
    
main(sys.argv)
 
