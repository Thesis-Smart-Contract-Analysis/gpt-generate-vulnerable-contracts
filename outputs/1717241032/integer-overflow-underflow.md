```solidity
// Smart Contract with Integer Overflow/Underflow Vulnerability

pragma solidity ^0.8.0;

contract IntegerOverflowUnderflow {
    uint256 public balance = 100;

    function add(uint256 _value) public {
        balance += _value;
    }

    function subtract(uint256 _value) public {
        balance -= _value;
    }
}
```

### Remediation:

To mitigate the Integer Overflow/Underflow vulnerability, you can use SafeMath library from OpenZeppelin to perform arithmetic operations on integers. Here's how you can update the smart contract using SafeMath:

```solidity
// Smart Contract with SafeMath to prevent Integer Overflow/Underflow

pragma solidity ^0.8.0;
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract IntegerOverflowUnderflowFixed {
    using SafeMath for uint256;

    uint256 public balance = 100;

    function add(uint256 _value) public {
        balance = balance.add(_value);
    }

    function subtract(uint256 _value) public {
        balance = balance.sub(_value);
    }
}
```

By using SafeMath library, you ensure that arithmetic operations are performed safely without the risk of Integer Overflow/Underflow vulnerabilities.