Here is an example of a smart contract with Typographical Error vulnerability:

```solidity
pragma solidity ^0.8.0;

contract TypoVulnerable {
    uint public balance;

    function depoist(uint _amount) public {
        balance += _amount;
    }
}
```

In the above smart contract, there is a typographical error in the function name `depoist` instead of `deposit`. This can lead to unintended behavior and potential vulnerabilities in the contract.

To remediate the Typographical Error vulnerability, you should correct the function name to `deposit` to ensure that the function is correctly called and executed as intended. Here is the remediated version of the smart contract:

```solidity
pragma solidity ^0.8.0;

contract TypoFixed {
    uint public balance;

    function deposit(uint _amount) public {
        balance += _amount;
    }
}
```

By fixing the typographical error in the function name, you can prevent potential issues and ensure that the smart contract functions as expected.