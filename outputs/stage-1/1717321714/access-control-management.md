# Smart contract with Access Control Management vulnerability

```solidity
pragma solidity ^0.4.24;

contract AccessControlVulnerable {
  
  address public owner;

  function AccessControlVulnerable() {
    owner = msg.sender;
  }

  function changeOwner(address _newOwner) {
    owner = _newOwner;
  }

}
```

In the above smart contract `AccessControlVulnerable`, the vulnerability lies in the `changeOwner` function where anyone can change the owner of the contract without any access control checks.

# Description

The `changeOwner` function allows any caller to change the `owner` of the contract without any access control checks. This can lead to unauthorized ownership changes and potential security risks.

# Remediations

- Implement access control checks in the `changeOwner` function to restrict ownership changes to authorized addresses only.
- Use modifiers like `onlyOwner` to ensure that only the designated owner can change the ownership of the contract.