# Smart Contract with Integer Overflow/Underflow Vulnerability

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IntegerOverflowUnderflow {
    uint public balance = 1;

    // This function causes an underflow
    function decrement(uint value) public {
        balance -= value; // Vulnerable line: potential underflow if value > balance
    }

    // This function causes an overflow
    function increment(uint value) public {
        balance += value; // Vulnerable line: potential overflow if balance + value exceeds uint max
    }
}
```

### Description of the Vulnerability in the Above Smart Contract
The smart contract `IntegerOverflowUnderflow` contains two functions that manipulate the state variable `balance`. The `decrement` function can lead to an underflow if the `value` passed to it is greater than `balance`. Similarly, the `increment` function can cause an overflow if `value` added to `balance` exceeds the maximum value that a `uint` can hold in Solidity.

# Remediations

1. **Use SafeMath Library:**
   - The SafeMath library provides functions that automatically check for overflows and underflows. By using this library, you can ensure that all arithmetic operations are performed safely. Here's how you can apply it:
     ```solidity
     // SPDX-License-Identifier: MIT
     pragma solidity ^0.8.0;

     import "@openzeppelin/contracts/utils/math/SafeMath.sol";

     contract IntegerOverflowUnderflow {
         using SafeMath for uint;

         uint public balance = 1;

         function decrement(uint value) public {
             balance = balance.sub(value); // SafeMath prevents underflow
         }

         function increment(uint value) public {
             balance = balance.add(value); // SafeMath prevents overflow
         }
     }
     ```

2. **Check Conditions Manually:**
   - Before performing operations, manually check conditions to prevent overflows and underflows:
     ```solidity
     // SPDX-License-Identifier: MIT
     pragma solidity ^0.8.0;

     contract IntegerOverflowUnderflow {
         uint public balance = 1;

         function decrement(uint value) public {
             require(balance >= value, "Insufficient balance to decrement");
             balance -= value;
         }

         function increment(uint value) public {
             require(balance + value >= balance, "Overflow detected");
             balance += value;
         }
     }
     ```

3. **Solidity 0.8.x Automatic Checks:**
   - If using Solidity version 0.8.x or later, the compiler automatically includes checks for overflows and underflows. Ensure that your contracts are compiled with a compatible version to leverage these built-in safety features.

Each of these remediations helps to mitigate the risks associated with integer overflow and underflow, enhancing the security and reliability of your smart contract.