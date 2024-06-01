# Short Address

## Mô tả

Lỗ hổng này liên quan đến cách mà EVM decode dữ liệu giao dịch. Cụ thể hơn, nó liên quan đến việc hợp đồng thông minh sử dụng đối số có kiểu là địa chỉ (`address`) nhưng không thực hiện kiểm tra độ dài của dữ liệu giao dịch.

Xét ví dụ sau:

```sol
//source: https://ericrafaloff.com/analyzing-the-erc20-short-address-attack/
pragma solidity ^0.4.11;
 
contract MyToken {
  
  mapping (address => uint) balances;
  
  event Transfer(address indexed _from, address indexed _to, uint256 _value);
  
  function MyToken() {
    balances[tx.origin] = 10000;
  }
  
  function sendCoin(address to, uint amount) returns(bool sufficient) {
    if (balances[msg.sender] < amount) return false;
    balances[msg.sender] -= amount;
    balances[to] += amount;
    Transfer(msg.sender, to, amount);
    return true;
  }
  
  function getBalance(address addr) constant returns(uint) {
    return balances[addr];
  }
  
}
```

Giao dịch thực thi hàm `sendCoin()` có dạng như sau:

```
0x90b98a11
00000000000000000000000062bec9abe373123b9b635b75608f94eb8644163e
0000000000000000000000000000000000000000000000000000000000000002
```

Với:
- `0x90b98a11` là định danh hàm.
- `00000000000000000000000062bec9abe373123b9b635b75608f94eb8644163e` là đối số thứ nhất: địa chỉ của bên nhận token. 
- `0000000000000000000000000000000000000000000000000000000000000002` là đối số thứ hai: lượng token cần gửi.

Giả sử ứng dụng sử dụng hợp đồng thông minh trên cố định lượng token chuyển đi là 2 và chỉ nhận dữ liệu đầu vào là địa chỉ của bên nhận token.

Kẻ tấn công có thể sử dụng một địa chỉ có kích thước là 19 byte. Dữ liệu giao dịch có dạng như sau #footnote[Ký tự xuống dòng là để cho dễ nhìn, dữ liệu giao dịch không có ký tự này.]:

```
0x90b98a11
00000000000000000000000062bec9abe373123b9b635b75608f94eb86441600
00000000000000000000000000000000000000000000000000000000000002  
                                                              ^^
                                                The missing byte
```

Sự kiện `Transfer` được kích hoạt có các giá trị như sau:
- `_from`: `0x58bad47711113aea5bc5de02bce6dd7aae55cce5`
- `_ to`: `0x62bec9abe373123b9b635b75608f94eb86441600`
- `_value`: `512`

Có thể thấy, byte `00` đầu tiên của đối số thứ hai được xem như là byte cuối cùng của đối số thứ nhất. Điều này khiến cho đối số thứ hai bị mất một byte. EVM xử lý vấn đề này bằng cách đệm thêm một byte `00` vào bên phải của đối số thứ hai, khiến cho giá trị của nó từ `0x02` (2) thành `0x0200` (512).

Như vậy, kẻ tấn công đã tạo ra một giao dịch với lượng token được chuyển đi gấp 256 lần. 

Việc có một địa chỉ với byte cuối là `0x0` và hợp đồng thông minh có ít nhất 512 token là không quá khó xảy ra.

## Cách khắc phục

Thực hiện kiểm tra kích thước của dữ liệu giao dịch.

Ví dụ:

```sol
// source: https://www.reddit.com/r/ethereum/comments/63s917/comment/dfwmhc3/
contract NonPayloadAttackableToken {
  
  modifier onlyPayloadSize(uint size) {
    assert(msg.data.length == size + 4);
    _;
  } 
  
  function transfer(address _to, uint256 _value) onlyPayloadSize(2 * 32) {
    // do stuff
  }
  
}
```

Trong ví dụ trên:
- `msg.data` chứa dữ liệu giao dịch và thuộc tính `length` cho biết kích thước của dữ liệu giao dịch.
- Giá trị 4 byte cộng thêm chính là kích thước của định danh hàm.

Kể từ phiên bản 0.5.0, lỗ hổng này đã được giải quyết. Cụ thể, khi dữ liệu giao dịch không đủ kích thước thì giao dịch sẽ bị hoàn trả @v0.5.0-soliditychangelogmd.
