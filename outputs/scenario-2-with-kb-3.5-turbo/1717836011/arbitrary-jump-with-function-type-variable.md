# Smart contract

```solidity
/*
 * @source: https://gist.github.com/wadeAlexC/7a18de852693b3f890560ab6a211a2b8
 * @author: Alexander Wade
 */

pragma solidity ^0.4.25;

contract FunctionTypes {

  constructor() public payable { require(msg.value != 0); }

  function withdraw() private {
    require(msg.value == 0, 'dont send funds!'); // Vulnerable line
    address(msg.sender).transfer(address(this).balance);
  }

  function frwd() internal { 
    withdraw(); 
  }

  struct Func { 
    function () internal f; 
  }

  function breakIt() public payable {
    require(msg.value != 0, 'send funds!');
    Func memory func;
    func.f = frwd;
    assembly { 
      mstore(func, add(mload(func), callvalue))
    }
    func.f();
  }
}
```

Description of the vulnerability: The vulnerability lies in the `breakIt()` function where the attacker can manipulate the `func` variable using assembly code to jump to an arbitrary location in the bytecode, bypassing the `require()` statement in the `withdraw()` function.

# Remediations

- Avoid using assembly code whenever possible, as it introduces complexities and potential vulnerabilities.
- Restrict the ability for users to assign arbitrary values to function type variables to prevent such manipulation.