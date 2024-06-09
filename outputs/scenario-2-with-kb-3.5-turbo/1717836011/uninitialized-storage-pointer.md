# Smart contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

contract StorageLayout {
    bool public unlocked = false; // slot 0
    struct NameRecord { // map hashes to addresses
        bytes32 name;
        address mappedAddress;
    }
    
    mapping(address => NameRecord) public registeredNameRecord; // slot 1
    mapping(bytes32 => address) public resolve; // slot 2
    
    function register(bytes32 _name, address _mappedAddress) public {
        // set up the new NameRecord
        NameRecord newRecord;
        newRecord.name = _name;
        newRecord.mappedAddress = _mappedAddress;
        
        resolve[_name] = _mappedAddress;
        registeredNameRecord[msg.sender] = newRecord;
        
        require(unlocked); // only allow registrations if contract is unlocked
    }
}
```

Description of the vulnerability: In the `register` function of the `StorageLayout` contract, the `NameRecord newRecord;` variable is declared without specifying a data location. This causes `newRecord` to default to the `storage` data location, making it act as a pointer to the storage slot 0 where the `unlocked` variable is stored. As a result, assigning a value to `newRecord.name` in the function can inadvertently modify the `unlocked` state variable.

# Remediations

- Specify the data location explicitly for the `newRecord` variable to avoid it pointing to storage slots unintentionally. For example, you can declare `NameRecord storage newRecord;` to ensure it operates in the storage data location explicitly.
- Ensure that all variables, especially those that could potentially point to storage slots, are properly initialized before use to prevent unintended modifications to state variables.