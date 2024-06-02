# Smart contract

```solidity
pragma solidity ^0.4.24;

contract BuiltInSymbolShadowing {

  uint public msg;
  
  function setMessage(uint _msg) {
    msg = _msg;
  }

}
```

The vulnerability lies in the line `uint public msg;` where the variable `msg` is declared as a state variable with the same name as the global `msg` object in Solidity. This can lead to unexpected behavior as the state variable `msg` shadows the global `msg` object.

# Remediations

- Use unique variable names to avoid shadowing built-in symbols.
- Avoid using variable names that conflict with global objects or keywords in Solidity.