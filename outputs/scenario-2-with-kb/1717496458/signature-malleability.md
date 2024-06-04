# Smart Contract with Signature Malleability Vulnerability

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SignatureMalleable {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function changeOwner(bytes memory signature) public {
        bytes32 message = keccak256(abi.encodePacked(msg.sender));
        require(recoverSigner(message, signature) == owner, "Invalid signature");
        owner = msg.sender;
    }

    function recoverSigner(bytes32 message, bytes memory sig) internal pure returns (address) {
        (uint8 v, bytes32 r, bytes32 s) = splitSignature(sig);
        return ecrecover(message, v, r, s);
    }

    function splitSignature(bytes memory sig) internal pure returns (uint8, bytes32, bytes32) {
        require(sig.length == 65, "Invalid signature length");

        bytes32 r;
        bytes32 s;
        uint8 v;

        assembly {
            r := mload(add(sig, 32))
            s := mload(add(sig, 64))
            v := byte(0, mload(add(sig, 96)))
        }

        return (v, r, s);
    }
}
```

### Description of the Vulnerability
The vulnerability in the `changeOwner` function arises from not enforcing a strict check on the `s` value of the ECDSA signature. In ECDSA, both `s` and `(n - s) % n` (where `n` is the curve order) are valid for the signature, which can lead to signature malleability. An attacker could potentially submit a valid signature with its `s` value altered to `n - s`, and it would still pass the `ecrecover` check, allowing unintended changes to the contract state or behavior.

# Remediations

- **Enforce Canonical Signature**: Modify the `recoverSigner` function to ensure that the `s` value of the signature is in the lower half of the curve order. This is known as enforcing a "low S" value, which can help mitigate signature malleability.

```solidity
function recoverSigner(bytes32 message, bytes memory sig) internal pure returns (address) {
    (uint8 v, bytes32 r, bytes32 s) = splitSignature(sig);
    uint256 curveOrder = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141;
    require(uint256(s) <= curveOrder / 2, "Signature s value is too high");
    return ecrecover(message, v, r, s);
}
```

- **Use a Library for Signature Handling**: Utilize a well-tested library such as OpenZeppelin's ECDSA library for handling signatures. This library includes functions that handle common pitfalls in signature verification and ensures that the signatures are canonical.

```solidity
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

function changeOwner(bytes memory signature) public {
    bytes32 message = ECDSA.toEthSignedMessageHash(abi.encodePacked(msg.sender));
    require(ECDSA.recover(message, signature) == owner, "Invalid signature");
    owner = msg.sender;
}
```

These remediations help ensure that the signature cannot be malleably altered without invalidating it, thus securing the contract against such attacks.