# Smart contract

```solidity
pragma solidity ^0.8.0;

contract AccessControlVulnerability {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address newOwner) public {
        owner = newOwner; // Vulnerable line
    }

    function withdrawFunds() public {
        require(msg.sender == owner, "Only owner can withdraw funds");
        payable(owner).transfer(address(this).balance);
    }
}
```

Description of the vulnerability: The vulnerability in this smart contract lies in the `transferOwnership` function where it allows anyone to change the owner of the contract without any access control check. This can lead to unauthorized ownership changes and potential misuse of contract funds.

# Remediations

- Implement access control modifiers: Use access control modifiers like `onlyOwner` to restrict certain functions to be executed only by the owner of the contract. This ensures that critical functions can only be accessed by authorized parties.
- Use OpenZeppelin's Ownable contract: Utilize OpenZeppelin's Ownable contract which provides a secure way to manage ownership and access control in smart contracts. This helps in preventing unauthorized access to sensitive functions.