```solidity
// Smart Contract with Typographical Error Vulnerability

pragma solidity ^0.8.0;

contract TypoVulnerable {
    uint public totalSupply;

    // Function to mint new tokens with a typographical error
    function mint(uint _amount) public {
        totalSuply += _amount; // Typo: totalSuply instead of totalSupply
    }
}
```

### Remediation:
To fix the Typographical Error Vulnerability in the smart contract, the typo in the variable name `totalSuply` should be corrected to `totalSupply` in the `mint` function. Here is the corrected version of the smart contract:

```solidity
// Smart Contract with Typographical Error Vulnerability Remediated

pragma solidity ^0.8.0;

contract TypoVulnerable {
    uint public totalSupply;

    // Function to mint new tokens with the typo corrected
    function mint(uint _amount) public {
        totalSupply += _amount; // Typo corrected: totalSupply
    }
}
```

By correcting the typo in the variable name, the smart contract will function as intended without the Typographical Error Vulnerability.