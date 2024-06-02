# Smart contract

```solidity
pragma solidity ^0.4.24;

contract VulnerableContract {
    string public name;

    function setName(string _name) public {
        name = "\u202e" + _name; // Right-To-Left Override Control Character vulnerability
    }
}
```

Description: The vulnerability lies in the `setName` function where the `name` variable is set with a string that includes the Right-To-Left Override Control Character (`\u202e`). This character can be used maliciously to reverse the text direction and potentially deceive users.

# Remediations

- Ensure input validation to prevent the inclusion of special characters like the Right-To-Left Override Control Character.
- Use libraries or functions that sanitize input to remove any potentially harmful characters before setting variables.

Remember to always validate and sanitize user input to prevent such vulnerabilities in your smart contracts.