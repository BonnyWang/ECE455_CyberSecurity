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
        while lineIndex > 0:
            lineIndex -= 1;
            line = lines[lineIndex];

            if ("alances[msg.sender]" in line) or ("alance[msg.sender]" in line):
                if ('0' in line) or ('-' in line):
                    
                    # escape since this call is safe, check next call function
                    break;
            
            # Scope level check
            if ("{" in line) and ("}" not in line):
                return False;
            
            # Function level check
            if "function" in line:
                return False;
    
    # All call are checked with coexist of deduction inside the scope
    return True;

def detectModifier(lines, callLineIndexs):
    for lineIndex in callLineIndexs:
        modifierName = "onlyOwner";

        tempIndex = lineIndex;

        while tempIndex > 0:
            tempIndex -= 1;
            line = lines[tempIndex];

            if ("function" in line) and (modifierName in line):
                # Safe check next call function
                break;
            
            if "require(msg.sender==owner)" in line.replace(" ", ""):
                modifierIndex = tempIndex;
                while modifierIndex > 0:
                    modifierIndex -= 1;
                    subline = lines[modifierIndex];
                    if "modifier" in subline:
                        modifierName = subline.replace("modifier","").replace("()","").replace("{", "").replace(" ", "").strip();
                        
                        # recheck all
                        tempIndex = lineIndex;

        if tempIndex == 0:
            return False;
        return True;
    
    # All the call fucntion has the corresponding modifier
    return False;



# Check Reentrancy vulnerbility
def checkReentrancy(lines):

    containsCall, callLineIndexs =  detectCallInvocation(lines);

    if containsCall:
        balanceDeduced = detectBalanceDeduction(lines, callLineIndexs);
        modifierPresented = detectModifier(lines, callLineIndexs);
        
        if (not balanceDeduced) and (not modifierPresented):
            return True;
        return False;
    else:
        return False;

if __name__ == "__main__":
    contract = input("Enter the smart contract to check:");
    
    fd = open(contract);

    lines = fd.readlines();

    print(checkReentrancy(lines));




# TODO: check cross function vulnerbility