# Smart contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract Foo {
    Bar bar;

    constructor(address _bar) {
        bar = Bar(_bar); // Vulnerable line
    }

    function callBar() public {
        bar.log();
    }
}

contract Bar {
    event Log(string message);

    function log() public {
        emit Log("Bar was called");
    }
}

contract Mal {
    event Log(string message);

    function log() public {
        emit Log("Mal was called");
    }
}
```

Description of the vulnerability: The vulnerability lies in the constructor of the `Foo` contract where an external contract address is passed and then typecasted to the `Bar` contract. This can lead to hiding malicious code from users who may not be aware of the actual contract being used.

# Remediations

- **Remediation 1:** Initialize a new instance of the smart contract within the constructor to ensure the correct contract is being used.
- **Remediation 2:** Use the `public` visibility modifier for the entity variable to allow users to verify the source code of the smart contract before executing functions.