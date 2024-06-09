# Assert and Require Violation

## Xử lý ngoại lệ trong Solidity

Solidity sử dụng các ngoại lệ hoàn trả trạng thái (state-reverting exception) để xử lý lỗi. Cụ thể, các ngoại lệ này sẽ hủy bỏ các sự thay đổi trên các biến trạng thái. Khi ngoại lệ xảy ra trong một lời gọi hàm đến smart contract khác, nó sẽ được lan truyền đến smart contract hiện tại trừ khi được xử lý bởi câu lệnh `try/catch`.

Các ngoại lệ chứa một thực thể thuộc kiểu `error`. Có hai loại thực thể `error` có sẵn là `Panic(uint256)` và `Error(string)`.

`Panic(uint256)` được gây ra bởi hàm `assert`. Hàm này chỉ nên được sử dụng để kiểm tra các lỗi bên trong (internal error) và các giá trị bất biến (invariant). Nếu có ngoại lệ xảy ra, `assert` sẽ tiêu thụ hết lượng gas còn lại.

Mỗi internal error sẽ tương ứng với một mã lỗi, một số internal error phổ biến:
- `0x11`: Nếu một thao tác tính toán bị tràn số (overflow/underflow) nằm bên ngoài khối `unchecked{ ... }`.
- `0x12`: Xảy ra khi chia cho 0 chẳng hạn như `5 / 0` hoặc `23 % 0`.
- `0x21`: Nếu chuyển một giá trị quá lớn hoặc số âm thành một kiểu enum.
- `0x31`: Nếu gọi hàm `.pop()` cho mảng rỗng.
- `0x32`: Nếu truy cập vào một mảng, bytesN (mảng các byte có kích thước cố định chẳng hạn như `bytes1`, `bytes2`, ...) hoặc một lát cắt của mảng (array slice) tại một chỉ số nằm bên ngoài phạm vi hoặc có giá trị âm. Ví dụ: `x[i]` với `i >= x.length` hoặc `i < 0`.
- `0x41`: Nếu cấp phát quá nhiều bộ nhớ hoặc tạo mảng quá lớn.

`Error(string)` được gây ra bởi hàm `require`. Hàm này được sử dụng để kiểm tra dữ liệu đầu vào và giá trị trả về của lời gọi hàm đến các smart contract khác. Nếu có ngoại lệ xảy ra, `require` sẽ hoàn trả lại lượng gas còn lại.

Ví dụ bên dưới minh họa cho việc sử dụng `require` và `assert`:

```sol
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.5.0 <0.9.0;

contract Sharer {
  
    function sendHalf(address payable addr) public payable returns (uint balance) {
        require(msg.value % 2 == 0, "Even value required.");
        uint balanceBeforeTransfer = address(this).balance;
        addr.transfer(msg.value / 2);
        // Since transfer throws an exception on failure and
        // cannot call back here, there should be no way for us to
        // still have half of the Ether.
        assert(address(this).balance == balanceBeforeTransfer - msg.value / 2);
        return address(this).balance;
    }
    
}
```

Kiểu `error` còn có thể được định nghĩa và sử dụng với câu lệnh `revert` như sau:

```sol
pragma solidity ^0.8.4;

error InsufficientBalance(uint256 available, uint256 required);

contract TestToken {
  
  mapping(address => uint) balance;
  
  function transfer(address to, uint256 amount) public {
    if (amount > balance[msg.sender])z
      revert InsufficientBalance({
        available: balance[msg.sender],
        required: amount
      });
    balance[msg.sender] -= amount;
    balance[to] += amount;
  }
  // ...
  
}
```

## Mô tả

Các hàm hoạt động đúng không nên gây ra `Panic(uint256)`, kể cả khi dữ liệu đầu vào không đúng. Nếu điều này xảy ra thì đồng nghĩa với việc dùng `assert` sai mục đích hoặc smart contract tồn tại lỗi cần phải sửa chữa.

Ví dụ:

```sol
/*
 * @source: ChainSecurity
 * @author: Anton Permenev
 */
pragma solidity ^0.4.21;

contract GasModel{
  
  uint x = 100;
  function check(){
    uint a = gasleft();
    x = x + 1;
    uint b = gasleft();
    assert(b > a);
  }
  
}
```

Trong ví dụ trên, hàm `assert` có đối số là `b > a`. Tuy nhiên, thao tác cập nhật biến trạng thái (`x = x + 1`) sẽ tiêu thụ gas nên giá trị của `b` sẽ không bao giờ lớn hơn giá trị của `a`. Như vậy, hàm `assert` sẽ luôn hoàn trả giao dịch và sử dụng hết lượng gas còn lại.

Đối với `require`, nếu hàm này luôn hoàn trả giao dịch và lượng gas còn lại thì đó có thể là dấu hiệu của việc:
- Tồn tại lỗi trong smart contract cần phải sửa chữa.
- Biểu thức luận lý truyền vào hàm `require` khó thỏa mãn.

Ví dụ:

```sol
pragma solidity ^0.4.25;

contract Bar {
  
  Foo private f = new Foo();
  function doubleBaz() public view returns (int256) {
    return 2 * f.baz(0);
  }
  
}

contract Foo {
  
  function baz(int256 x) public pure returns (int256) {
    require(0 < x);
    return 42;
  }
  
}
```

Hàm `doubleBaz` của smart contract `Bar` gọi hàm `baz` của smart contract `Foo` nhưng luôn truyền giá trị 0 vào tham số `x`. Điều này khiến cho hàm `require` trong hàm `baz` luôn gây ra ngoại lệ và hoàn trả giao dịch cũng như là lượng gas còn lại.

## Cách khắc phục

Đối với `assert`: cần phải sử dụng `assert` đúng mục đích và sửa lỗi mà làm `assert` luôn gây ra ngoại lệ. 

Trong ví dụ của smart contract `GasModel` ở trên, cần sửa lại biểu thức luận lý truyền vào hàm `assert` như sau:

```sol
/*
 * @source: ChainSecurity
 * @author: Anton Permenev
 */
pragma solidity ^0.4.21;

contract GasModelFixed{
  
  uint x = 100;
  function check(){
    uint a = gasleft();
    x = x + 1;
    uint b = gasleft();
    assert(b < a);
  }
  
}
```

Đối với `require`: cần phải đảm bảo rằng biểu thức luận lý truyền vào hàm `require` có thể thỏa mãn. 

Trong ví dụ của smart contract `Bar` và `Foo` ở trên, có thể sửa lại bằng cách thay đổi đối số truyền vào hàm `baz` hoặc sửa kiểu dữ liệu của tham số `x` thành số nguyên không dấu:

```sol
pragma solidity ^0.4.25;

contract Bar {
  
  Foo private f = new Foo();
  function doubleBaz() public view returns (int256) {
    return 2 * f.baz(1); // Changes the external contract to not hit the overly strong requirement.
  }
  
}

contract Foo {
  
  function baz(int256 x) public pure returns (int256) {
    require(0 < x); // You can also fix the contract by changing the input to the uint type and removing the require
    return 42;
  }
  
}
```