```solidity
// Vulnerable Smart Contract with Floating Compiler Version

pragma solidity >=0.4.0 <0.6.0;

contract FloatingCompilerVersion {
    uint public data;

    function setData(uint _data) public {
        data = _data;
    }
}
```

### Remediation:

To fix the Floating Compiler Version vulnerability, you should specify a fixed compiler version in the pragma statement. Here is the remediated version of the smart contract:

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

By specifying a fixed compiler version in the pragma statement, you ensure that the smart contract is compiled using a specific version of the Solidity compiler, reducing the risk of compatibility issues and vulnerabilities related to floating compiler versions.