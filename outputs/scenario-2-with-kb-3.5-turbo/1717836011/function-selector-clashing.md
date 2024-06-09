# Smart contract

```solidity
pragma solidity ^0.5.0;

import "openzeppelin-eth/contracts/token/ERC20/ERC20Burnable.sol";
import "openzeppelin-eth/contracts/token/ERC20/ERC20Detailed.sol";
import "zos-lib/contracts/Initializable.sol";

contract BurnableToken is Initializable, ERC20Burnable, ERC20Detailed {

  function initialize(
    string memory name,
    string memory symbol,
    uint8 decimals,
    uint256 initialSupply
  ) 
    public 
    initializer
  {
    super.initialize(name, symbol, decimals);
    _mint(msg.sender, initialSupply);
  }

  // Vulnerability: Function Selector Clashing vulnerability present in the following function
  function collate_propagate_storage(bytes16) external {
    implementation.delegatecall(abi.encodeWithSignature(
        "transfer(address,uint256)", proxyOwner, 1000
    ));
  }
  
}
```

Description of the vulnerability: The `collate_propagate_storage` function in the `BurnableToken` contract contains the Function Selector Clashing vulnerability. The function's 4-byte function selector hash clashes with another function's selector hash, potentially leading to unintended function execution.

# Remediations

- Implement unique function signatures: Ensure that each function in a contract has a unique function signature to prevent clashes with other function selectors. This can be achieved by carefully designing function names and parameters to avoid collisions.
- Use function modifiers: Utilize function modifiers to add additional checks or conditions before executing critical functions, reducing the risk of unauthorized or unintended function calls.