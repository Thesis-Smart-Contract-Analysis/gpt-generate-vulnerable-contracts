Below is a vulnerable smart contract that has the "Hiding Malicious Code with External Contract" vulnerability:

```solidity
pragma solidity ^0.8.0;

interface MaliciousContract {
    function stealFunds(address _to, uint _amount) external;
}

contract VulnerableContract {
    MaliciousContract public maliciousContract;

    constructor(address _maliciousContractAddress) {
        maliciousContract = MaliciousContract(_maliciousContractAddress);
    }

    function transferFunds(address _to, uint _amount) public {
        maliciousContract.stealFunds(_to, _amount);
    }
}
```

In this vulnerable smart contract `VulnerableContract`, the `transferFunds` function calls a function `stealFunds` from an external contract `MaliciousContract`. The `stealFunds` function in the external contract may contain malicious code to steal funds or perform unauthorized actions.

### Remediation:
To mitigate the "Hiding Malicious Code with External Contract" vulnerability, you can follow these remediation steps:

1. **Use Trusted Contracts**: Only interact with external contracts that are trusted and audited. Ensure that the external contract's code is transparent and does not contain any malicious logic.

2. **Implement Access Control**: Add access control mechanisms to restrict who can call critical functions in the external contract. This can prevent unauthorized parties from invoking harmful functions.

3. **Code Review and Auditing**: Thoroughly review the code of the external contract and conduct security audits to identify any potential vulnerabilities or malicious code.

4. **Use Events for Transparency**: Emit events in the external contract to track and monitor the actions performed by the contract. This can help in detecting any suspicious behavior.

By implementing these remediation steps, you can reduce the risk of falling victim to the "Hiding Malicious Code with External Contract" vulnerability in your smart contracts.