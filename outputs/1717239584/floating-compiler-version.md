```solidity
// Vulnerable Smart Contract with Floating Compiler Version

pragma solidity >=0.4.0 < 0.6.0;

contract FloatingCompilerVersion {
    uint public data;

    function setData(uint _data) public {
        data = _data;
    }
}
```

## Remediation:

To fix the Floating Compiler Version vulnerability in the smart contract, you should specify a fixed compiler version in the pragma statement. This will ensure that the smart contract is compiled using a specific version of the Solidity compiler.

```solidity
// Fixed Smart Contract with Specific Compiler Version

pragma solidity 0.5.16;

contract FixedCompilerVersion {
    uint public data;

    function setData(uint _data) public {
        data = _data;
    }
}
```

By specifying a fixed compiler version in the pragma statement, you eliminate the risk of using outdated or potentially vulnerable compiler versions. It is recommended to always use a specific and up-to-date compiler version to ensure the security and reliability of your smart contracts.