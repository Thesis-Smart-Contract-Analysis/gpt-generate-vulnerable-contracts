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

In this vulnerable smart contract, the `VulnerableContract` interacts with an external contract `MaliciousContract` through an interface. The `transferFunds` function in `VulnerableContract` calls the `stealFunds` function of `MaliciousContract`, which can potentially execute malicious code to steal funds or perform unauthorized actions.

### Remediation:
To mitigate the "Hiding Malicious Code with External Contract" vulnerability, you can follow these remediation steps:

1. **Audit External Contracts**: Before interacting with any external contract, thoroughly audit the code and functionality of the external contract to ensure it is secure and does not contain any malicious code.

2. **Use Trusted Contracts**: Only interact with external contracts that are trusted and have been verified to be secure. Maintain a whitelist of approved contracts that your contract can interact with.

3. **Limited Permissions**: If possible, limit the permissions and actions that the external contract can perform when interacting with your contract. Implement access control mechanisms to restrict the capabilities of the external contract.

4. **Event Logging**: Implement event logging in your contract to track and monitor the interactions with external contracts. This can help in detecting any suspicious behavior or unauthorized actions.

By following these remediation steps, you can enhance the security of your smart contract and reduce the risk of falling victim to malicious code hidden in external contracts.