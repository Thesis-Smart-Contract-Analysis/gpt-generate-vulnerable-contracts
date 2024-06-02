# Smart contract

```solidity
pragma solidity ^0.4.24;

contract VulnerableContract {
    string public name;

    function setName(string _name) public {
        name = _name;
    }

    function setNameWithOverride(string _name) public {
        name = "\u202e" + _name; // Right-To-Left Override Control Character vulnerability
    }
}
```

Description: The `setNameWithOverride` function in the smart contract `VulnerableContract` contains a vulnerability where the `name` variable is set with a Right-To-Left Override Control Character. This character can be used maliciously to visually reverse text and potentially deceive users.

# Remediations

- Ensure that user input is properly validated and sanitized before setting any string variables.
- Avoid using special characters that can alter the visual representation of text in sensitive areas of the smart contract.