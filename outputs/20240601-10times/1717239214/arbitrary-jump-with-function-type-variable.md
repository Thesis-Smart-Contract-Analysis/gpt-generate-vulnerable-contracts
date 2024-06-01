Here is a vulnerable smart contract that has the Arbitrary Jump with Function Type Variable vulnerability:

```solidity
pragma solidity ^0.8.0;

contract ArbitraryJump {
    address public owner;
    bool public isOwner;

    constructor() {
        owner = msg.sender;
        isOwner = true;
    }

    function arbitraryJump(address _target, bytes memory _data) public {
        require(msg.sender == owner, "Only owner can call this function");
        
        (bool success, ) = _target.delegatecall(_data);
        require(success, "Delegatecall failed");
    }
}
```

In the `arbitraryJump` function, the owner of the contract can call any function in any contract by providing the target address and data. This can lead to arbitrary code execution and potential security vulnerabilities.

### Remediation:
To mitigate the Arbitrary Jump with Function Type Variable vulnerability, you should avoid using `delegatecall` with untrusted input data. Here are some suggestions for remediation:

1. **Whitelist Trusted Contracts**: Maintain a whitelist of trusted contracts that can be called using `delegatecall`. Only allow calls to functions in these trusted contracts.

2. **Limit Functionality**: Restrict the functionality of the `arbitraryJump` function to only allow specific and safe operations. Avoid allowing arbitrary function calls.

3. **Input Validation**: Validate the input parameters, especially the target address, to ensure that only authorized and safe contracts can be called.

4. **Use Safe Delegation**: Consider using safer alternatives like `call` or `staticcall` instead of `delegatecall` if possible. These alternatives have less risk of arbitrary code execution.

By implementing these remediation steps, you can reduce the risk of arbitrary code execution and enhance the security of your smart contract.