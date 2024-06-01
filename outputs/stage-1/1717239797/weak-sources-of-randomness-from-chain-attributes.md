```solidity
// Smart contract with Weak Sources of Randomness from Chain Attributes vulnerability

pragma solidity ^0.8.0;

contract WeakRandomness {
    uint256 public randomNumber;

    constructor() {
        // Using block.timestamp as a source of randomness
        randomNumber = uint256(keccak256(abi.encodePacked(block.timestamp)));
    }

    function generateRandomNumber() public {
        // Using block.difficulty as a source of randomness
        randomNumber = uint256(keccak256(abi.encodePacked(block.difficulty)));
    }
}
```

In the smart contract above, the `randomNumber` is generated using `block.timestamp` and `block.difficulty` as sources of randomness. However, both `block.timestamp` and `block.difficulty` are not secure sources of randomness as they can be manipulated by miners or external attackers.

## Remediation:

To address the Weak Sources of Randomness from Chain Attributes vulnerability, you can use an external randomness oracle or a verifiable random function (VRF) to generate secure random numbers. Here is an example of how you can improve the smart contract:

```solidity
// Improved Smart contract with Secure Randomness using Chainlink VRF

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

    function requestRandomNumber() public {
        require(LINK.balanceOf(address(this)) >= fee, "Not enough LINK tokens");
        requestRandomness(keyHash, fee);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness) internal override {
        randomNumber = randomness;
    }
}
```

In the improved smart contract, we are using Chainlink VRF (Verifiable Random Function) to generate secure random numbers. Chainlink VRF provides a secure and tamper-proof source of randomness that cannot be manipulated by miners or external attackers. By using Chainlink VRF, you can ensure that the random numbers generated in your smart contract are secure and unpredictable.