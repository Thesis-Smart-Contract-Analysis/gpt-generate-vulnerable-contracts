# Smart Contract

```solidity
pragma solidity ^0.4.24;

contract ImmutableBugs {
    uint public count = 1; // line 4

    function run(uint256 input) public {
        count -= input; // line 6
    }
}
```

The vulnerability in the above smart contract lies in line 6, where the `count` variable is decremented by the `input` parameter without any checks. This can lead to an integer underflow if `input` is greater than `count`. In Solidity versions prior to 0.8.0, integer underflow and overflow are not automatically checked, and they can corrupt the state of the smart contract.

# Remediations

1. **Use SafeMath Library:** For Solidity versions below 0.8.0, use OpenZeppelin's SafeMath library to safely perform arithmetic operations. This library provides methods that automatically check for overflows and underflows.
   ```solidity
   import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/SafeMath.sol";

   contract ImmutableBugs {
       using SafeMath for uint256;
       uint public count = 1;

       function run(uint256 input) public {
           count = count.sub(input); // SafeMath's sub function automatically reverts on underflow
       }
   }
   ```

2. **Upgrade Solidity Version:** If possible, upgrade the Solidity compiler version to 0.8.0 or higher. Starting from version 0.8.0, Solidity includes automatic checks for arithmetic operations, which revert the transaction in case of an overflow or underflow.
   ```solidity
   // SPDX-License-Identifier: MIT
   pragma solidity ^0.8.0;

   contract ImmutableBugs {
       uint public count = 1;

       function run(uint256 input) public {
           count -= input; // Automatically reverts on underflow
       }
   }
   ```

3. **Explicit Checks:** Add explicit checks before performing arithmetic operations to ensure that underflows or overflows do not occur.
   ```solidity
   pragma solidity ^0.4.24;

   contract ImmutableBugs {
       uint public count = 1;

       function run(uint256 input) public {
           require(input <= count, "Input exceeds count");
           count -= input;
       }
   }
   ```

Each of these remediations ensures that the state of the smart contract remains consistent and prevents potential vulnerabilities due to integer underflows.