# Smart contract with Authorization through `tx.origin` vulnerability

```solidity
// Vulnerable code
contract VulnerableContract {
    
    address public owner;
    
    constructor() {
        owner = tx.origin; // Vulnerability here
    }
    
    function transferOwnership(address newOwner) public {
        require(tx.origin == owner, "Only owner can transfer ownership");
        owner = newOwner;
    }
}
```

Description of the vulnerability in the above smart contract:
The vulnerability lies in the constructor of the `VulnerableContract` where it assigns the `tx.origin` as the owner. This allows an attacker to manipulate the `tx.origin` value during contract deployment and take over the ownership of the contract.

# Remediations

- **Remediation 1**: Replace `tx.origin` with `msg.sender` for authentication.
  
  ```solidity
  contract SecureContract {
      
      address public owner;
      
      constructor() {
          owner = msg.sender; // Fixed
      }
      
      function transferOwnership(address newOwner) public {
          require(msg.sender == owner, "Only owner can transfer ownership");
          owner = newOwner;
      }
  }
  ```

- **Remediation 2**: Implement access control using a modifier to ensure only the owner can perform certain actions.

  ```solidity
  contract SecureContract {
      
      address public owner;
      
      constructor() {
          owner = msg.sender;
      }
      
      modifier onlyOwner() {
          require(msg.sender == owner, "Only owner can call this function");
          _;
      }
      
      function transferOwnership(address newOwner) public onlyOwner {
          owner = newOwner;
      }
  }
  ```