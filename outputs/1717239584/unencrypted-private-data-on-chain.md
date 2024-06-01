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

In the smart contract `UnencryptedData` above, the `secretData` variable is marked as private but it is stored on the blockchain in plain text. This means that anyone who has access to the blockchain can view the contents of `secretData` by simply reading the blockchain data.

## Remediation

To address the Unencrypted Private Data On-Chain vulnerability, sensitive data should never be stored in plain text on the blockchain. Instead, sensitive data should be encrypted before being stored on the blockchain. Here is an updated version of the smart contract with encryption implemented:

```solidity
pragma solidity ^0.8.0;

contract EncryptedData {

    address private owner;
    bytes private encryptedData;
    bytes private encryptionKey;

    constructor(bytes memory _encryptionKey) {
        owner = msg.sender;
        encryptionKey = _encryptionKey;
    }

    function setEncryptedData(bytes memory _data) public {
        require(msg.sender == owner, "Only the owner can set the encrypted data");
        encryptedData = _data;
    }

    function getEncryptedData() public view returns (bytes memory) {
        return encryptedData;
    }

    function decryptData(bytes memory _data) public view returns (string memory) {
        // Decrypt the data using the encryption key
        // Add decryption logic here
    }
}
```

In the updated `EncryptedData` smart contract, the `encryptedData` variable stores the sensitive data in an encrypted format. The `encryptionKey` is used to encrypt and decrypt the data. The `decryptData` function can be used to decrypt the data using the encryption key.

By encrypting sensitive data before storing it on the blockchain, the confidentiality and security of the data are maintained, and unauthorized parties cannot access the sensitive information.