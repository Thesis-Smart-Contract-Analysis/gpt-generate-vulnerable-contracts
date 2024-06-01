Below is a vulnerable smart contract with Timestamp Dependency vulnerability:

```solidity
// Vulnerable Smart Contract with Timestamp Dependency

pragma solidity ^0.8.0;

contract TimeLock {
    address public owner;
    uint public unlockTime;

    constructor() {
        owner = msg.sender;
        unlockTime = block.timestamp + 1 minutes; // Unlock after 1 minute for testing purposes
    }

    function unlock() public {
        require(msg.sender == owner, "Only the owner can unlock");
        require(block.timestamp >= unlockTime, "The unlock time has not arrived yet");

        // Perform unlock operation
        owner = address(0);
    }
}
```

In the above smart contract `TimeLock`, the `unlock` function is designed to unlock the contract after a certain timestamp has passed. However, relying solely on `block.timestamp` for time-based operations can be vulnerable to manipulation by miners.

An attacker with control over the mining process can potentially manipulate the timestamp to bypass the time lock and unlock the contract prematurely.

### Remediation for Timestamp Dependency Vulnerability:

To mitigate the Timestamp Dependency vulnerability, it is recommended to use block numbers instead of timestamps for time-dependent operations. Block numbers are more secure and less susceptible to manipulation.

Here is the remediated version of the smart contract `TimeLock` using block numbers:

```solidity
// Remediated Smart Contract with Block Number Dependency

pragma solidity ^0.8.0;

contract TimeLock {
    address public owner;
    uint public unlockBlock;

    constructor() {
        owner = msg.sender;
        unlockBlock = block.number + 10; // Unlock after 10 blocks for testing purposes
    }

    function unlock() public {
        require(msg.sender == owner, "Only the owner can unlock");
        require(block.number >= unlockBlock, "The unlock block has not arrived yet");

        // Perform unlock operation
        owner = address(0);
    }
}
```

In the remediated version, the `unlock` function now uses `block.number` to determine the unlock condition instead of `block.timestamp`. This change makes the contract less vulnerable to timestamp manipulation attacks.

By using block numbers, the smart contract becomes more secure and resistant to timestamp manipulation vulnerabilities.