# Smart contract

```solidity
pragma solidity 0.4.24;

contract SimpleDAO {
  
  mapping (address => uint) public credit;

  function donate(address to) payable public{
    credit[to] += msg.value;
  }

  function withdraw(uint amount) public {
    if (credit[msg.sender]>= amount) { // Vulnerable line
      require(msg.sender.call.value(amount)());
      credit[msg.sender]-=amount;
    }
  }  

  function queryCredit(address to) view public returns(uint){
    return credit[to];
  }
  
}
```

Description of the vulnerability: The vulnerability in the `SimpleDAO` contract lies in the `withdraw` function where the `msg.sender.call.value(amount)()` is used before updating the `credit[msg.sender]` state variable. This allows an attacker to re-enter the `withdraw` function before the state is updated, leading to potential re-entrancy attacks.

# Remediations

- **Remediation 1: Check-Effect-Interaction Pattern**
  Implement the Check-Effect-Interaction pattern to prevent re-entrancy attacks. Update the `withdraw` function as follows:
  
  ```solidity
  function withdraw(uint amount) public {
    if (credit[msg.sender] >= amount) {
      uint256 currentCredit = credit[msg.sender]; // Store current credit
      credit[msg.sender] -= amount; // 1. Check
      require(msg.sender.call.value(amount)()); // 2. Effect
      assert(credit[msg.sender] == currentCredit - amount); // Ensure state is updated
    }
  }
  ```

- **Remediation 2: Use ReentrancyGuard**
  Utilize the `ReentrancyGuard` contract from OpenZeppelin to prevent re-entrancy attacks. You can apply the `nonReentrant` modifier to functions susceptible to re-entrancy. This modifier ensures that the function cannot be called recursively.

By implementing these remediations, you can mitigate the re-entrancy vulnerability in the `SimpleDAO` contract.