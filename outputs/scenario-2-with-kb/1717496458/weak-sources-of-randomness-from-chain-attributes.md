# Smart Contract

```solidity
pragma solidity ^0.8.0;

contract RandomNumberGame {
    uint256 private lastBlockNumber;
    bytes32 private lastBlockHash;

    function play() public {
        require(lastBlockNumber != block.number, "Wait for new block");
        require(blockhash(block.number - 1) == lastBlockHash, "Blockhash not matched");

        uint256 userRandomNumber = uint256(
            keccak256(
                abi.encodePacked(
                    lastBlockHash,
                    block.timestamp, // Vulnerable line
                    block.difficulty,
                    msg.sender
                )
            )
        ) % 100;

        lastBlockNumber = block.number;
        lastBlockHash = blockhash(block.number - 1);

        if (userRandomNumber == 50) {
            // Winner logic
        }
    }
}
```

Description of the vulnerability in the above smart contract:
The smart contract uses `block.timestamp` as part of the seed for generating a random number. This is vulnerable because miners can manipulate the timestamp of the blocks they mine within a certain range. This manipulation can influence the outcome of the random number generation, potentially allowing a miner to predict or alter the result to their advantage.

# Remediations

1. **Avoid Using `block.timestamp` for Randomness**: Replace `block.timestamp` with other less manipulable sources if randomness is critical. For instance, consider using a commit-reveal scheme combined with user-provided entropy to generate randomness.

2. **External Oracle for Randomness**: Use an external oracle service like Chainlink VRF (Verifiable Random Function) to obtain provably-fair and tamper-resistant random numbers. This service provides randomness that is verifiable on-chain and is resistant to manipulation by miners or users.

3. **Increase Complexity of Randomness Sources**: Combine multiple independent sources of entropy. For example, you could mix `block.difficulty`, an oracle-provided random number, and hashes of recent transactions to create a more secure random number generator.

4. **Time Delay and Multi-Block Analysis**: Implement a time delay between when the random number seed is submitted and when it is used, ensuring that the seed covers a span of multiple blocks. This reduces the risk of manipulation by making it harder for miners to predict future block hashes and timestamps.

By implementing these remediations, the smart contract can significantly reduce the risk associated with using blockchain attributes for generating random numbers, leading to a more secure and fair gaming experience.