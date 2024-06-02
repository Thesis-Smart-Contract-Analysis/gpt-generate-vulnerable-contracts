# Smart contract

```solidity
pragma solidity ^0.8.0;

contract ArbitraryStorage {

    mapping(uint256 => uint256) public data;

    function writeToArbitraryStorage(uint256 _index, uint256 _value) public {
        data[_index] = _value; // Vulnerable line
    }
}
```

The vulnerability lies in the line where the function `writeToArbitraryStorage` writes to the `data` mapping at an arbitrary index specified by `_index`, allowing potential attackers to manipulate storage at unintended locations.

# Remediations

- Use a whitelist approach to restrict storage writes to specific indices only.
- Implement access control mechanisms to ensure only authorized users can write to storage locations.
- Consider using a fixed-size array or a more structured storage layout to prevent arbitrary writes.