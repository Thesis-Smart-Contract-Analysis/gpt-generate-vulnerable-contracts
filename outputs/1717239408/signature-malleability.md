Below is a smart contract that demonstrates the Signature Malleability vulnerability:

```solidity
pragma solidity ^0.8.0;

contract SignatureMalleability {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function changeOwner(address _newOwner, uint8 _v, bytes32 _r, bytes32 _s) public {
        bytes32 hash = keccak256(abi.encodePacked(_newOwner));
        address signer = ecrecover(hash, _v, _r, _s);
        require(signer == owner, "Invalid signature");
        owner = _newOwner;
    }
}
```

In the `changeOwner` function, the new owner address is passed along with the `v`, `r`, and `s` parameters for signature verification. However, the signature malleability vulnerability arises when an attacker can manipulate the signature parameters in such a way that the signature still appears valid but the outcome is different.

To exploit this vulnerability, an attacker can modify the `r` and `s` values while keeping the `v` value the same, resulting in a different address being set as the owner without the signature verification failing.

### Remediation:

To mitigate the Signature Malleability vulnerability, you can follow these best practices:

1. **Use a Standardized Message Format**: Use a standardized message format for signing messages to prevent attackers from manipulating the message content.

2. **Normalize Signatures**: Normalize the `r` and `s` values to prevent malleability. This can be achieved by enforcing specific ranges or formats for these values.

3. **Use a Secure Signature Scheme**: Consider using more secure signature schemes like ECDSA (Elliptic Curve Digital Signature Algorithm) with proper key management practices.

4. **Implement Strict Signature Verification**: Implement strict signature verification logic to ensure that the signature parameters are validated correctly.

By following these remediation steps, you can reduce the risk of the Signature Malleability vulnerability in your smart contracts.