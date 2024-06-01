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

In this vulnerable contract, the `VulnerableContract` interacts with an external contract `MaliciousContract` through an interface. The `transferFunds` function in `VulnerableContract` calls the `stealFunds` function of the `MaliciousContract`, which can potentially execute malicious code to steal funds or perform unauthorized actions.

### Remediation:
To mitigate the "Hiding Malicious Code with External Contract" vulnerability, you can follow these remediation steps:

1. **Use Trusted Contracts**: Only interact with contracts that are trusted and audited. Avoid interacting with external contracts that are not verified or could potentially contain malicious code.

2. **Implement Access Control**: Implement access control mechanisms to restrict which addresses or contracts can call sensitive functions in your contract. This can prevent unauthorized contracts from calling critical functions.

3. **Code Review and Auditing**: Conduct thorough code reviews and security audits to identify and address any vulnerabilities in the smart contract code, especially when interacting with external contracts.

4. **Use Events for Transparency**: Emit events for critical actions in the contract to provide transparency and allow external monitoring of contract activities. This can help detect any unexpected behavior caused by external contract interactions.

By following these remediation steps, you can enhance the security of your smart contract and reduce the risk of falling victim to malicious code hidden in external contracts.