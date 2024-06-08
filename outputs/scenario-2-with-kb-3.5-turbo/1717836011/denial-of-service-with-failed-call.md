# Smart contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableContract {
    address public owner;
    address[] public investors;
    uint[] public investorTokens;

    function invest() public payable {
        investors.push(msg.sender);
        investorTokens.push(msg.value * 5); // 5 times the wei sent
    }

    function distribute() public {
        require(msg.sender == owner);

        for(uint i = 0; i < investors.length; i++) {
            investors[i].call{value: investorTokens[i]}(""); // Vulnerable line
        }
    }
}
```

Description of the vulnerability: The vulnerability lies in the `distribute` function where it iterates over the `investors` array and makes an external call to each investor's address with the corresponding token amount. If an investor's address is a contract with a fallback function that consumes a significant amount of gas or reverts, it can lead to a denial of service by exhausting gas and preventing further token transfers.

# Remediations

- Implement a withdrawal pattern where investors can pull their tokens instead of automatically pushing tokens to their addresses. This way, investors have control over when and how they receive their tokens, reducing the risk of a DoS attack.
- Use a withdrawal pattern that allows investors to claim their tokens individually, reducing the impact of a single investor causing a DoS attack on the entire contract.