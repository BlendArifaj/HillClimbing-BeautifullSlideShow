import copy
import datetime
import random

class beautifulSlideShowHillClimbing:
    initialSolution = []
    initialFitness = 0
    outputSolution = []
    outputFitness = 0
    inputForm  = []
    fileName = ""
    totalPhoto = 0
    actualSolution = []
    actualFitness = 0

    def __init__(self,_fileName):
        self.initialSolution = []
        self.inputForm = []
        self.fileName = _fileName
        self.totalPhoto = 0
        self.actualFitness = 0
        self.initialFitness = 0
        self.actualSolution = []
        self.initializeInputForm()
        self.generateInitialSolution()

    def outputToFile(self):
        file = open("HillClimbingResults_"+str(datetime.datetime.now())+".out","w+")
        file.write(str(len(self.actualSolution))+"\n")
        for i in range(0,len(self.actualSolution),1):
            if isinstance(self.actualSolution[i], int):
                file.write(str(self.actualSolution[i])+"\n")
            else:
                file.write(str(self.actualSolution[i][0]) +" "+str(self.actualSolution[i][1])+"\n")

        file.close()

    def initializeInputForm(self):
        file = open(self.fileName, 'r')
        self.totalPhoto = int(file.readline())
        fileRows = filter(None,file.read().split('\n'))
        for row in fileRows:
            self.inputForm.append(row.split(' '))

    def generateInitialSolution(self):
        self.initialSolution = random.sample(range(0, self.totalPhoto), self.totalPhoto)
        self.postProcessingInitialSolutionVerticalPhoto()
        self.calculateInitialFitnes()
        self.setActualSolution(self.initialSolution,self.initialFitness)

    def checkIfPhotosHasTagsInCommon(self,photo_1,photo_2):
        tagsPhoto_1 = self.getPhotoTags(photo_1)
        tagsPhoto_2 = self.getPhotoTags(photo_2)
        return not set(tagsPhoto_1).isdisjoint(tagsPhoto_2)

    def postProcessingInitialSolutionVerticalPhoto(self):
        for i in range(0,len(self.initialSolution),1):
            if len(self.initialSolution) > i:
                if self.getPhotoPosition(self.initialSolution[i]) == 'V':
                    photoToCombine = self.findNextVerticalPhoto(i)
                    self.initialSolution[i] = [self.initialSolution[i],photoToCombine]
                    self.initialSolution.remove(photoToCombine)
            else:
                break

    def getPhotoPosition(self,element):
        if isinstance(element,int):
            return self.inputForm[element][0]
        return "VV"

    def findNextVerticalPhoto(self,position):
        for i in range(position + 1, len(self.initialSolution), 1):
            if (self.getPhotoPosition(self.initialSolution[i]) == 'V'):
                    return self.initialSolution[i]

    def setActualSolution(self,_solution,_fitnes):
        self.actualSolution = copy.copy(_solution)
        self.actualFitness  = copy.copy(_fitnes)

    def calculateInitialFitnes(self):
        for i in range(0,len(self.initialSolution)-1,1):
            self.initialFitness = self.initialFitness + self.getMinimumBetweenTwoPhotos(self.getPhotoTags(self.initialSolution[i]),self.getPhotoTags(self.initialSolution[i+1]))

    def getMinimumBetweenTwoPhotos(self,photo1,photo2):
        countTagsOnlyPhoto1 = self.getTotalDifferentTags(photo1, photo2)
        countTagsOnlyPhoto2 = self.getTotalDifferentTags(photo2, photo1)
        countSameTags = len(photo1) - countTagsOnlyPhoto1
        return min(countTagsOnlyPhoto1, countTagsOnlyPhoto2, countSameTags)

    def getTotalDifferentTags(self,photoTags1,photoTags2):
        differentTags = list(set(photoTags1) - set(photoTags2))
        return len(differentTags)

    def getPhotoTags(self,position):
        if isinstance(position, int):
            tmp = copy.copy(self.inputForm[position])
            tmp[0:2] = []
            return tmp
        else:
            tmp_1 = copy.copy(self.inputForm[position[0]])
            tmp_1[0:2] = []
            tmp_2 = copy.copy(self.inputForm[position[1]])
            tmp_2[0:2] = []
            return self.combineTags(tmp_1,tmp_2)

    def getPhotoTags2(self,position):
        if position >= len(self.actualSolution):
            return  []
        if isinstance(self.actualSolution[position], int):
            if position < 0 or position >= len(self.initialSolution):
                return []
            tmp = copy.copy(self.inputForm[self.actualSolution[position]])
            tmp[0:2] = []
            return tmp
        else:
            tmp_1 = copy.copy(self.inputForm[self.actualSolution[position][0]])
            tmp_1[0:2] = []
            tmp_2 = copy.copy(self.inputForm[self.actualSolution[position][1]])
            tmp_2[0:2] = []
            return self.combineTags(tmp_1,tmp_2)

    def combineTags(self,photoTag1,photoTag2):
        return list(set(photoTag1) | set(photoTag2))

    def HillClimbingAlgorithm(self,iteration):
        for i in range(0, iteration, 1):
            rndTmp = random.sample(range(0, len(self.actualSolution)), 2)
            val = copy.copy(self.actualFitness)
            tmp = copy.copy(self.actualSolution)
            x = rndTmp[0]
            y = rndTmp[1]
            val= self.calculateNeighborhoodFitnessVal(val,x, y)
            if(val >= self.actualFitness):
                tmp[x], tmp[y] = tmp[y], tmp[x]
                self.actualFitness = copy.copy(val)
                self.actualSolution = copy.copy(tmp)

    def calculateNeighborhoodFitness(self,x,y):
        return  self.actualFitness  -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x-1),self.getPhotoTags2(x))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x),self.getPhotoTags2(x+1))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y-1),self.getPhotoTags2(x))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x),self.getPhotoTags2(y+1))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y-1),self.getPhotoTags2(y))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y),self.getPhotoTags2(y+1))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x-1),self.getPhotoTags2(y))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y),self.getPhotoTags2(x+1))

    def calculateNeighborhoodFitnessVal(self,actualFitnes,x,y):
        return  actualFitnes  -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x-1),self.getPhotoTags2(x))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x),self.getPhotoTags2(x+1))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y-1),self.getPhotoTags2(x))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x),self.getPhotoTags2(y+1))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y-1),self.getPhotoTags2(y))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y),self.getPhotoTags2(y+1))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x-1),self.getPhotoTags2(y))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y),self.getPhotoTags2(x+1))

    def calculateNeighborhoodFitnessValNew(self,x,y):
        return  0  -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x-1),self.getPhotoTags2(x))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x),self.getPhotoTags2(x+1))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y-1),self.getPhotoTags2(x))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x),self.getPhotoTags2(y+1))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y-1),self.getPhotoTags2(y))    \
                                    -   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(y),self.getPhotoTags2(y+1))    \
                                    +   self.getMinimumBetweenTwoPhotos(self.getPhotoTags2(x-1),self.getPhotoTags2(x+1))    \



if __name__ == "__main__":
    #file = "/home/blendarifaj/FIEK - Mater/Viti 2/Semestri 3/Algoritmet e Inspiruara nga Natyra/Detyra/qualification_round_2019.in/d_pet_pictures.txt"
    #file = "/home/blendarifaj/FIEK - Mater/Viti 2/Semestri 3/Algoritmet e Inspiruara nga Natyra/Detyra/qualification_round_2019.in/qualification_round_2019.in/c_memorable_moments.txt"
    #file = "/home/blendarifaj/FIEK - Mater/Viti 2/Semestri 3/Algoritmet e Inspiruara nga Natyra/Detyra/qualification_round_2019.in/qualification_round_2019.in/d_pet_pictures.txt"
    #file = "/home/blendarifaj/FIEK - Mater/Viti 2/Semestri 3/Algoritmet e Inspiruara nga Natyra/Detyra/qualification_round_2019.in/qualification_round_2019.in/e_shiny_selfies.txt"
    #file = "/home/blendarifaj/FIEK - Mater/Viti 2/Semestri 3/Algoritmet e Inspiruara nga Natyra/Detyra/qualification_round_2019.in/qualification_round_2019.in/b_lovely_landscapes.txt"
    file = "/home/blendarifaj/FIEK - Mater/Viti 2/Semestri 3/Algoritmet e Inspiruara nga Natyra/Detyra/qualification_round_2019.in/qualification_round_2019.in/e_shiny_selfies.txt"
    tmp = beautifulSlideShowHillClimbing(file)
    print(tmp.initialSolution)
    print(tmp.initialFitness)
    tmp.HillClimbingAlgorithm(10000)
    print(tmp.actualSolution)
    print(tmp.actualFitness)
    tmp.outputToFile()
