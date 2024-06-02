# Smart contract

```solidity
pragma solidity ^0.4.24;

contract MaliciousCode {

  address public trustedContract;

  function setTrustedContract(address _contract) public {
    trustedContract = _contract;
  }

  function executeMaliciousCode() public {
    require(trustedContract != address(0));
    trustedContract.call(bytes4(keccak256("withdrawAll()")));
  }

}
```

The vulnerability lies in the line `trustedContract.call(bytes4(keccak256("withdrawAll()")));` where the smart contract `MaliciousCode` is calling an external contract's function without proper validation or control.

# Remediations

- Ensure that the `trustedContract` address is set to a trusted and secure contract that you have control over.
- Implement access control mechanisms to restrict which contracts can be called using `delegatecall` or `call` functions.