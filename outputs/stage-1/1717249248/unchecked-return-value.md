Below is a vulnerable smart contract with Unchecked Return Value vulnerability:

```solidity
pragma solidity ^0.8.0;

contract UncheckedReturnValue {
    
    function transferFunds(address payable recipient, uint amount) public {
        (bool success, ) = recipient.call{value: amount}("");
        // No check on the success variable
    }
    
}
```

In the `transferFunds` function of the smart contract `UncheckedReturnValue`, the return value of the `call` function is not checked. This can lead to unexpected behavior if the `call` fails but the contract continues execution assuming it was successful.

### Remediation:

To mitigate the Unchecked Return Value vulnerability, you should always check the return value of the `call` function to ensure the success of the external call. Here is the remediated version of the smart contract:

```solidity
pragma solidity ^0.8.0;

contract CheckedReturnValue {
    
    function transferFunds(address payable recipient, uint amount) public {
        (bool success, ) = recipient.call{value: amount}("");
        require(success, "Transfer failed");
    }
    
}
```

In the remediated version, the return value of the `call` function is checked using `require(success, "Transfer failed")`. This ensures that the function execution will revert if the external call fails, preventing any unexpected behavior.