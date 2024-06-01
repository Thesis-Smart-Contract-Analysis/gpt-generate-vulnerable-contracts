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

In this vulnerable smart contract, the `VulnerableContract` interacts with an external contract `MaliciousContract` through an interface. The `transferFunds` function in `VulnerableContract` calls the `stealFunds` function of the `MaliciousContract`, which can potentially execute malicious code to steal funds or perform unauthorized actions.

### Remediation:
To mitigate the "Hiding Malicious Code with External Contract" vulnerability, you should follow these best practices:

1. **Use Trusted Contracts**: Only interact with contracts that are trusted and audited. Avoid interacting with external contracts that you do not have control over.

2. **Implement Access Control**: Implement access control mechanisms to restrict who can call sensitive functions in your contract. This can prevent unauthorized external contracts from calling critical functions.

3. **Use Function Modifiers**: Use function modifiers to add access control logic to functions that interact with external contracts. This can help ensure that only authorized callers can invoke these functions.

4. **Audit External Contracts**: If you need to interact with external contracts, ensure that they are secure and have been audited for vulnerabilities. Verify the source code and functionality of external contracts before integrating them into your system.

By following these remediation steps, you can reduce the risk of malicious code being hidden in external contracts and protect your smart contract from unauthorized actions.