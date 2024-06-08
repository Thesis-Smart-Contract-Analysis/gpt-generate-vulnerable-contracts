# Smart contract

```solidity
contract VulnerableContract {
    
    address public trustedCallee;
    uint256 public value;

    constructor(address _trustedCallee) {
        trustedCallee = _trustedCallee;
    }

    function executeDelegateCall(bytes memory _data) public {
        (bool success, ) = trustedCallee.delegatecall(_data); // Line with vulnerability
        require(success, "Delegatecall failed");
    }

}
```

Description of the vulnerability in the above smart contract:

The vulnerability in the `VulnerableContract` lies in the `executeDelegateCall` function where it uses `delegatecall` to execute code from the `trustedCallee` address. If an attacker can manipulate the `trustedCallee` address to point to a malicious contract, they can exploit this vulnerability to modify the state of `VulnerableContract`.

# Remediations

- **Remediation 1:** Implement a whitelist mechanism to ensure that only pre-approved addresses can be set as the `trustedCallee`. This way, only known and trusted contracts can be called via `delegatecall`.

- **Remediation 2:** Use a secure proxy contract pattern where the logic contract and the data contract are separated. The proxy contract should only forward calls to a fixed and audited logic contract, reducing the risk of calling untrusted contracts.