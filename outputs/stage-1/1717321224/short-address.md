# Smart contract with Short Address Vulnerability

```solidity
pragma solidity ^0.4.24;

contract ShortAddressVulnerability {

  function withdrawFunds(address _recipient) public {
    require(_recipient == 0x123456789); // Short Address Vulnerability here
    _recipient.transfer(this.balance);
  }

}
```

In the above smart contract, the vulnerability lies in the line where the `_recipient` address is compared to a short address `0x123456789`. Short addresses can be padded with zeros, and this can lead to unexpected behavior when comparing addresses.

# Description

Short Address Vulnerability occurs when comparing an address with a short address that is not properly padded with zeros. This can lead to security risks as the comparison may not work as intended.

# Remediations

- Explicitly pad the address with zeros to ensure it has the correct length before comparison.
- Use libraries like OpenZeppelin's Address library to handle address-related operations securely.