# Unexpected Balance

## Mô tả

Ngoài việc nhận ETH từ các hàm `payable`, smart contract còn có thể nhận ETH thông qua một số cách khác chẳng hạn như hàm `selfdestruct`.

Việc giả định rằng ETH chỉ đến từ các hàm `payable` và thực hiện các phép so sánh đối với biến `this.balance` có thể làm ảnh hưởng đến kết quả thực thi của smart contract. Trong trường hợp xấu nhất, điều này có thể làm smart contract rơi vào trạng thái từ chối dịch vụ.

Ví dụ sau đây @self-destruct-ref là một trò chơi cho phép các người chơi đặt ETH vào smart contract thông qua hàm `deposit`. 

```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract EtherGame {
  
  uint256 public targetAmount = 7 ether;
  address public winner;

  function deposit() public payable {
    require(msg.value == 1 ether, "You can only send 1 Ether");

    uint256 balance = address(this).balance;
    require(balance <= targetAmount, "Game is over");

    if (balance == targetAmount) {
      winner = msg.sender;
    }
  }

  function claimReward() public {
    // ...
  }
    
}
```

Có thể thấy, mỗi người chơi chỉ có thể đặt 1 ETH một lần và nếu người chơi nào làm cho số dư của smart contract chạm mốc 7 ETH thì sẽ trở thành người chiến thắng.

Kẻ tấn công có thể xây dựng một smart contract như sau:

```sol
contract Attacker {
  
  EtherGame etherGame;

  constructor(EtherGame _etherGame) {
    etherGame = EtherGame(_etherGame);
  }

  function attack() public payable {
    address payable addr = payable(address(etherGame));
    selfdestruct(addr);
  }
  
}
```

Hàm `attack` trong smart contract `Attacker` sẽ xóa bytecode của smart contract này trên blockchain rồi ép smart contract `EtherGame` nhận ETH thông qua hàm `selfdestruct`. 

Giả sử người chơi A đặt vào trò chơi 1 ETH, kẻ tấn công khởi tạo smart contract `Attacker` với `msg.value` là 7. Sau đó, kẻ tấn công gọi hàm `attack` để hủy bytecode của `Attacker` và chuyển 7 ETH sang cho `EtherGame`. Điều này khiến cho số dư (`this.balance`) của `EtherGame` có giá trị là 8 và khiến cho những người dùng khác không thể đặt cọc cũng như là trờ thành người chiến thắng (từ chối dịch vụ).

Còn một cách khác để ép smart contract nhận ETH mà không thông qua việc gọi hàm. Cụ thể, kẻ tấn công xác định các địa chỉ smart contract mà một địa chỉ có thể tạo ra. Khi đó, kẻ tấn công sẽ gửi trước ETH vào các địa chỉ này và làm cho số dư của smart contract được tạo ra có giá trị khác 0.

Công thức dùng để tính toán địa chỉ của smart contract:

```sol
keccak256(rlp.encode([<account_address>, <transaction_nonce>]))
```

Với:
- `keccak256` là một hàm băm.
- `rlp.encode` là minh họa cho việc encode dữ liệu theo giao thức RLP (Recursive-Length Prefix).
- `account_address` là địa chỉ tạo ra smart contract.
- `transanction_nonce` có giá trị bắt đầu bằng 1 và tăng dần theo thời gian khi có một giao dịch được gửi đi từ địa chỉ.

## Cách khắc phục

Không sử dụng giá trị `this.balance` làm điều kiện để thực thi những hành động quan trọng. Thay vào đó, có thể sử dụng một biến để đếm lượng ETH được chuyển đến smart contract thông qua các hàm `payable`.

Ví dụ, đối với smart contract `EtherGame` trên, có thể dùng thêm biến `depositedEther` như sau:

```sol
contract EtherGame {
  
  uint256 public targetAmount = 7 ether;
  address public winner;
  uint public depositedEther;

  function deposit() public payable {
    require(msg.value == 1 ether, "You can only send 1 Ether");

    uint balance = depositedEther + msg.value;
    require(balance <= targetAmount, "Game is over");

    if (balance == targetAmount) {
      winner = msg.sender;
    }

    depositedEther += msg.value;
  }

  function claimReward() public {
    // ...
  }
    
}
```
