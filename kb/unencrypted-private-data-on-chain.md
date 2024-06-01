# Unencrypted Private Data On-Chain

## Mô tả

Trạng thái hiển thị `private` không đảm bảo rằng giá trị của biến sẽ được giữ bí mật. Bởi vì, khi cập nhật các biến trạng thái, người dùng cần gửi các giao dịch lên blockchain. Các giao dịch này là công khai với tất cả mọi người và có thể được phân tích bởi kẻ tấn công nhằm suy ra giá trị của biến. 

Do tính chất này, smart contract không nên lưu những dữ liệu riêng tư hoặc cần mã hóa.

Ví dụ, xét smart contract `OddEven` sau:

```sol
/*
 * @source: https://gist.github.com/manojpramesh/336882804402bee8d6b99bea453caadd#file-odd-even-sol
 * @author: https://github.com/manojpramesh
 * Modified by Kaden Zipfel
 */

pragma solidity ^0.5.0;

contract OddEven {
  
  struct Player {
    address addr;
    uint number;
  }

  Player[2] private players;
  uint count = 0;

  function play(uint number) public payable {
    require(msg.value == 1 ether, 'msg.value must be 1 eth');
    players[count] = Player(msg.sender, number);
    count++;
    if (count == 2) selectWinner();
  }

  function selectWinner() private {
    uint n = players[0].number + players[1].number;
    (bool success, ) = players[n%2].addr.call.value(address(this).balance)("");
    require(success, 'transfer failed');
    delete players;
    count = 0;
  }
  
}
```

Smart contract trên là một trò chơi giữa hai người chơi. Mỗi người chơi lần lượt gọi hàm `play` với đối số của `number` là một con số bất kỳ. Nếu tổng hai số của hai người chơi (`n`) là chẵn thì người chơi đầu tiên sẽ được nhận toàn bộ ETH của contract. Ngược lại, nếu `n` là lẻ thì người chơi thứ hai sẽ được nhận toàn bộ ETH.

Giả sử người chơi đầu tiên gọi hàm `play` trong một giao dịch có dữ liệu như sau:

```
0x6587f6ec0000000000000000000000000000000000000000000000000000000000000064
```

Người chơi thứ hai sẽ phân tích dữ liệu trên như sau @r_2018_keeping-secrets-on-ethereum:
- `6587f6ec` là 4 byte đầu tiên trong giá trị băm Keccak-256 của "play(uint)".
- `0000000000000000000000000000000000000000000000000000000000000064` là giá trị đối số của `number` được đệm cho đủ 32 byte và có giá trị ở hệ thập phân là 100.

Từ những thông tin này, người chơi thứ hai sẽ chọn một số lẻ bất kỳ để tổng hai số của hai người chơi là số lẻ nhằm nhận được ETH từ smart contract.

## Cách khắc phục

Lưu dữ liệu riêng tư ở bên ngoài blockchain hoặc sử dụng mã hóa. 

Đối với smart contracrt `OddEven` ở trên, có thể áp dụng mô hình commit-reveal tương tự như phần @weak-sources-of-randomness-from-chain-attributes-remediation[]. Cụ thể, các biến trạng thái và cấu trúc trong smart contract phục vụ cho trò chơi sẽ có dạng như sau:

```sol
/*
 * @source: https://github.com/yahgwai/rps
 * @author: Chris Buckland
 * Modified by Kaden Zipfel
 * Modified by Kacper Żuk
 */

contract OddEven {
  
  enum Stage {
    FirstCommit,
    SecondCommit,
    FirstReveal,
    SecondReveal,
    Distribution
  }

  struct Player {
    address addr;
    bytes32 commitment;
    bool revealed;
    uint number;
  }

  Player[2] private players;
  Stage public stage = Stage.FirstCommit;
  // ...
  
}
```

Trò chơi sẽ bao gồm 3 giai đoạn. Giai đoạn đầu tiên là giai đoạn commit:

```sol
contract OddEven {
  
  // ...
  function play(bytes32 commitment) public payable {
    // Only run during commit stages
    uint playerIndex;
    if(stage == Stage.FirstCommit) playerIndex = 0;
    else if(stage == Stage.SecondCommit) playerIndex = 1;
    else revert("only two players allowed");

    // Require proper amount deposited
    // 1 ETH as a bet + 1 ETH as a bond
    require(msg.value == 2 ether, 'msg.value must be 2 eth');

    // Store the commitment
    players[playerIndex] = Player(msg.sender, commitment, false, 0);

    // Move to next stage
    if(stage == Stage.FirstCommit) stage = Stage.SecondCommit;
    else stage = Stage.FirstReveal;
  }
  // ...
  
}
```

Ở giai đoạn này, mỗi người chơi sẽ gửi lên smart contract giá trị băm (`commitment`) của các giá trị sau:
- Địa chỉ của người chơi.
- Con số tham gia trò chơi.
- Một giá trị bí mật.

Ngoài ra, người chơi cũng cần phải gửi thêm 1 ETH nhằm đảm bảo người chơi sẽ phải tiết lộ con số tham gia trò chơi và giá trị bí mật.

Giai đoạn thứ hai là giai đoạn tiết lộ bí mật:

```sol
contract OddEven {

  // ...
  function reveal(uint number, bytes32 blindingFactor) public {
    // Only run during reveal stages
    require(stage == Stage.FirstReveal || stage == Stage.SecondReveal, "wrong stage");

    // Find the player index
    uint playerIndex;
    if(players[0].addr == msg.sender) playerIndex = 0;
    else if(players[1].addr == msg.sender) playerIndex = 1;
    else revert("unknown player");

    // Protect against double-reveal, which would trigger move to Stage.Distribution too early
    require(!players[playerIndex].revealed, "already revealed");

    // Check the hash to prove the player's honesty
    require(keccak256(abi.encodePacked(msg.sender, number, blindingFactor)) == players[playerIndex].commitment, "invalid hash");

    // Update player number if correct
    players[playerIndex].number = number;

    // Protect against double-reveal
    players[playerIndex].revealed = true;

    // Move to next stage
    if(stage == Stage.FirstReveal) stage = Stage.SecondReveal;
    else stage = Stage.Distribution;
  }
  // ...
  
}
```

Ở giai đoạn này, mỗi người chơi sẽ phải tiết lộ con số tham gia trò chơi (`number`) và giá trị bí mật (`blindingFactor`).

Giai đoạn cuối cùng là giai đoạn tính toán kết quả và phân bố ETH:

```sol
contract OddEven {

  // ...
  function distribute() public {
    // Only run during distribution stage
    require(stage == Stage.Distribution, "wrong stage");

    // Find winner
    uint n = players[0].number + players[1].number;

    // Payout winners winnings and bond
    players[n%2].addr.call.value(3 ether)("");

    // Payback losers bond
    players[(n+1)%2].addr.call.value(1 ether)("");

    // Reset the state
    delete players;
    stage = Stage.FirstCommit;
  }
  
}
```

Giai đoạn này sẽ tính toán kết quả và gửi ETH cho các người chơi.
