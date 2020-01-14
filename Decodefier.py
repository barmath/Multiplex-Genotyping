# The eficiency time is quadradratic due some loop but I try to compensate
# this not so efficiency but using set stead of list due their linar time

# The Class decodefier take the input and break it in group of tests
# and then break the lines of the test in order to pass to the next class
# the results decodified and ready to be compute.
class Decodefier:
    #Global variables
    testRecivied =""
    splitedTests = []

    #Set the file to be tested
    def recivier(self):
        self.testRecivied  = open("input.txt", "r")

    #Split the group of tests
    def decodeGroups(self):
        group = []
        tempReci = self.testRecivied
        line = tempReci.readline()

        while(line):
            group.append(self.decodeLines(line,tempReci))
            line = tempReci.readline()
            if(line == "\n"):
                break
        self.splitedTests = group

    #Split the lines and clean the \n of the file 
    def decodeLines(self,l,gr):
        i = 0
        group = []
        line = l

        while(line):

            if "\n" in line:
                line = line.replace("\n","")

            group.append(line)
            line = gr.readline()

            if(line == "\n"):
                break

        return(group)

    #Main function to run the class
    def main(self):
        try:
            self.recivier()
            self.decodeGroups()
        except:
            print('Some probrem with the file has occurred')
#This is responsible to compute the results decodified in the class above
class Compute:

    normals = set()
    mutants = set()

    validMutants = set()
    difMutants = False

    #When Compute is called this initial method what will be used and runs it
    def __init__(self, listOfTests):
        self.groupOfTests = listOfTests
        self.separate()

    def separate(self):
        for i in range(len(self.groupOfTests)):
            self.computeSet(self.groupOfTests[i])

    def computeSet(self,setOfTests):

        for i in setOfTests:
            data = i.split(",")

            #Set the label to be check 
            prevResult = data[0]

            #Delete the label NORM or MUT
            del data[0]

            #Acording to the group it put on the respective set 
            if(prevResult == "NORM"):
                self.normals = self.defineSet(self.normals,data)
                
            elif(prevResult == "MUT"):
                self.is_diferent_mutant(data)
                self.mutants = self.defineSet(self.mutants,data)

                
        condition ="ok"

        self.validMutants = self.validate()
        condition = self.analizer(self.validMutants)

        self.output(condition)

        #Clear sets for the next group's analysis 
        self.normals.clear()
        self.mutants.clear()
        condition ="ok"
        
    #Put the data of the test in its respective set
    def defineSet(self,set,data):
        set.update(data)
        return set

    #Compute the real mutants compring the sets
    def validate(self):
        validMutants = self.mutants.difference(self.normals)
        return validMutants
  
    #Compute the final results and check the inconsistent results 
    def analizer(self,finalSet):

        countIconsi = 0
        noUnique = False

        if not finalSet:
            if self.mutants:
                countIconsi += 1
        else:
            if not self.normals:
                if self.difMutants:
                    countIconsi += 2
        
        if (countIconsi > 0):

            if (countIconsi == 1):
                return "INCONSISTENT"
            elif (countIconsi >= 2):
                return "NONUNIQUE"
        else:
            return "ok"
            
    
    def is_diferent_mutant(self,data):
        for i in data:
            if i not in self.mutants:
                self.difMutants = True 

    #Build the output computed
    def output(self,condition):
        if (condition == "ok"):

            lenMut = len(self.validMutants)
            lenNor = len(self.normals)

    
            print('MUT COUNT: {}'.format(lenMut))
            print('NORM COUNT: {}'.format(lenNor))

            for i in sorted(self.validMutants):
                print(i+',MUT')

            for i in sorted(self.normals):
                print(i+',NORM')

            print()
        
        else:
            print(condition)
            print()

#Runing class
class Run:
    def __init__(self):
        a =Decodefier()
        a.main()
        b = Compute(a.splitedTests)

run = Run()







