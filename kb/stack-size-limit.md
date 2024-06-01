# Stack Size Limit

## Mô tả

Mỗi lần smart contract gọi thực thi hàm của  smart contract khác (hoặc gọi đến chính nó thông qua `this.f()`), call stack tương ứng với giao dịch sẽ tăng lên một frame @atzei_2017_a. Giới hạn của call stack cho mỗi giao dịch là 1024 @solidity-1024-call-stack-depth. Khi chạm đến giới hạn này, tất cả các lời gọi hàm đến bên ngoài smart contract (hoặc `this.f()`) đều gây ra ngoại lệ.

Kẻ tấn công có thể khai thác tính chất này để tạo ra một giao dịch có call stack gần đầy trước khi gọi hàm trong smart contract để gây ra ngoại lệ. Nếu ngoại lệ không được xử lý thì smart contract có thể rơi vào trạng thái từ chối dịch vụ.

Ví dụ, xét smart contract sau:

```sol
contract Government {

  // ...
  function lendGovernmentMoney() returns (bool) {
    uint amount = msg.value;
    if (lastTimeOfNewCredit + ONE_MINUTE < block.timestamp) {
      // Return money to sender
      msg.sender.send(amount);
      // Sends all contract money to the last creditor
      creditorAddresses[creditorAddresses.length - 1].send(profitFromCrash);
      corruptElite.send(this.balance);
      // Reset contract state
      lastTimeOfNewCredit = block.timestamp;
      profitFromCrash = 0;
      creditorAddresses = new address[](0);
      creditorAmounts = new uint[](0);
      round += 1;
      return false;
    }
    // ...
  }
  // ...
  
}
```

Kẻ tấn công có thể là chủ sở hữu smart contract và ý định của người này là không chuyển ETH cho người chiến thắng. Để khai thác lỗ hổng, kẻ tấn công xây dựng một smart contract như sau:

```sol
contract Attacker {
  
  function attack(address target, uint count) {
    if (0 <= count && count < 1023) {
      this.attack.gas(msg.gas - 2000)(target, count + 1);
    } else {
      Governmental(target).lendGovernmentMoney();
    }
  }
  
}
```

Có thể thấy, hàm `attack` của `Attacker` tự gọi đến chính nó 1022 lần. Sau đó, nó gọi đến hàm `lendGovernmentMoney` của `Governmental`. Độ sâu của call stack lúc này là 1023.

Khi `lendGovernmentMoney` gọi hàm `send` lần đầu tiên (`msg.sender.send(amount)`), call stack sẽ có độ sâu là 1024. Điều này sẽ gây ra ngoại lệ và khiến giao dịch bị hoàn trả.

## Cách khắc phục

Sau khi có EIP-150 @eip-150, smart contract gọi hàm chỉ cung cấp 63/64 lượng gas còn lại cho smart contract khác. 

Cụ thể, lượng gas R được giữ lại ở smart contract gọi hàm sẽ là @eip-150-and-the-63-64-rule-for-gas:

$
R = A - 63/64 * A
$

Với $A$ là lượng gas khả dụng tối đa ở độ sâu $N$ của call stack (không tính lượng gas tiêu thụ bởi những thao tác khác trong hàm). Giá trị này được tính như sau:

$
A = I * (63/64)^N
$

Với I là lượng gas ban đầu (tại độ sâu 0 của call stack).

Ví dụ, gas ban đầu là 3000 thì:
- Độ sâu $N = 10$ sẽ có $3000 * (63/64)^{10} = 2562$ gas khả dụng.
- Độ sâu $N = 20$ sẽ có $3000 * (63/64)^{20} = 2189$ gas khả dụng.



#figure(image("imgs/Gas available graph.png"), caption: [Minh họa tỷ lệ gas khả dụng theo độ sâu của ngăn xếp])

Có thể thấy, lượng gas khả dụng giảm rất nhanh xuống 0 và giúp tránh được việc call stack bị tràn.
