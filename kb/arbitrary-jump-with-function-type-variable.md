# Arbitrary Jump with Function Type Variable

## Kiểu dữ liệu hàm trong Solidity

Là một tham chiếu đến hàm với một nguyên mẫu hàm cụ thể. Biến thuộc kiểu dữ liệu này có thể được gọi thực thi tương tự như các hàm thông thường.

Ví dụ, đoạn mã sau giúp thay đổi hàm cần thực thi giữa `add` và `sub` một cách linh động khi chạy:

```sol
// source: https://medium.com/authio/solidity-ctf-part-2-safe-execution-ad6ded20e042
pragma solidity ^0.4.23;

contract AddSub {
    
  function add(uint a, uint b) internal pure returns (uint) {
    return a + b;
  }
  
  function sub(uint a, uint b) internal pure returns (uint) {
    return a - b;
  }
  
  function math(uint _a, uint _b, bool _add) public pure returns (uint) {
    function (uint, uint) internal pure returns (uint) func;
    func = _add ? add : sub;
    return func(_a, _b);
  }
}
```

## Mô tả

Kẻ tấn công có thể sử dụng các chỉ thị hợp ngữ (assembly instruction) chẳng hạn như `mstore` hoặc toán tử gán bằng để thay đổi tham chiếu của biến có kiểu là hàm đến bất kỳ chỉ thị nào nhằm phá vỡ các giới hạn truy cập và thay đổi các biến trạng thái.

Trong ví dụ bên dưới, cách duy nhất để kẻ tấn công gọi hàm `withdraw()` để rút ETH là thông qua hàm `breakIt()`. Tuy nhiên, câu lệnh `require()` trong hai hàm này mâu thuẫn với nhau và mục tiêu của kẻ tấn công là vượt qua được câu lệnh `require()` ở trong hàm `withdraw()`.

```sol
/*
 * @source: https://gist.github.com/wadeAlexC/7a18de852693b3f890560ab6a211a2b8
 * @author: Alexander Wade
 */

pragma solidity ^0.4.25;

contract FunctionTypes {

  constructor() public payable { require(msg.value != 0); }

  function withdraw() private {
    require(msg.value == 0, 'dont send funds!');
    address(msg.sender).transfer(address(this).balance);
  }

  function frwd() internal { 
    withdraw(); 
  }

  struct Func { 
    function () internal f; 
  }

  function breakIt() public payable {
    require(msg.value != 0, 'send funds!');
    Func memory func;
    func.f = frwd;
    assembly { 
      mstore(func, add(mload(func), callvalue))
    }
    func.f();
  }
}
```

Lỗ hổng tồn tại trong đoạn mã hợp ngữ giúp trỏ biến `func` đến vị trí của một chỉ thị ở trong bytecode.

- Mã lệnh `mstore` có nguyên mẫu hàm là `mstore(p, v)` và được dùng để lưu giá trị `v` vào vùng nhớ `p`. 
- Giá trị sẽ được lưu vào vùng nhớ là `add(mload(func), callvalue)`. Với:
  - Mã lệnh `callvalue` giúp đẩy `msg.value` vào ngăn xếp.
  - Mã lệnh `mload` giúp đẩy giá trị vùng nhớ ban đầu của `func` lên ngăn xếp.

Để nhảy đến một ví trí bất kỳ, mà cụ thể là sau câu lệnh `require()` ở trong hàm `withdraw()`, kẻ tấn công chỉ cần dựa trên giá trị ban đầu của `func` và vị trí của chỉ thị cần nhảy đến ở trong bytecode để tìm ra giá trị `msg.value` cần sử dụng.

## Cách khắc phục

Hạn chế việc sử dụng hợp ngữ và không cho phép người dùng có thể gán các giá trị tùy ý cho các biến có kiểu là hàm.
