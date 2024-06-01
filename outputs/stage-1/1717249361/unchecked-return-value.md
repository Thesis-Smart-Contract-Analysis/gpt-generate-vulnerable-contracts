Here is a vulnerable smart contract with Unchecked Return Value vulnerability:

```solidity
pragma solidity ^0.8.0;

contract UncheckedReturnValue {
    
    function transferFunds(address payable _recipient, uint _amount) public {
        (bool success, ) = _recipient.call{value: _amount}("");
        // No check on the success variable
    }
    
}
```

In the `transferFunds` function, the return value of the `call` function is not checked. This can lead to unexpected behavior if the call fails but the contract continues execution assuming it was successful.

### Remediation:

To remediate the Unchecked Return Value vulnerability, you should always check the return value of the `call` function to ensure the success of the external call. Here is the fixed version of the smart contract:

```solidity
pragma solidity ^0.8.0;

contract SafeTransfer {
    
    function transferFunds(address payable _recipient, uint _amount) public {
        (bool success, ) = _recipient.call{value: _amount}("");
        require(success, "Transfer failed");
    }
    
}
```

In the remediated version, the `require` statement is added to check the `success` variable after the `call` function. This ensures that the contract will revert if the external call fails, preventing any unexpected behavior.