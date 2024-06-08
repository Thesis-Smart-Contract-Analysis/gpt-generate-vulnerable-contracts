# Smart contract

```solidity
pragma solidity ^0.5.0;

contract TimedCrowdsale {

  event Finished();
  event notFinished();

  // Vulnerability: Timestamp Dependency vulnerability on the following line
  function isSaleFinished() private returns (bool) {
    return block.timestamp >= 1546300800;
  }

  function run() public {
    if (isSaleFinished()) {
      emit Finished();
    } else {
      emit notFinished();
    }
  }

}
```

Description of the vulnerability in the above smart contract:
The smart contract `TimedCrowdsale` contains a Timestamp Dependency vulnerability on the line where it checks if the sale is finished based on `block.timestamp`. This vulnerability allows an attacker to manipulate the block timestamp to prematurely trigger the `Finished` event.

# Remediations

- Use a more secure and reliable source of time information, such as an external Oracle, to avoid relying solely on `block.timestamp`.
- Implement a time-based mechanism that is less susceptible to manipulation, such as using block numbers or a combination of multiple sources of time information for validation.
- Consider adding additional checks or validations to ensure the integrity of time-sensitive operations within the smart contract.