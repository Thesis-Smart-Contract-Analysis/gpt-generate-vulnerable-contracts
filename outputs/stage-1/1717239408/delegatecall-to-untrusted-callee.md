Below is a vulnerable smart contract that has the Delegatecall to Untrusted Callee vulnerability:

```solidity
pragma solidity ^0.8.0;

contract Proxy {

  address owner;

  constructor() {
    owner = msg.sender;  
  }

  function getOwner() public view returns (address) {
    return owner;
  }

  function forward(address callee, bytes memory _data) public {
    (bool success, ) = callee.delegatecall(_data);
    require(success);
  }

}

contract Attacker {
    
  address owner;

  fallback() external { 
    owner = 0xB514b2e847116c7B57e0BFac3a180eB049cd395c;
  }

}
```

In this vulnerable setup, the `Proxy` contract has a `forward` function that uses `delegatecall` to call a function in an untrusted contract, in this case, the `Attacker` contract. The `Attacker` contract has a `fallback` function that changes the `owner` variable in the `Proxy` contract to an address controlled by the attacker.

### Remediation:

To remediate the Delegatecall to Untrusted Callee vulnerability, you should ensure that the `delegatecall` is only used to call functions in trusted contracts. Here is an example of how you can modify the `forward` function in the `Proxy` contract to include a whitelist of trusted contracts:

```solidity
pragma solidity ^0.8.0;

contract Proxy {

  address owner;
  mapping(address => bool) public trustedContracts;

  constructor() {
    owner = msg.sender;  
  }

  function getOwner() public view returns (address) {
    return owner;
  }

  function addTrustedContract(address _contract) public {
    trustedContracts[_contract] = true;
  }

  function forward(address callee, bytes memory _data) public {
    require(trustedContracts[callee], "Untrusted contract");
    (bool success, ) = callee.delegatecall(_data);
    require(success);
  }

}

contract Attacker {
    
  address owner;

  fallback() external { 
    owner = 0xB514b2e847116c7B57e0BFac3a180eB049cd395c;
  }

}
```

In the remediated version, the `Proxy` contract now includes a `trustedContracts` mapping where trusted contracts can be added. The `forward` function now checks if the callee contract is in the list of trusted contracts before performing the `delegatecall`. This ensures that only trusted contracts can be called using `delegatecall`.