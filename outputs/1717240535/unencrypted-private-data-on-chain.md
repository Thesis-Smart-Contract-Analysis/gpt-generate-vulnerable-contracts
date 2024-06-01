Below is a vulnerable smart contract that has the Unencrypted Private Data On-Chain vulnerability:

```solidity
pragma solidity ^0.8.0;

contract UnencryptedData {

    address private owner;
    string private secretData;

    constructor() {
        owner = msg.sender;
    }

    function setSecretData(string memory _data) public {
        require(msg.sender == owner, "Only the owner can set the secret data");
        secretData = _data;
    }

    function getSecretData() public view returns (string memory) {
        return secretData;
    }
}
```

In the smart contract `UnencryptedData` above, the `secretData` variable is marked as private but it is stored in plain text on the blockchain. This means that anyone who has access to the blockchain can read the contents of `secretData` by simply looking at the blockchain data.

### Remediation:
To address the Unencrypted Private Data On-Chain vulnerability, you should encrypt sensitive data before storing it on the blockchain. Here is an updated version of the smart contract with encrypted data:

```solidity
pragma solidity ^0.8.0;

contract EncryptedData {

    address private owner;
    bytes private encryptedData;
    address private encryptionKey;

    constructor(address _encryptionKey) {
        owner = msg.sender;
        encryptionKey = _encryptionKey;
    }

    function setEncryptedData(bytes memory _data) public {
        require(msg.sender == owner, "Only the owner can set the encrypted data");
        encryptedData = _data;
    }

    function getEncryptedData() public view returns (bytes memory) {
        require(msg.sender == owner || msg.sender == encryptionKey, "Only the owner or encryption key holder can access the encrypted data");
        return encryptedData;
    }
}
```

In the updated `EncryptedData` smart contract, the `encryptedData` is stored as bytes and should be encrypted using a secure encryption algorithm before being set. The `encryptionKey` is used to decrypt the data when needed. Only the owner and the encryption key holder can access the encrypted data.

By encrypting sensitive data before storing it on the blockchain, you can ensure that the data remains secure and private, even if it is visible on the blockchain.