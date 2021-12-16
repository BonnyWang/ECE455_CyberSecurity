import os;

from checkReentrancy import checkReentrancy;


if __name__ == "__main__":

    outPutResults = open("myTestResult", "w");

    for filename in os.listdir("./reentrancy"):
        contractFd = open("./reentrancy/"+filename);
        contents = contractFd.readlines();
        vulnerbal, callLineIndexs, relatedFunctions = checkReentrancy(contents);
        
        if vulnerbal:
            outPutResults.write(filename + " 1\n");
        else:
            outPutResults.write(filename + " 0\n");