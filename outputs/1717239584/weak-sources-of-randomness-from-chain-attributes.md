```solidity
// Smart contract with Weak Sources of Randomness from Chain Attributes vulnerability

pragma solidity ^0.8.0;

contract WeakRandomness {
    uint256 public randomNumber;

    constructor() {
        // Using block.timestamp as a source of randomness
        randomNumber = uint256(block.timestamp) % 100;
    }

    function getRandomNumber() public view returns (uint256) {
        return randomNumber;
    }
}
```

In the above smart contract, the `randomNumber` is generated using `block.timestamp` as a source of randomness. However, using `block.timestamp` for generating random numbers is not secure as it can be manipulated by miners to some extent.

## Remediation:

To mitigate the Weak Sources of Randomness from Chain Attributes vulnerability, you can use an external source of randomness such as an Oracle service or Chainlink VRF (Verifiable Random Function) to generate secure random numbers.

Here is an example of how you can integrate Chainlink VRF into the smart contract:

```solidity
// Smart contract with Secure Randomness using Chainlink VRF

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract SecureRandomness is VRFConsumerBase {
    bytes32 internal keyHash;
    uint256 internal fee;
    uint256 public randomNumber;

    constructor(address _vrfCoordinator, address _link, bytes32 _keyHash, uint256 _fee) 
        VRFConsumerBase(_vrfCoordinator, _link)
    {
        keyHash = _keyHash;
        fee = _fee;
    }

    function getRandomNumber() public {
        require(LINK.balanceOf(address(this)) >= fee, "Not enough LINK tokens");
        requestRandomness(keyHash, fee);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness) internal override {
        randomNumber = randomness % 100;
    }
}
```

In the remediated smart contract, we are using Chainlink VRF to securely generate random numbers. The `fulfillRandomness` function is called when the random number is generated by Chainlink VRF, and the `randomNumber` is calculated securely.