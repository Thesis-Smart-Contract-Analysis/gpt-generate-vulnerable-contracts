# Smart contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableContract {

  function manipulateSignature(bytes memory signature) public pure returns(bytes memory) {
    (uint8 v, bytes32 r, bytes32 s) = splitSignature(signature);

    uint8 manipulatedV = v % 2 == 0 ? v - 1 : v + 1;
    uint256 manipulatedS = modNegS(uint256(s));
    bytes memory manipulatedSignature = abi.encodePacked(r, bytes32(manipulatedS), manipulatedV);

    return manipulatedSignature;
  }

  function splitSignature(bytes memory sig) public pure returns (uint8 v, bytes32 r, bytes32 s) {
    require(sig.length == 65, "Invalid signature length");
    assembly {
      r := mload(add(sig, 32))
      s := mload(add(sig, 64))
      v := byte(0, mload(add(sig, 96)))
    }
    if (v < 27) {
      v += 27;
    }
    require(v == 27 || v == 28, "Invalid signature v value");
  }

  function modNegS(uint256 s) public pure returns (uint256) {
    uint256 n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141;        
    return n - s;
  }

}
```

Description of the vulnerability: The vulnerability lies in the `manipulateSignature` function of the `VulnerableContract` contract. This function allows an attacker to manipulate a valid signature by changing the `v` value to be either `v - 1` or `v + 1` based on whether `v` is even or odd, and by calculating a new `s` value using the `modNegS` function. This manipulation can result in a new valid signature that can be used to impersonate the original signer.

# Remediations

- Implement signature verification logic that checks for malleability by ensuring that the `v` value is within a specific range and that the `s` value is positive.
- Use a secure library or contract, such as OpenZeppelin's `ECDSA` library, for signature verification to prevent signature malleability vulnerabilities.