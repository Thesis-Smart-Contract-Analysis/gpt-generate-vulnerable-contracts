# Smart contract

```solidity
pragma solidity ^0.5.0;

contract MaliciousToken {
    string public name;

    constructor(string memory _name) public {
        name = _name;
    }

    function setName(string memory _name) public {
        name = _name;
    }
}
```

Description of the vulnerability in the above smart contract:

The vulnerability in the smart contract lies in the `setName` function where an attacker can exploit the Right-To-Left Override Control Character vulnerability by inserting the U+202E character to manipulate the display order of characters in the `_name` parameter. This can lead to misleading or obfuscated information being displayed to users, potentially causing confusion or deception.

# Remediations

- Implement input validation: Before setting the `name` variable, validate the input string to ensure it does not contain any control characters, including the Right-To-Left Override Control Character (U+202E). Reject any input that contains such characters.
- Sanitize user input: Use a function to sanitize user input by removing or replacing any potentially harmful characters, including control characters like U+202E, before assigning the input to the `name` variable. This helps prevent unexpected behavior due to maliciously crafted input.