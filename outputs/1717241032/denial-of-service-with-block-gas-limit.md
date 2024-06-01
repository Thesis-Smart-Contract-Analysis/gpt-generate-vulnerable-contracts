Below is a vulnerable smart contract that exhibits Denial of Service with Block Gas Limit vulnerability:

```solidity
// Vulnerable smart contract with Denial of Service with Block Gas Limit vulnerability
// This contract is vulnerable to a DoS attack by consuming all gas in a single transaction

pragma solidity ^0.8.0;

contract DoSBlockGasLimit {
    mapping(uint => uint) public values;

    function addValue(uint _index, uint _value) public {
        values[_index] = _value;
    }

    function consumeGas(uint _index) public {
        while(true) {
            values[_index] += 1;
        }
    }
}
```

In the above smart contract, the `consumeGas` function contains a `while` loop that runs indefinitely, consuming all the gas in a single transaction. This can lead to a Denial of Service (DoS) attack by blocking other transactions from being processed due to the high gas consumption.

### Remediation:

To mitigate the Denial of Service with Block Gas Limit vulnerability, you can implement gas limits and use checks to prevent excessive gas consumption. Here is an updated version of the smart contract with gas limit and checks:

```solidity
// Updated smart contract with gas limit and checks to prevent DoS attack

pragma solidity ^0.8.0;

contract DoSBlockGasLimitFixed {
    mapping(uint => uint) public values;

    function addValue(uint _index, uint _value) public {
        values[_index] = _value;
    }

    function consumeGas(uint _index) public {
        uint gasToUse = 10000; // Set a reasonable gas limit
        uint gasUsed = 0;

        while(gasUsed < gasToUse) {
            values[_index] += 1;
            gasUsed = gasleft(); // Check remaining gas
        }
    }
}
```

In the updated smart contract, the `consumeGas` function now includes a gas limit (`gasToUse`) and a check to ensure that the gas consumption does not exceed the specified limit. This helps prevent excessive gas consumption and mitigates the risk of a DoS attack with Block Gas Limit vulnerability.