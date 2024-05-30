# Typographical Error

## Mô tả

Lỗi đánh máy có thể dẫn đến những hành vi không mong muốn trong smart contract. 

Ví dụ:

```sol
pragma solidity ^0.4.25;

contract TypoOneCommand {
  uint numberOne = 1;

  function alwaysOne() public {
    numberOne =+ 1;
  }
}
```

Có thể thấy, phép toán `numberOne += 1` được viết nhầm thành `numberOne =+ 1`. Biểu thức này có ý nghĩa là gán `numberOne` cho giá trị `+1` thay vì cộng `numberOne` cho 1.

## Cách khắc phục

Lỗi này có thể được tránh khỏi nếu kiểm tra các điều kiện cần thiết trước khi thực hiện tính toán hoặc dùng thư viện SafeMath của OpenZeppelin.

Ngoài ra, toán tử một ngôi `+` đã bị loại bỏ kể từ phiên bản 0.5.0 @solidity-v0.5.0-breaking-changes của Solidity.
