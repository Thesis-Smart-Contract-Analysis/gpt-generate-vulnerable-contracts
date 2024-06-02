# Smart contract

```solidity
pragma solidity ^0.4.24;

contract UntrustworthyDataFeeds {
  
  uint public price;
  
  function setPrice(uint _price) {
    price = _price;
  }
  
  function getPrice() public view returns (uint) {
    return price;
  }
  
}
```

The vulnerability lies in the `setPrice` function where the price is directly set without any validation or verification from external data feeds.

# Remediations

- Implement a mechanism to fetch price data from trusted external data feeds and update the price in the smart contract based on that data.
- Use an oracle service to securely retrieve price data and update the price in the smart contract.