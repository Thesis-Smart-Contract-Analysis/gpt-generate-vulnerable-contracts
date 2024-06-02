# Smart contract with Denial of Service with Block Gas Limit Vulnerability

```solidity
pragma solidity ^0.4.24;

contract DenialOfService {
    
    mapping(address => uint) public balances;

    function contribute() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() public {
        require(balances[msg.sender] > 0);
        msg.sender.transfer(balances[msg.sender]);
        balances[msg.sender] = 0;
    }

    function kill() public {
        selfdestruct(msg.sender);
    }

    function loop() public {
        while (true) {
            contribute();
        }
    }
}
```

In the `loop` function, the vulnerability lies in the infinite loop that continuously calls the `contribute` function, causing the gas to be consumed rapidly and leading to a Denial of Service with Block Gas Limit vulnerability.

# Remediations

- Implement a check to limit the number of contributions per address within a certain block to prevent excessive gas consumption.
- Use a withdrawal pattern where users can only withdraw their funds in a controlled manner to avoid potential abuse.

Remember to always consider the gas limits and potential gas costs when designing smart contracts to prevent such vulnerabilities.