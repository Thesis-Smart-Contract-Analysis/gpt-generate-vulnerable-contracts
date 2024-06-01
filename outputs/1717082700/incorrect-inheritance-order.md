```solidity
// Incorrect Inheritance Order Vulnerability Example

pragma solidity ^0.8.0;

contract A {
    uint public a;

    constructor(uint _a) {
        a = _a;
    }
}

contract B is A {
    uint public b;

    constructor(uint _a, uint _b) A(_a) {
        b = _b;
    }
}

contract C is B {
    uint public c;

    constructor(uint _a, uint _b, uint _c) B(_a, _b) {
        c = _c;
    }
}
```

In the above example, the contract `C` inherits from contract `B`, which in turn inherits from contract `A`. However, the constructors are called in the wrong order in the inheritance chain. The correct order should be `A` -> `B` -> `C`, but the constructors are called in the order `B` -> `A` -> `C`.

### Remediation:

To fix the Incorrect Inheritance Order vulnerability, you should ensure that the constructors are called in the correct order in the inheritance chain. In this case, the constructors should be called in the order `A` -> `B` -> `C`.

Here is the remediated version of the smart contract:

```solidity
// Corrected Inheritance Order

pragma solidity ^0.8.0;

contract A {
    uint public a;

    constructor(uint _a) {
        a = _a;
    }
}

contract B is A {
    uint public b;

    constructor(uint _a, uint _b) A(_a) {
        b = _b;
    }
}

contract C is B {
    uint public c;

    constructor(uint _a, uint _b, uint _c) B(_a, _b) {
        c = _c;
    }
}
```

By ensuring that the constructors are called in the correct order, you can mitigate the Incorrect Inheritance Order vulnerability in your smart contract.