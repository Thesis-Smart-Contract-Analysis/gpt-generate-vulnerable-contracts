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

## Remediation

To address the Weak Sources of Randomness from Chain Attributes vulnerability, it is recommended to use a more secure source of randomness. One common approach is to use an external randomness oracle or a decentralized random number generator like Chainlink VRF (Verifiable Random Function).

Here is an example of how you can integrate Chainlink VRF into the smart contract to improve randomness:

```solidity
// Smart contract with improved randomness using Chainlink VRF

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract RandomnessWithChainlink is VRFConsumerBase {
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

In the remediated smart contract, we are using Chainlink VRF to generate a secure and verifiable random number. This ensures that the randomness is not predictable or manipulable by external entities.