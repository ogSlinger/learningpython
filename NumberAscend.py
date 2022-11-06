def numberAscend (inputList, separator = ' '):

    myInput = inputList.split(separator)

    inputIndex = 0

    #Casting the list elements into ints
    for recentNumber in myInput[:]:
        myInput[inputIndex] = int(recentNumber)
        inputIndex += 1

    rank = 0
    recentNumberCount = 0
    outputList = [' '] * len(myInput)

    #compares each element to every element in the list
    for recentNumber in myInput:
        for element in myInput:

            #recentNumberCount is how many times the number appears on the list
            #rank is the index of where the number will be written on new list
            if recentNumber < element:
                None
            elif recentNumber == element:
                recentNumberCount += 1
            elif recentNumber > element:
                rank += 1

        #Write the number down starting at rank position and going left-to-right writing for every
        #instance of the number
        while recentNumberCount > 0:
            outputList[rank] = recentNumber
            recentNumberCount -= 1
            rank += 1

        #Reset for the next number to be compared
        rank = 0
        recentNumberCount = 0

    #Weakness to this is the entire list gets compared to itself. So, the more there are duplicate
    #numbers in the list, the less efficient the code becomes.

    return outputList[:]