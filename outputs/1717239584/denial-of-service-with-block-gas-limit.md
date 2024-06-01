```solidity
// Smart contract vulnerable to Denial of Service with Block Gas Limit

pragma solidity ^0.8.0;

contract DoSBlockGasLimit {
    
    mapping(uint => uint) public data;

    function addToData(uint _index, uint _value) public {
        data[_index] = _value;
    }

    function consumeGas() public {
        for (uint i = 0; i < 1000000; i++) {
            data[i] = i;
        }
    }
}
```

In the smart contract `DoSBlockGasLimit` above, the `consumeGas` function contains a loop that iterates a large number of times (1,000,000 iterations) and writes to the `data` mapping. This can consume a significant amount of gas and potentially exceed the block gas limit, causing a denial of service (DoS) attack.

### Remediation:

To mitigate the Denial of Service with Block Gas Limit vulnerability, you can consider the following remediation steps:

1. **Gas Limit Check**: Implement gas limit checks in functions that involve loops or potentially consume a large amount of gas. This can prevent the function from consuming excessive gas and causing a DoS attack.

2. **Gas-Efficient Code**: Optimize the code to be more gas-efficient. Avoid unnecessary loops or operations that consume a lot of gas. Consider breaking down large operations into smaller chunks that can be executed over multiple transactions.

3. **Gas Refund**: If possible, design the contract in a way that allows users to recover gas costs in case of failed transactions. This can help prevent DoS attacks by discouraging attackers from consuming excessive gas without achieving their goal.

By implementing these remediation steps, you can reduce the risk of Denial of Service attacks with Block Gas Limit vulnerabilities in your smart contracts.