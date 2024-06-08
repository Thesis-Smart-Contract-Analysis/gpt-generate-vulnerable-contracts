# Smart contract

```solidity
pragma solidity ^0.8.0;

contract CallToTheUnknown {
    
    function call(address _addr) external payable {
        (bool success, bytes memory data) = _addr.call{value: msg.value, gas: 5000}(abi.encodeWithSignature("foo(string,uint256)", "call foo", 123));
    }
    
}
```

Description of the vulnerability in the above smart contract:
The vulnerability in the smart contract lies in the `call` function where it attempts to call a function on the address `_addr` using `abi.encodeWithSignature`. If the function with the specified signature does not exist on the target contract, the fallback function of the target contract will be invoked unexpectedly, potentially leading to unintended behavior or exploits.

# Remediations

- Use the `call` function with a specific return type to handle potential errors and prevent unintended fallback invocation.
- Implement a whitelist mechanism to only allow calls to known and trusted contracts to mitigate the risk of calling unknown functions.