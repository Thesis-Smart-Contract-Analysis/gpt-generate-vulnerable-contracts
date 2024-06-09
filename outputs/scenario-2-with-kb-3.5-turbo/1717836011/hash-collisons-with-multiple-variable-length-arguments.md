# Smart contract

```solidity
/*
 * @author: Steve Marx
 * Modified by Kaden Zipfel
 */
pragma solidity ^0.5.0;

import "./ECDSA.sol";

contract AccessControl {
  
  using ECDSA for bytes32;
  mapping(address => bool) isAdmin;
  mapping(address => bool) isRegularUser;
  // Add admins and regular users.
  function addUsers(
    address[] calldata admins,
    address[] calldata regularUsers,
    bytes calldata signature
  )
      external
  {
    if (!isAdmin[msg.sender]) {
      // Allow calls to be relayed with an admin's signature.
      bytes32 hash = keccak256(abi.encodePacked(admins, regularUsers)); // Vulnerable line
      address signer = hash.toEthSignedMessageHash().recover(signature);
      require(isAdmin[signer], "Only admins can add users.");
    }
    for (uint256 i = 0; i < admins.length; i++) {
      isAdmin[admins[i]] = true;
    }
    for (uint256 i = 0; i < regularUsers.length; i++) {
      isRegularUser[regularUsers[i]] = true;
    }
  }
    
}
```

## Description

The vulnerability in the smart contract `AccessControl` lies in the line where `abi.encodePacked` is used to hash multiple variable-length arrays (`admins` and `regularUsers`). This can lead to hash collisions, allowing an attacker to manipulate the input arrays to generate the same hash value, bypassing the authentication check and potentially gaining unauthorized access.

# Remediations

- **Remediation 1:** Use fixed-length arrays instead of variable-length arrays in the `addUsers` function to prevent hash collisions with multiple variable-length arguments. This ensures that the input size is fixed and known, reducing the risk of collisions.

- **Remediation 2:** Implement stricter input validation and authentication mechanisms to verify the integrity of the input data and signatures, ensuring that only authorized users can modify the access control lists. Consider using more secure hashing algorithms or cryptographic techniques to enhance the security of the authentication process.