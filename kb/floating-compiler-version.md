# Floating Compiler Version

## Mô tả

Một contract có thể được biên dịch bởi nhiều phiên bản của trình biên dịch khác nhau. 

Ví dụ:

```sol
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

Trong ví dụ trên, smart contract khai báo rất nhiều phiên bản của trình biên dịch theo kiểu SemVer (Semantic Versoning). Điều này có thể dẫn đến việc phiên bản được sử dụng lúc kiểm thử và lúc triển khai smart contract khác nhau. Nếu smart contract được triển khai bởi một phiên bản của trình biên dịch có chứa lỗi thì có thể làm ảnh hưởng đến tính đúng đắn của nó.

## Cách khắc phục

Cần phải cố định phiên bản của trình biên dịch được sử dụng cho smart contract, ví dụ:

```sol
pragma solidity 0.4.25;
// or
pragma solidity =0.4.25;

contract SemVerFloatingPragmaFixed { }
```
