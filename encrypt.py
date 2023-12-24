import random

"""Ord returns the character's ASCII position. lowercase characters start at 97, so we subtract by 97"""

def chunky(path):
    """Function that takes a file and breaks it up into blocks of 2 characters"""
    unencryptedFile = open(path, "r")
    unencryptedContent = unencryptedFile.readlines()
    
    #make everything lowercase
    lower = [word.lower() for word in unencryptedContent]
    
    #replace all spaces with an empty string
    modifiedList = [word.replace(" ", "") for word in lower]
    
    #break up each word into 2 letter blocks
    chunks = [word[i:i+2] for word in modifiedList for i in range(0, len(word), 2)]
    
    #close file
    unencryptedFile.close()
    
    
    values = [] #list for letters converted to their ascii value (subtracted by 97 to work in normal alphabet positions)
    for block in chunks:
        for letter in block:
            values.append(ord(letter) - 97)
        #end for
    #end for
    
    return values
#end function here


class Unencrypted(object):
    """Unecnrypted matrix, converted from sentence to numbers"""
    
    def __init__(self, path) -> None:
        self.path = path

        allValues = chunky(self.path)
        
        rowOne = []
        rowTwo = []
        
        #take every other letter and place it into first row
        for letter in allValues[0::2]:
            rowOne.append(letter)
        #end for-loop
        
        #same idea as above
        for letter in allValues[1::2]:
            rowTwo.append(letter)
        #end for-loop
        
        self.topMat = rowOne
        self.botMat = rowTwo
    #end constructor
    
    def __str__(self) -> str:
        matrix_info = f"Unecnrypted Matrix:"
        matrix_info += f"{self.topMat}\n"
        matrix_info += f"{self.botMat}"
        return matrix_info
    #end string method
#end class unencrypted


class Key(object):
    """key matrix. numbers to be randomly generated"""
    
    def __init__(self) -> None:
        self.firstNumber = random.randint(1, 100)
        self.secondNumber = random.randint(1, 100)
        self.thirdNumber = random.randint(1, 100)
        self.fourthNumber = random.randint(1, 100)
    #end constructor
    
    def __str__(self) -> str:
        key_info = "Key matrix\n"
        key_info += f"{self.firstNumber} "
        key_info += f"{self.secondNumber}\n"
        key_info += f"{self.thirdNumber} "
        key_info += f"{self.fourthNumber}"
        return key_info
    #end string method
#end class key




class Matrix(object):
    """Matrix class that converts file contents into matrix"""
    
    def __init__(self, unecnrypted=str, key=False) -> None:
        """Check when matrix is created if it has an address for unecnrypted matrix. if it is empty, then that means key is true. if it is not empty, call encryption matrix class"""
        self.unecnryptedMatrix = unecnrypted    #passed from matrix creation. this would contain the file path if one is passed
        self.key = key                          #passed as True or False when creating the matrix. 
        #rows one and two divided into halves to make it easier to multiply and add when encrypting
        self.rowOneFirstHalf = []
        self.rowOneSecondHalf = []
        self.rowTwoFirstHalf = []
        self.rowTwoSecondHalf = []
        #rowOne and rowTwo are used for combining the halves from above after carrying out calculations
        self.rowOne = []
        self.rowTwo = []
        #these two are used for converting rowOne and rowTwo from above from numbers back into their alphabetical values
        self.encryptedOne = []
        self.ecnryptedTwo = []
        #final encrypted list, to be written into a file and returned
        self.encryptedText = []
        
        if self.unecnryptedMatrix == "":
            self.key = True
        #end if
        
        if self.key == True:
            self.newKey = Key()
            self.firstNumber = self.newKey.firstNumber
            self.secondNumber = self.newKey.secondNumber
            self.thirdNumber = self.newKey.thirdNumber
            self.fourthNumber = self.newKey.fourthNumber
        #end key matrix creation
        
        else:
            self.newUnencrypted = Unencrypted(self.unecnryptedMatrix)
            self.topMat = self.newUnencrypted.topMat
            self.botMat = self.newUnencrypted.botMat
        #end all matrix creations
    #end constructor here
    
    
    def __str__(self) -> str:
        matrix_info = ""
        if self.key == True:
            matrix_info += "Key matrix"
            matrix_info = str(self.newKey)
        #end if
        else:
            matrix_info = "Unencrypted matrix"
            matrix_info += str(self.newUnencrypted)        
        #end else
        return matrix_info
    #end string method
   
    
    def encrypt(self, other):
        """Method to encrypt a matrix. Would be called on the unencrypted matrix and passes the key matrix to multiply"""
        
        filePath = "encryptedText.txt"
        encryptedFile = open(filePath, "w")
        
        for topNumber in self.topMat:
            self.rowOneFirstHalf.append(other.firstNumber * topNumber)
            self.rowTwoFirstHalf.append(other.thirdNumber * topNumber)
        #end for
        for botNumber in self.botMat:
            self.rowOneSecondHalf.append(other.secondNumber * botNumber)
            self.rowTwoSecondHalf.append(other.fourthNumber * botNumber)
        #end for
        
        #make sure each half is the same size
        if len(self.rowOneFirstHalf) == len(self.rowOneSecondHalf):
            #for every number in position i in first list, add it to the number in the same position i as other list
            self.rowOne = [(x + y)%26 for x, y in zip(self.rowOneFirstHalf, self.rowOneSecondHalf)]
        #end if
        
        if len(self.rowTwoFirstHalf) == len(self.rowTwoSecondHalf):
            self.rowTwo = [(x+y)%26 for x, y in zip(self.rowTwoFirstHalf, self.rowTwoSecondHalf)]
        #end if
        
        else:
            print("List lengths do not match, add statement earlier that forces them to match")
        
        
        #encrypt first line on its own
        for number in self.rowOne:
            self.encryptedOne.append(chr(number + 97))
        #end for        
        
        #encrypt second line on its own
        for number in self.rowTwo:
            self.ecnryptedTwo.append(chr(number + 97))
        #end for
        
        #combine
        self.encryptedText = [item for pair in zip(self.encryptedOne, self.ecnryptedTwo) for item in pair]
        
        #write the list into the new file
        for letter in self.encryptedText:
            encryptedFile.write(letter)
        #end for-loop
        
        encryptedFile.close()
        
        return filePath
    
        
        
#end class here

#main program
myKey = Matrix("", True) #generate key matrix, if developer wants to see the key, just print it out here, but it is not put in the program by default to keep it secure

secretText = Matrix("test.txt", False)    #create the matrix to be encrypted

#call the encrypt method on the matrix that's being encrypted and pass the key matrix. encryot method returns the path of the encrypted file, which is assigned to encryptedPath here
encryptedPath = secretText.encrypt(myKey)


encryptedFile = open(encryptedPath, "r")
encryptedContent = encryptedFile.read()

print("File encrypted\n")
print(encryptedContent)

encryptedFile.close()
