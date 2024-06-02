# Smart contract

```solidity
pragma solidity ^0.4.24;

contract UntrustworthyDataFeeds {
  
  uint public price;
  
  function updatePrice(uint _newPrice) {
    price = _newPrice;
  }
  
  function getPrice() public view returns (uint) {
    return price;
  }
  
}
```

The vulnerability lies in the `updatePrice` function where the price is directly updated without any validation or verification from external data feeds.

# Remediations

- Implement a mechanism to fetch price data from trusted external data feeds or oracles to update the price in the smart contract.
- Use a decentralized oracle service to securely retrieve external data and update the price in the smart contract.