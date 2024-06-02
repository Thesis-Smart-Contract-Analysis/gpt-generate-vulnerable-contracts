# Smart contract with Frozen Ether Vulnerability

```solidity
pragma solidity ^0.4.24;

contract FrozenEther {
    address public owner;

    function withdraw() public {
        require(msg.sender == owner);
        msg.sender.transfer(address(this).balance);
    }

    function setOwner(address _newOwner) public {
        owner = _newOwner;
    }
}
```

In the above smart contract, the vulnerability lies in the `withdraw` function. The `owner` can change by calling the `setOwner` function, but the `withdraw` function does not restrict the withdrawal to only the current `owner`. This allows anyone to call the `withdraw` function and withdraw all the Ether stored in the contract.

# Remediations

- Add a modifier to the `withdraw` function to ensure only the current `owner` can withdraw funds.
- Implement access control mechanisms to restrict unauthorized access to critical functions.
- Consider using a withdrawal pattern where users need to request a withdrawal and the owner approves it before transferring funds.