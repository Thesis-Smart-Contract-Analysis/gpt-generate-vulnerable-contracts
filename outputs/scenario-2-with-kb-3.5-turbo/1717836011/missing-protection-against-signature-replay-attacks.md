# Smart contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "./ECDSA.sol";

contract MultiSigWallet {
  
  using ECDSA for bytes32;

  address[2] public owners;

  constructor(address[2] memory _owners) payable { owners = _owners; }

  function deposit() external payable { }

  function transfer(address _to, uint256 _amount, bytes[2] memory _sigs)
    external
  {
    bytes32 txHash = getTxHash(_to, _amount);
    require(_checkSigs(_sigs, txHash), "invalid sig");

    (bool sent,) = _to.call{value: _amount}("");
    require(sent, "Failed to send Ether");
  }

  function getTxHash(address _to, uint256 _amount)
    public
    view
    returns (bytes32)
  {
    return keccak256(abi.encodePacked(_to, _amount));
  }

  function _checkSigs(bytes[2] memory _sigs, bytes32 _txHash)
    private
    view
    returns (bool)
  {
    bytes32 ethSignedHash = _txHash.toEthSignedMessageHash();

    for (uint256 i = 0; i < _sigs.length; i++) {
      address signer = ethSignedHash.recover(_sigs[i]);
      bool valid = signer == owners[i];

      if (!valid) {
        return false;
      }
    }

    return true;
  }
  
}
```

Description of the vulnerability in the above smart contract: The vulnerability lies in the `MultiSigWallet` contract's `transfer` function, where it does not protect against Signature Replay Attacks. This means that an attacker can reuse previously used signatures to execute unauthorized transfers.

# Remediations

- Implement a nonce mechanism: Introduce a nonce value that is included in the data to be signed. This nonce should be unique for each transaction and prevent signature replay attacks. Update the `transfer` function to include a nonce parameter and modify the `getTxHash` function to incorporate the nonce value in the hash calculation.
- Maintain a record of executed transactions: Keep track of executed transactions using a mapping to prevent the reuse of signatures. Add a mapping in the contract to store the status of each transaction and check this mapping before executing a transfer.