import nltk;

def detectCallInvocation(lines):
    callLineIndexs = [];
    containsCall = False;
    for index,line in enumerate(lines):
        if (".call." in line) or (".call{{" in line):
            
            # check if the value is set to 0, otherwise it is still safe
            if("value(0)" in line) or ("value: 0" in line):
                return False, callLineIndexs;
            else:
                callLineIndexs.append(index);
                containsCall = True;
            
    return containsCall, callLineIndexs;


def detectBalanceDeduction(lines, callLineIndexs):

    # balanceDeducted = True;

    for lineIndex in callLineIndexs:
        tempLineIndex = lineIndex;
        while tempLineIndex > 0:
            tempLineIndex -= 1;
            line = lines[tempLineIndex];

            if ("alances[msg.sender]" in line) or ("alance[msg.sender]" in line):
                if ('0' in line) or ('-' in line):
                    callLineIndexs.remove(lineIndex);
                    # escape since this call is safe, check next call function
                    break;
            
            # Scope level check
            if ("{" in line) and ("}" not in line):
                return False, callLineIndexs;
            
            # Function level check
            if "function" in line:
                return False, callLineIndexs;
    
    # All call are checked with coexist of deduction inside the scope
    return True, callLineIndexs;

def detectModifier(lines, callLineIndexs):
    for lineIndex in callLineIndexs:
        modifierName = "onlyOwner";

        updatedModifier = False;

        tempIndex = lineIndex;

        while tempIndex > 0:
            tempIndex -= 1;
            line = lines[tempIndex];

            if ("function" in line) and (modifierName in line):
                # Safe check next call function
                callLineIndexs.remove(lineIndex);
                break;
            
            if ("require(msg.sender==owner)" in line.replace(" ", "")) and (not updatedModifier):
                modifierIndex = tempIndex;
                while modifierIndex > 0:
                    modifierIndex -= 1;
                    subline = lines[modifierIndex];
                    if "modifier" in subline:
                        modifierName = nltk.word_tokenize(subline)[1];
                        
                        # recheck all
                        tempIndex = lineIndex;
                        updatedModifier = True;

        if tempIndex == 0:
            return False, callLineIndexs;
        return True,callLineIndexs;
    
    # All the call fucntion has the corresponding modifier
    return False,callLineIndexs;

# find the function given current index
def findFunction(lines, index):
    while index > 0:
        index -= 1;

        if "function" in lines[index]:
            return nltk.word_tokenize(lines[index])[1], index;

def findVulnerFunction(lines, callLineIndexs):
    functions = [];
    functionLineIndex = [];
    for lineIndex in callLineIndexs:
        f , i =findFunction(lines, lineIndex);
        functions.append(f);
        functionLineIndex.append(i);
    
    for index,line in enumerate(lines):
        for f in functions:
            if (str(f+"(") in line) and (index not in functionLineIndex):
                f, i = findFunction(lines, index);
                functions.append(f);
    
    return functions;
                

                


    


# Check Reentrancy vulnerbility
def checkReentrancy(lines):

    containsCall, callLineIndexs =  detectCallInvocation(lines);

    relatedFunctions = [];

    if containsCall:
        balanceDeduced, callLineIndexs = detectBalanceDeduction(lines, callLineIndexs);
        modifierPresented, callLineIndexs = detectModifier(lines, callLineIndexs);
        
        if (not balanceDeduced) and (not modifierPresented):
            relatedFunctions = findVulnerFunction(lines, callLineIndexs);
            return True, callLineIndexs, relatedFunctions;
        return False, callLineIndexs, relatedFunctions;
    else:
        return False, callLineIndexs, relatedFunctions;

if __name__ == "__main__":
    contract = input("Enter the smart contract to check:");
    
    fd = open(contract);

    lines = fd.readlines();

    print(checkReentrancy(lines));