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
        while lineIndex > 0:
            lineIndex -= 1;
            line = lines[lineIndex];

            if ("function" and "onlyOwner") in line:
                # Safe check next call function
                break;

        return False;
    
    # All the call fucntion has the corresponding modifier
    return True;



# Check Reentrancy vulnerbility
def checkReentrancy(name):
    fd = open(name);

    lines = fd.readlines();

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
    

    print(checkReentrancy(contract));




# modifier onlyOwner() 
# require(msg.sender == owner);
# function forwardFunds()??? internal onlyOwner


# Dangerous pattern
# function forwardFunds() internal {
    # 5.    wallet.call.value(msg.value).gas(10000000)();
    # 6.    balances[wallet] -= msg.value;
    # 7.  }

# def detectFunction():





# If no protection above, check if there exist a modifier constraints protection
# def checkModifierConstraints():

# Important practice: mark untrusted function, if the untrusted function call another untrusted function, then it is also untrusted
# function untrustedWithdraw() public {
#     uint256 amount = balances[msg.sender];
#     require(msg.sender.call.value(amount)());
#     balances[msg.sender] = 0;
# }

# function untrustedSettleBalance() external {
#     untrustedWithdraw();
# }

# Suggest changes 
# checks-effects-interactions pattern
# Suggest : mutex pattern