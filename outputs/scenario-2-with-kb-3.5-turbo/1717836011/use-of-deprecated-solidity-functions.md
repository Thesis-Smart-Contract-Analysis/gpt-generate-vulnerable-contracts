# Smart contract with Use of Deprecated Solidity Functions Vulnerability

```solidity
contract DeprecatedSimple {

  function DeprecatedSimple() public { } // Line 3

  function useDeprecated() public constant { // Line 5
    bytes32 blockhash = block.blockhash(0); // Line 6
    bytes32 hashofhash = sha3(blockhash); // Line 7

    uint gas = msg.gas; // Line 9

    if (gas == 0) { // Line 11
      throw; // Line 12
    }

    address(this).callcode(); // Line 14

    var a = [1,2,3]; // Line 16

    var (x, y, z) = (false, "test", 0); // Line 18

    suicide(address(0)); // Line 20
  }

  function () public {} // Line 22
}
```

Description: The smart contract `DeprecatedSimple` contains the Use of Deprecated Solidity Functions vulnerability due to the usage of deprecated functions like `block.blockhash`, `sha3`, `msg.gas`, `callcode`, and `suicide`.

# Remediations

- Update `block.blockhash(0)` to `blockhash(0)` and `sha3` to `keccak256`.
- Replace `msg.gas` with `gasleft`.
- Change `address(this).callcode()` to `address(this).delegatecall()`.
- Use explicit data types instead of `var`.
- Replace `suicide(address(0))` with `selfdestruct(address(0))`.
- Consider using the `view` modifier instead of `constant`.
- Rename the constructor function to `constructor`.

By applying these remediations, the smart contract can mitigate the Use of Deprecated Solidity Functions vulnerability and ensure compatibility with newer compiler versions.