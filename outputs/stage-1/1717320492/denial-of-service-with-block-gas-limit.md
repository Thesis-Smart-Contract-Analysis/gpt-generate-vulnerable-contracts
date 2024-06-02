# Smart contract

```solidity
pragma solidity ^0.4.24;

contract DenialOfService {
    mapping(address => uint) public balances;

    function contribute() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint amount = balances[msg.sender];
        require(amount > 0);
        msg.sender.transfer(amount);
        balances[msg.sender] = 0;
    }

    function() public payable {
        while (true) {
            contribute();
        }
    }
}
```

## Description

The vulnerability in the smart contract `DenialOfService` lies in the fallback function that creates a denial of service attack by continuously contributing funds to the contract, causing it to consume all available gas in a single transaction.

## Remediations

- Implement a gas limit check in the fallback function to prevent excessive gas consumption.
- Add a mechanism to limit the number of contributions per transaction to avoid potential abuse.