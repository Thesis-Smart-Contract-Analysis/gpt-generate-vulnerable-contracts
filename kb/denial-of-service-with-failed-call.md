# Denial of Service with Failed Call

## Mô tả

Các lời gọi đến bên ngoài smart contract (thực thi hàm hoặc chuyển ETH) có thể thất bại một cách không có hoặc có chủ đích. Trong trường hợp kẻ tấn công gọi đến bên ngoài smart contract nhiều lần trong cùng một giao dịch, smart contract có thể trở nên không khả dụng.

Ví dụ:

```sol
contract DistributeTokens {
  address public owner; // gets set somewhere
  address[] investors; // array of investors
  uint[] investorTokens; // the amount of tokens each investor gets

  // ... extra functionality, including transfertoken()

  function invest() public payable {
    investors.push(msg.sender);
    investorTokens.push(msg.value * 5); // 5 times the wei sent
  }

  function distribute() public {
    require(msg.sender == owner); // only owner
    for(uint i = 0; i < investors.length; i++) {
      // here transferToken(to,amount) transfers "amount" of tokens to the address "to"
      transferToken(investors[i],investorTokens[i]);
    }
  }
}
```

Trong ví dụ này, kẻ tấn công có thể tạo ra một lượng lớn các địa chỉ và lưu vào mảng `investors` thông qua hàm `invest`. Nếu kích thước của mảng `investors` quá lớn, việc lặp qua từng phần tử của nó và thực hiện chuyển token (`transferToken`) có thể gây ra ngoại lệ hết gas (out-of-gas exception). Khi đó, các lời gọi hàm `transferToken` thành công trong giao dịch sẽ bị hủy bỏ và khiến cho smart contract không còn khả dụng.

Ví dụ khác, smart contract sau đây thực hiện gửi ETH cho người đặt cược cao nhất.

```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BadAuction {

  address payable highestBidder;
  uint highestBid;

  function bid() public payable {
    require(msg.value >= highestBid);

    if (highestBidder != address(0)) {
      highestBidder.transfer(highestBid);
    }

    highestBidder = payable(msg.sender);
    highestBid = msg.value;
  }
  
}
```

Smart contract này có thể bị tấn công DoS nếu kẻ tấn công luôn làm cho hàm `transfer` gây ra ngoại lệ:

```sol
contract Attacker {
  
  BadAuction badAuction;

  constructor(address badAuctionAddress) {
    badAuction = BadAuction(badAuctionAddress);
  }

  function bid() public payable {
    badAuction.bid{value: msg.value}();
  }

  receive() external payable {
    revert();
  }
    
}
```

Cụ thể, kẻ tấn công sẽ đặt cược và trở thành người đặt cược lớn nhất thông qua hàm `bid` của smart contract `Attacker`. Sau đó, không ai có thể trở thành người đặt cược lớn nhất được nữa do hàm `fallback` của `Attacker` luôn gây ra ngoại lệ và hoàn trả giao dịch. Điều này làm mất đi tính sẵn sàng của smart contract.

## Cách khắc phục

Những điều cần lưu ý khi thực hiện gọi đến bên ngoài smart contract:
- Không gọi đến bên ngoài smart contract nhiều lần trong cùng một giao dịch.
- Luôn giả định rằng lời gọi đến bên ngoài smart contract có thể thất bại.
- Xử lý các lời gọi thất bại.

Đối với việc chuyển ETH, có thể áp dụng mẫu bảo mật Pull-over-Push @solidity-patterns để tạo ra một hàm cho phép người dùng có thể rút ETH thay vì tự động chuyển cho họ. 

Ví dụ:

```sol
contract PullOverPush {

  mapping(address => uint) credits;

  function allowForPull(address receiver, uint amount) private {
    credits[receiver] += amount;
  }

  function withdrawCredits() public {
    uint amount = credits[msg.sender];

    require(amount != 0);
    require(address(this).balance >= amount);

    credits[msg.sender] = 0;

    msg.sender.transfer(amount);
  }
}
```
