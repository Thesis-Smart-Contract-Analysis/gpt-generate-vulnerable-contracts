# Smart contract

```solidity
pragma solidity 0.8.0;

contract FrozenEther {
    mapping(address => uint) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }
}
```

Description of the vulnerability in the above smart contract: The vulnerability in this smart contract lies in the fact that it allows users to deposit Ether into the contract but does not provide any functionality for users to withdraw their deposited Ether. This can lead to a situation where Ether gets locked within the contract and cannot be withdrawn by the depositors.

# Remediations

- Add a withdrawal function: Implement a function that allows users to withdraw their deposited Ether from the contract. This function should update the user's balance and transfer the Ether back to the user.
- Implement a time-lock mechanism: Set a time-lock mechanism where deposited Ether can only be withdrawn after a certain period of time to prevent immediate withdrawals and provide a safety net for users in case of emergencies.