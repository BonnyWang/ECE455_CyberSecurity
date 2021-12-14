# Safe
patternSafe = ["call.value(0)"];

# If the funciton does not invoke call value then safe
# TODO detect a call.value and check whether the balance is deducted before
# balances[msg.sender] = balances[msg.sender] - _value;
# assert(msg.sender.call.value(_value)(_data));

TODO 
# modifier onlyOwner() 
# require(msg.sender == owner);
# function forwardFunds()??? internal onlyOwner


# Dangerous pattern
# function forwardFunds() internal {
    # 5.    wallet.call.value(msg.value).gas(10000000)();
    # 6.    balances[wallet] -= msg.value;
    # 7.  }

def detectFunction():

# Function to detect whether call.value is used in function and whether it is followed by the value(0) pattern, if not check other safe contraints.
def detectCallInvocation():

def detectBalanceDeduction():

# If no protection above, check if there exist a modifier constraints protection
def checkModifierConstraints():

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