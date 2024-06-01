# Incorrect Constructor Name

## Mô tả

Trong hàm tạo của Solidity thường thực hiện những hành động đặc quyền chẳng hạn như thiết lập chủ sở hữu của smart contract. Trước phiên bản 0.4.22, hàm tạo có tên trùng với tên smart contract. Tuy nhiên, nếu một hàm đáng lẽ được dùng làm hàm tạo nhưng có tên không trùng với tên của smart contract thì nó sẽ trở thành một hàm bình thường và có thể được gọi bởi bất kỳ ai.

Ví dụ:

```sol
/*
 * @source: https://github.com/trailofbits/not-so-smart-contracts/blob/master/wrong_constructor_name/incorrect_constructor.sol
 * @author: Ben Perez
 * Modified by Gerhard Wagner
 */

pragma solidity 0.4.24;

contract Missing {
  
  address private owner;

  modifier onlyowner {
    require(msg.sender==owner);
    _;
  }

  function missing() public {
    owner = msg.sender;
  }

  function () payable { } 

  function withdraw() public onlyowner {
   owner.transfer(this.balance);
  }
  
}
```

Trong ví dụ trên, hàm `missing` đáng lẽ là hàm tạo nhưng có tên không trùng với tên của smart contract `Missing`. Điều này khiến cho bất kỳ ai cũng có thể gọi hàm `missing` để trở thành chủ sở hữu của smart contract.

## Cách khắc phục

Kể từ phiên bản 0.4.22, hàm tạo có tên là `constructor`. Lập trình viên nên nâng cấp phiên bản của smart contract để tránh lỗ hổng này.
