# Smart contract with Denial of Service with Block Gas Limit Vulnerability

```solidity
pragma solidity ^0.8.0;

contract DenialOfService {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdrawAll() public {
        uint amount = balances[msg.sender];
        require(amount > 0, "Insufficient balance");

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        balances[msg.sender] = 0;
    }

    function() external payable {
        while (true) {
            deposit(); // Repeatedly deposit to consume all gas
        }
    }
}
```

## Description
The vulnerability in the smart contract lies in the fallback function that calls the `deposit` function repeatedly, consuming all available gas. This can lead to a denial of service attack with the block gas limit, preventing other transactions from being processed.

## Remediations
- Implement a gas limit check in the fallback function to prevent consuming all gas.
- Use a withdrawal pattern where users need to explicitly withdraw funds instead of automatically withdrawing in the fallback function.