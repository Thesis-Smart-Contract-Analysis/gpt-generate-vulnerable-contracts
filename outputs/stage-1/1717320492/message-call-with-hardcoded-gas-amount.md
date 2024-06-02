# Smart contract

```solidity
pragma solidity ^0.4.24;

contract MessageCallWithHardcodedGasAmount {
    
    function sendMessage(address _recipient) public {
        _recipient.call.value(1 ether).gas(2300)(""); // Vulnerable line
    }
    
}
```

## Description

In the smart contract `MessageCallWithHardcodedGasAmount`, the `sendMessage` function contains a vulnerability where the gas amount for the message call is hardcoded to 2300. Hardcoding the gas amount can lead to unexpected behavior or failed transactions, especially if the called function requires more gas to execute.

## Remediations

- Use the `gasleft()` function to dynamically determine the available gas for the message call.
- Allow the caller to specify the gas amount for the message call as a parameter to the function.
- Implement proper error handling and fallback mechanisms in case the message call runs out of gas.