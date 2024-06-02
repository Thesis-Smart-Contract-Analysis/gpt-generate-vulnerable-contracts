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

## Description

The vulnerability in the smart contract `UntrustworthyDataFeeds` lies in the fact that the `price` variable can be manipulated directly by calling the `setPrice` function. This allows anyone to set the price to any value without any restrictions or validations.

## Remediations

- Implement access control mechanisms to restrict who can call the `setPrice` function. This can be achieved by using modifiers or access control patterns like Ownable.
- Consider using an Oracle service to fetch external data feeds securely and update the price variable based on the data retrieved from the Oracle. This ensures that the price is coming from a trusted source rather than being set directly by external users.