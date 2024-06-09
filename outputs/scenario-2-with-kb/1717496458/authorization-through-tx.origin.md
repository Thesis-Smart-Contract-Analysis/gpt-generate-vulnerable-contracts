# Smart Contract with `tx.origin` Vulnerability

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableAuth {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function changeOwner(address _newOwner) public {
        require(tx.origin == owner, "Not owner"); // Vulnerable line: uses tx.origin for authorization
        owner = _newOwner;
    }
}
```

The vulnerability in this smart contract arises from the use of `tx.origin` to check if the caller is the owner. The `tx.origin` always refers to the original external account that started the transaction, which can lead to security issues if the transaction is initiated through intermediate contracts.

# Remediations

1. **Use `msg.sender` for Direct Authorization Checks:**
   Replace `tx.origin` with `msg.sender` to ensure that only the direct caller of the function can change the owner, which is safer and prevents unauthorized access through intermediary contracts.

   ```solidity
   require(msg.sender == owner, "Not owner");
   ```

2. **Implement More Robust Access Control:**
   Utilize established smart contract libraries such as OpenZeppelin's `Ownable` contract for managing ownership and access controls. This approach not only simplifies the code but also benefits from community-reviewed security practices.

   ```solidity
   // Import OpenZeppelin's Ownable contract
   import "@openzeppelin/contracts/access/Ownable.sol";

   contract SecureAuth is Ownable {
       function changeOwner(address _newOwner) public onlyOwner {
           transferOwnership(_newOwner);
       }
   }
   ```

By implementing these remediations, the smart contract can avoid the pitfalls associated with `tx.origin` and ensure that ownership management is secure and reliable.