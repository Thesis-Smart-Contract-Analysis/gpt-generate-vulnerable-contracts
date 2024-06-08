# Smart contract

```solidity
pragma solidity ^0.8.0;

contract VulnerableContract {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address newOwner) public {
        owner = newOwner; // Vulnerability: Lack of proper signature verification
    }
}
```

Description of the vulnerability in the above smart contract:
The vulnerability in the smart contract is the lack of proper signature verification in the `transferOwnership` function. The function allows anyone to change the `owner` of the contract without verifying the authenticity of the caller's signature, leading to unauthorized ownership transfers.

# Remediations

- Remediation 1:
Implement proper signature verification using the `ecrecover` function to ensure that only authorized parties can change the ownership of the contract. This involves passing the signature parameters (v, r, s) along with the message hash to `ecrecover` and verifying that the recovered address matches the expected owner.

- Remediation 2:
Utilize access control mechanisms such as OpenZeppelin's Ownable contract to manage ownership and permission control in a more secure and standardized manner. By inheriting from Ownable, you can ensure that only the contract owner can execute sensitive functions like `transferOwnership`.