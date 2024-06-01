# Contracts that lock Ether

## Mô tả

Nếu mã nguồn có các hàm `payable` nhưng không có hàm rút ETH thì sẽ khiến cho ETH bị khóa ở trong hợp đồng thông minh @zaazaa_2023_unveiling.

Ví dụ:

```sol
// source: https://github.com/crytic/slither/wiki/Detector-Documentation#contracts-that-lock-ether

pragma solidity 0.4.24;

contract Locked {
  
    function receive() payable public { }
    
}
```

## Cách khắc phục

Xóa `payable` hoặc thêm vào hàm rút ETH.
