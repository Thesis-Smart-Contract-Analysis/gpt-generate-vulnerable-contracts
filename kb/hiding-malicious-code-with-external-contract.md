# Hiding Malicious Code with External Contract

## Mô tả

Trong Solidity, bất kỳ địa chỉ nào cũng có thể được ép kiểu thành một thực thể của hợp đồng thông minh. Kẻ tấn công có thể lợi dụng điều này để giấu mã độc @hiding-malicious-code-with-external-contract-ref.

Trong ví dụ dưới, kẻ tấn công triển khai `Foo` ở trên chuỗi khối với đối số hàm tạo là địa chỉ của `Mal`. Trong hàm tạo, `Foo` ép kiểu đối số thành một thực thể của `Bar`.

```sol
// source: https://solidity-by-example.org/hacks/hiding-malicious-code-with-external-contract/
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
contract Foo {
    Bar bar;

    constructor(address _bar) {
        bar = Bar(_bar);
    }

    function callBar() public {
        bar.log();
    }
}

contract Bar {
    event Log(string message);

    function log() public {
        emit Log("Bar was called");
    }
}

contract Mal {
    event Log(string message);

    function log() public {
        emit Log("Mal was called");
    }
}
```

Giả sử người dùng chỉ đọc được mã nguồn của `Foo` và `Bar`, họ thấy rằng hai hợp đồng thông minh này không có vấn đề gì và gọi sử dụng hàm `Foo.callBar()`. Người dùng mong muốn hàm `Bar.log()` được gọi nhưng trên thực tế thì `Mal.log()` mới là hàm được gọi.

Kẻ tấn công cũng có thể sử dụng hàm fallback để chứa mã độc.

## Cách khắc phục

Có thể sử dụng những cách sau:
- Khởi tạo một thực thể mới của hợp đồng thông minh ở trong hàm tạo.
- Sử dụng trạng thái hiển thị của biến thực thể là `public` để người dùng có thể kiểm tra mã nguồn của hợp đồng thông minh trước khi thực thi hàm.

Minh họa:

```sol
contract Foo {
  Bar public bar;
  // ...
  constructor() public {
      bar = new Bar();
  }
  // ...
}
```
