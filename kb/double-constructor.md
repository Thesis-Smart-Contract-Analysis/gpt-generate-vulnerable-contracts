# Double Constructor

## Mô tả

Tại phiên bản 0.4.22, smart contract có thể sử dụng cùng lúc hai loại hàm tạo: hàm tạo trùng tên với smart contract và hàm tạo có tên là `constructor`. Hàm tạo nào được định nghĩa trước sẽ được thực thi.

Ví dụ:

```sol
contract Example {

  address public admin;

  function Example() public {
    admin = address(0x0);
  }

  constructor() public {
    admin = msg.sender;
  }
  
}
```

Việc dùng hai hàm tạo có thể khiến cho smart contract hoạt động không như mong đợi của lập trình viên.

## Cách khắc phục

Chỉ sử dụng một hàm tạo hoặc sử dụng các phiên bản Solidity sau 0.4.22.
