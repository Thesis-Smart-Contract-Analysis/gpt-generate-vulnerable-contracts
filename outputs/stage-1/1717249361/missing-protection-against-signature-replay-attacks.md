Below is a vulnerable smart contract that lacks protection against Signature Replay Attacks:

```solidity
pragma solidity ^0.8.0;

contract SignatureReplayVulnerable {
    mapping(address => uint256) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount, bytes memory signature) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // Verify signature
        address signer = recoverSigner(amount, signature);
        require(signer == msg.sender, "Invalid signature");

        payable(msg.sender).transfer(amount);
        balances[msg.sender] -= amount;
    }

    function recoverSigner(uint256 amount, bytes memory signature) internal pure returns (address) {
        bytes32 message = keccak256(abi.encodePacked(amount));
        bytes32 ethSignedMessageHash = keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", message));
        address signer = ECDSA.recover(ethSignedMessageHash, signature);
        return signer;
    }
}
```

In the `withdraw` function of the smart contract above, a signature is used to verify the sender of the transaction. However, the contract is vulnerable to Signature Replay Attacks because it does not include any protection mechanism to prevent the same signature from being used multiple times to withdraw funds.

## Remediation:

To protect against Signature Replay Attacks, you can implement a nonce-based system where each withdrawal request includes a unique nonce that must be used only once. Here is an updated version of the smart contract with nonce-based protection:

```solidity
pragma solidity ^0.8.0;

contract SignatureReplayFixed {
    mapping(address => uint256) public balances;
    mapping(address => uint256) public nonces;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount, bytes memory signature, uint256 nonce) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // Verify signature and nonce
        require(nonces[msg.sender] < nonce, "Nonce must be increasing");
        address signer = recoverSigner(amount, nonce, signature);
        require(signer == msg.sender, "Invalid signature");

        payable(msg.sender).transfer(amount);
        balances[msg.sender] -= amount;
        nonces[msg.sender] = nonce;
    }

    function recoverSigner(uint256 amount, uint256 nonce, bytes memory signature) internal pure returns (address) {
        bytes32 message = keccak256(abi.encodePacked(amount, nonce));
        bytes32 ethSignedMessageHash = keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", message));
        address signer = ECDSA.recover(ethSignedMessageHash, signature);
        return signer;
    }
}
```

In the remediated version of the smart contract, a `nonce` parameter is added to the `withdraw` function. The `nonce` should be a unique value for each withdrawal request and must be increasing for each subsequent request. This ensures that the same signature cannot be replayed for multiple withdrawals. The `nonce` is stored in the `nonces` mapping for each user and checked before processing a withdrawal request.