# Smart Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Auction {
    address public highestBidder;
    uint public highestBid;

    function bid() public payable {
        require(msg.value > highestBid, "Bid not high enough.");

        // Refund the previous highest bidder
        payable(highestBidder).transfer(highestBid); // Vulnerable line

        highestBidder = msg.sender;
        highestBid = msg.value;
    }
}
```

The vulnerability in the above smart contract lies in the handling of state updates and external calls. The contract updates the state after making an external call (`transfer`), which can lead to re-entrancy issues. This is a specific form of Transaction Ordering Dependency where the order of transactions can affect the state negatively if a malicious actor can call the `bid()` function recursively.

# Remediations

1. **Use Checks-Effects-Interactions Pattern**: Restructure the function to perform all checks first, then update the state, and finally interact with external contracts. This minimizes the risk of re-entrancy.

    ```solidity
    function bid() public payable {
        require(msg.value > highestBid, "Bid not high enough.");

        address previousHighestBidder = highestBidder;
        uint previousHighestBid = highestBid;

        highestBidder = msg.sender;
        highestBid = msg.value;

        if (previousHighestBidder != address(0)) {
            payable(previousHighestBidder).transfer(previousHighestBid);
        }
    }
    ```

2. **Use Reentrancy Guard**: Implement a reentrancy guard to prevent nested calls to sensitive functions.

    ```solidity
    bool private locked;

    modifier noReentrant() {
        require(!locked, "No reentrancy");
        locked = true;
        _;
        locked = false;
    }

    function bid() public payable noReentrant {
        require(msg.value > highestBid, "Bid not high enough.");

        payable(highestBidder).transfer(highestBid);

        highestBidder = msg.sender;
        highestBid = msg.value;
    }
    ```

These remediations help ensure that the contract's state is updated securely before interacting with external addresses, thus mitigating risks associated with transaction ordering dependencies and re-entrancy attacks.