# Smart contract

```solidity
pragma solidity ^0.4.11;

contract MyToken {
  
  mapping (address => uint) balances;
  
  event Transfer(address indexed _from, address indexed _to, uint256 _value);
  
  function MyToken() {
    balances[tx.origin] = 10000;
  }
  
  function sendCoin(address to, uint amount) returns(bool sufficient) {
    if (balances[msg.sender] < amount) return false;
    balances[msg.sender] -= amount;
    balances[to] += amount;
    Transfer(msg.sender, to, amount);
    return true;
  }
  
  function getBalance(address addr) constant returns(uint) {
    return balances[addr];
  }
  
}
```

Description of the vulnerability: The vulnerability in the smart contract lies in the `sendCoin` function where it does not check the length of the transaction data when processing the address parameter. This can lead to a Short Address vulnerability where an attacker can manipulate the transaction data to send a different amount of tokens than intended.

# Remediations

- Implement a modifier to check the size of the transaction data before processing it in functions that involve address parameters.
- Use the `onlyPayloadSize` modifier to ensure that the transaction data has the expected size before executing the function.

By implementing the suggested remediation, you can prevent Short Address vulnerabilities and enhance the security of the smart contract.