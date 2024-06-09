# Smart contract

```solidity
pragma solidity >=0.4.0 < 0.6.0;
pragma solidity >=0.4.0<0.6.0;
pragma solidity >=0.4.14 <0.6.0;
pragma solidity >0.4.13 <0.6.0;
pragma solidity 0.4.24 - 0.5.2;
pragma solidity >=0.4.24 <=0.5.3 ~0.4.20;
pragma solidity <0.4.26;
pragma solidity ~0.4.20;
pragma solidity ^0.4.14;
pragma solidity 0.4.*;
pragma solidity 0.*;
pragma solidity *;
pragma solidity 0.4;
pragma solidity 0;

contract SemVerFloatingPragma { }
```

Description of the vulnerability: The smart contract `SemVerFloatingPragma` has a Floating Compiler Version vulnerability where multiple versions of the Solidity compiler are specified in the pragma statements. This can lead to inconsistencies in the compiler version used during testing and deployment, potentially introducing unexpected behavior or vulnerabilities.

# Remediations

- Specify a fixed version of the Solidity compiler in the pragma statement to ensure consistency in compilation:
  
  ```solidity
  pragma solidity =0.4.25;
  
  contract SemVerFloatingPragmaFixed { }
  ```

By fixing the Solidity compiler version in the pragma statement, you can mitigate the Floating Compiler Version vulnerability and ensure that the smart contract is compiled consistently across different environments.