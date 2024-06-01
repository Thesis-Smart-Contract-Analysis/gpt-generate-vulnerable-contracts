```solidity
// Smart Contract with Missing Protection against Signature Replay Attacks Vulnerability

pragma solidity ^0.8.0;

contract SignatureReplayVulnerability {
    
    mapping(address => uint256) public balances;
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    function withdraw(uint256 amount, bytes memory signature) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // Simulating signature verification (not secure)
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

In the above smart contract, the `withdraw` function allows a user to withdraw a specified amount by providing a signature. However, there is no protection against signature replay attacks, where an attacker can reuse a valid signature to withdraw funds multiple times.

## Remediation:

To protect against signature replay attacks, you can implement a nonce-based system where each withdrawal request includes a unique nonce that prevents replay attacks. Here is an updated version of the smart contract with nonce-based protection:

```solidity
// Smart Contract with Protection against Signature Replay Attacks

pragma solidity ^0.8.0;

contract SignatureReplayProtection {
    
    mapping(address => uint256) public balances;
    mapping(address => uint256) public nonces;
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    function withdraw(uint256 amount, bytes memory signature, uint256 nonce) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // Verify nonce to prevent replay attacks
        require(nonce > nonces[msg.sender], "Invalid nonce");
        
        // Simulating signature verification (not secure)
        address signer = recoverSigner(amount, signature);
        require(signer == msg.sender, "Invalid signature");
        
        nonces[msg.sender] = nonce; // Update nonce
        
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

In the remediated version, a `nonce` parameter is added to the `withdraw` function, and the nonce is checked to ensure it is greater than the previous nonce for the user. This prevents replay attacks by requiring a unique nonce for each withdrawal request.