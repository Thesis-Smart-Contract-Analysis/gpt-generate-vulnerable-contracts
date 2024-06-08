# Smart contract

```solidity
pragma solidity 0.4.24;

contract Missing {
  
  address private owner;

  modifier onlyowner {
    require(msg.sender==owner);
    _;
  }

  function missing() public { // Line with Incorrect Constructor Name vulnerability
    owner = msg.sender;
  }

  function () payable { } 

  function withdraw() public onlyowner {
   owner.transfer(this.balance);
  }
  
}
```

Description of the vulnerability: The smart contract `Missing` has a vulnerability due to the incorrect constructor name. The function `missing` is intended to be a constructor but is named differently, allowing anyone to call it and become the owner of the contract.

# Remediations

- Upgrade the Solidity version to 0.4.22 or higher where the constructor name should be explicitly defined as `constructor`.
- Rename the function `missing` to `constructor` to ensure it functions as the actual constructor of the smart contract.