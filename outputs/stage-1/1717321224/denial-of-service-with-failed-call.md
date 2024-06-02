# Smart contract

```solidity
pragma solidity ^0.4.24;

contract DenialOfService {

  function withdrawBalance() public {
    msg.sender.call.value(this.balance)();
  }

}
```

The vulnerability lies in the line `msg.sender.call.value(this.balance)();` where an external call is made to `msg.sender` without checking the return value, which can lead to a Denial of Service attack with Failed Call vulnerability.

# Remediations

- Use the `transfer` function instead of `call` to send Ether to `msg.sender` to prevent the possibility of a failed call.
- Implement a withdrawal pattern where users can withdraw their funds in a controlled manner to avoid potential reentrancy attacks.