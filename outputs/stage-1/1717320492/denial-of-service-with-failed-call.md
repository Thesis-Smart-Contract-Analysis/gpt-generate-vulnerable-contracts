# Smart contract

```solidity
pragma solidity ^0.4.24;

contract DenialOfService {

  function withdrawFunds() public {
    msg.sender.call.value(1 ether)(); // Vulnerable line
  }

}
```

The vulnerable line in the smart contract `DenialOfService` is where the `withdrawFunds` function uses `msg.sender.call.value(1 ether)();` to send 1 ether to the caller. This line is vulnerable to a Denial of Service with Failed Call attack because it allows anyone to call the function and potentially cause the contract to get stuck in a loop, consuming all available gas.

# Remediations

- Use the `transfer` function instead of `call` to send funds to the caller. This will prevent the contract from getting stuck in a loop and failing the call.
- Implement access control mechanisms to restrict who can call the `withdrawFunds` function, ensuring that only authorized users can withdraw funds.