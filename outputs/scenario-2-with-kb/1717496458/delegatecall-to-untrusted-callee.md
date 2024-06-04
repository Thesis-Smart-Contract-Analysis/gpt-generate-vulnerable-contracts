# Smart Contract with Delegatecall to Untrusted Callee Vulnerability

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UntrustedCallee {
    uint public value;

    function setValue(uint _value) public {
        value = _value;
    }
}

contract VulnerableDelegatecall {
    uint public value;
    address public owner;
    address public callee;

    constructor(address _callee) {
        owner = msg.sender;
        callee = _callee;
    }

    function setTrustedCallee(address _callee) public {
        require(msg.sender == owner, "Not owner");
        callee = _callee;
    }

    function unsafeDelegatecall(uint _value) public {
        (bool success, ) = callee.delegatecall(
            abi.encodeWithSignature("setValue(uint256)", _value)
        );
        require(success, "Delegatecall failed");
    }
}
```

### Description of the Vulnerability
In the `VulnerableDelegatecall` contract, the `unsafeDelegatecall` function uses `delegatecall` to invoke the `setValue` function on an address specified by `callee`. The `callee` address is set during contract construction and can be changed by the owner. However, if the `callee` address is set to an untrusted contract, that contract could execute malicious code in the context of the `VulnerableDelegatecall` contract, potentially leading to unexpected alterations of state variables or other security issues. This is because `delegatecall` executes the code of the target address in the context of the caller's storage.

# Remediations

1. **Validate Callee Contracts**: Ensure that the address specified as `callee` is a trusted and verified contract. This can be implemented by maintaining a list of approved contracts and checking against this list before performing the delegatecall.

2. **Use an Interface**: Instead of directly using `delegatecall`, define and use a known, trusted interface for interaction with external contracts. This approach limits the functions that can be called and reduces the surface for attacks.

3. **Restrict Function Access**: Limit the use of sensitive functions like `setTrustedCallee` to only the owner or through multi-signature verification to prevent unauthorized changes to the delegate callee.

4. **Event Logging**: Add event logging for critical actions such as changes to the `callee` address. This provides transparency and an audit trail that can be monitored for suspicious activities.

5. **Static Analysis and Testing**: Regularly use tools for static analysis to detect common vulnerabilities and ensure thorough testing, including tests for delegatecall invocations, to identify potential security issues before deployment.

By implementing these remediations, the security of the contract can be significantly enhanced, mitigating risks associated with the delegatecall to untrusted callees.