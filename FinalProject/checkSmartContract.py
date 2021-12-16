from checkReentrancy import checkReentrancy
from checkUnhandleException import check_UE


if __name__ == "__main__":
    fileName = input("Enter the smart contract you want to check:");

    fd = open(fileName);

    lines = fd.readlines();

    # reentrancy, callLineIndexs, relatedFunctions = checkReentrancy(lines);

    # if reentrancy:
    #     print("Have reentrancy vulnerability!");
    #     for call in callLineIndexs:
    #         print("Related Lines: " + str(call+1));
    #     for f in relatedFunctions:
    #         print("Vulnerable Functions: " + f);

    UE, relatedLines = check_UE(lines);

    if UE:
        print("Have unhandled exception vulnerability!");
        for line in relatedLines:
            print("Related Lines: " + str(line+1));