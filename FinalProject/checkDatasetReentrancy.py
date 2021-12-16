from checkReentrancy import checkReentrancy


if __name__ == "__main__":
    
    dataNames = open("final_reentrancy_name.txt");

    outPutResults = open("myTestResult", "w");

    smartContracts = dataNames.readlines();

    for contract in smartContracts:
        # Fix the path
        contract = contract.strip();
        contract = "./sourcecode/" + contract;
        
        contractFd = open(contract);

        contents = contractFd.readlines();
        if checkReentrancy(contents):
            outPutResults.write("1\n");
        else:
            outPutResults.write("0\n");
        