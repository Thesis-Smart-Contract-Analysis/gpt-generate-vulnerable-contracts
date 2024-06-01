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

To remediate the Delegatecall to Untrusted Callee vulnerability, you should ensure that the `delegatecall` is only used with trusted contracts or contracts that are under your control. Here are some steps to mitigate this vulnerability:

1. **Whitelist Trusted Contracts**: Maintain a whitelist of trusted contracts that can be called using `delegatecall`. Only allow `delegatecall` to be used with contracts on this whitelist.

2. **Use Interface Contracts**: Instead of directly using `delegatecall` with arbitrary contracts, define and use interface contracts that specify the functions that can be called. This way, you can ensure that only specific functions are invoked.

3. **Careful Contract Interaction**: Always be cautious when interacting with external contracts and ensure that the contracts being called are secure and do not have malicious intent.

By implementing these remediation steps, you can prevent the Delegatecall to Untrusted Callee vulnerability and enhance the security of your smart contracts.