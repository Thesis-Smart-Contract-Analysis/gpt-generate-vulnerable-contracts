# Built-in Symbol Shadowing

## Mô tả

Lỗ hổng này xảy ra khi lập trình viên dùng các định danh (identifier) có sẵn của Solidity để đặt tên cho biến, hàm, modifier hoặc sự kiện. Điều này có thể thay đổi hành vi mặc định của ngôn ngữ và gây ra các lỗi nghiệp vụ @zaazaa_2023_unveiling.

Ví dụ:

```sol
// source: https://github.com/crytic/slither/wiki/Detector-Documentation#builtin-symbol-shadowing
pragma solidity ^0.4.24;

contract Bug {
  
    uint now; // Overshadows current time stamp.

    function assert(bool condition) public {
        // Overshadows built-in symbol for providing assertions.
    }

    function get_next_expiration(uint earlier_time) private returns (uint) {
        return now + 259200; // References overshadowed timestamp.
    }
    
}
```

Trong ví dụ trên, định danh `now` được đặt tên cho biến còn định danh `assert` được đặt tên cho hàm.

## Cách khắc phục

Thay đổi tên của biến, hàm, modifier hoặc sự kiện mà trùng với tên định danh.
