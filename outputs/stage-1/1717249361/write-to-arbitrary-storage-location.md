Below is a vulnerable smart contract with Write to Arbitrary Storage Location vulnerability:

```solidity
pragma solidity ^0.8.0;

contract WriteToArbitraryStorage {
    mapping(uint256 => uint256) public data;

    function writeToStorage(uint256 _index, uint256 _value) public {
        data[_index] = _value;
    }

    function exploit(address _contractAddress, uint256 _index, uint256 _value) public {
        (bool success, ) = _contractAddress.delegatecall(abi.encodeWithSignature("writeToStorage(uint256,uint256)", _index, _value));
        require(success, "Exploit failed");
    }
}
```

In the `exploit` function, the `delegatecall` is used to call the `writeToStorage` function of another contract at the specified `_contractAddress`. This allows an attacker to write to arbitrary storage locations in the `WriteToArbitraryStorage` contract.

### Remediation:

To prevent the Write to Arbitrary Storage Location vulnerability, it is important to avoid using `delegatecall` to call external contracts that can modify the storage of the current contract. Here are some remediation steps:

1. **Avoid Delegatecall**: Use `call` instead of `delegatecall` when interacting with external contracts. `call` limits the called contract's access to its own storage and prevents it from modifying the storage of the calling contract.

2. **Whitelist Trusted Contracts**: Maintain a whitelist of trusted contracts that can be interacted with using `delegatecall`. Only allow `delegatecall` to contracts on the whitelist.

3. **Use Safe Delegatecall Libraries**: If `delegatecall` is necessary, consider using safe delegatecall libraries like DSProxy to handle delegatecall operations securely.

Here is an updated version of the smart contract with the remediation applied:

```solidity
pragma solidity ^0.8.0;

contract WriteToArbitraryStorageFixed {
    mapping(uint256 => uint256) public data;
    address public trustedContract;

    constructor(address _trustedContract) {
        trustedContract = _trustedContract;
    }

    function writeToStorage(uint256 _index, uint256 _value) public {
        require(msg.sender == trustedContract, "Only trusted contract can write to storage");
        data[_index] = _value;
    }
}
```

In this fixed version, the `writeToStorage` function can only be called by the trusted contract specified during deployment. This ensures that only the trusted contract can write to the storage of the `WriteToArbitraryStorageFixed` contract, preventing unauthorized writes to arbitrary storage locations.