# Smart contract with Incorrect Inheritance Order Vulnerability

```solidity
pragma solidity ^0.8.0;

contract A {
    function f() public pure returns (string memory) {
        return "A";
    }
}

contract B is A {
    function f() public pure returns (string memory) {
        return "B";
    }
}

contract C is A {
    function f() public pure returns (string memory) {
        return "C";
    }
}

contract D is B, C {
    function f() public pure returns (string memory) {
        return "D";
    }
}
```

Description of the vulnerability: In the above smart contract, the contract `D` inherits from both contracts `B` and `C`, which in turn inherit from contract `A`. Both contracts `B` and `C` override the function `f` from contract `A`. When contract `D` calls the function `f`, it is ambiguous whether the function from contract `B` or `C` will be executed.

# Remediations

- **Remediation 1:** To fix the Incorrect Inheritance Order vulnerability, ensure that the order of inheritance is from the most specific to the most general contract. In this case, contract `D` should inherit from contract `C` first and then from contract `B`.

```solidity
contract D is C, B {
    function f() public pure returns (string memory) {
        return "D";
    }
}
```

By changing the order of inheritance, the function `f` from contract `C` will be executed in contract `D`, resolving the ambiguity.