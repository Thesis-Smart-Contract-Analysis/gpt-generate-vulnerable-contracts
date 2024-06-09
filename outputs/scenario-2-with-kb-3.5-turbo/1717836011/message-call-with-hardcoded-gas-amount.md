# Smart contract

```solidity
pragma solidity 0.6.4;

interface ICallable {
  function callMe() external;
}

contract HardcodedNotGood {

  address payable _callable = 0xaAaAaAaaAaAaAaaAaAAAAAAAAaaaAaAaAaaAaaAa;
  ICallable callable = ICallable(_callable);

  constructor() public payable {
  }

  function doTransfer(uint256 amount) public {
    _callable.transfer(amount); // Vulnerability: Hardcoded gas amount in transfer function
  }

  function doSend(uint256 amount) public {
    _callable.send(amount); // Vulnerability: Hardcoded gas amount in send function
  }

   function callLowLevel() public {
     _callable.call.value(0).gas(10000)(""); // Vulnerability: Hardcoded gas amount in low-level call
   }

   function callWithArgs() public {
     callable.callMe{gas: 10000}();
   }
   
}
```

Description of the vulnerability: The vulnerabilities in the smart contract arise from the hardcoded gas amounts used in the `transfer`, `send`, and low-level `call` functions. Hardcoding gas amounts can lead to unexpected behavior due to changes in gas costs for EVM operations, potentially exposing the contract to re-entrancy attacks and other security risks.

# Remediations

- **Remediation 1:** Avoid using `transfer` and `send` functions as they provide a fixed amount of gas which may not be sufficient for complex operations. Instead, consider using `address.call{value: amount}("")` and specify the gas limit dynamically based on the gas requirements of the called function.

- **Remediation 2:** When using the low-level `call` function, avoid hardcoding the gas amount. Calculate the gas required for the operation dynamically based on the specific requirements of the called function. This ensures that the contract can adapt to changes in gas costs and remains secure against potential vulnerabilities.