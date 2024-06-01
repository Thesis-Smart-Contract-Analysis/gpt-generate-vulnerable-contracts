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

To fix the Floating Compiler Version vulnerability, you should specify a fixed version of the Solidity compiler in the pragma statement. Here is the remediated version of the smart contract:

```solidity
// Remediated Smart Contract with Fixed Compiler Version

pragma solidity 0.5.16;

contract FixedCompilerVersion {
    uint public data;

    function setData(uint _data) public {
        data = _data;
    }
}
```

By specifying a fixed version of the Solidity compiler in the pragma statement (in this case, version 0.5.16), you ensure that the smart contract will be compiled using a specific version of the compiler, reducing the risk of vulnerabilities related to floating compiler versions.