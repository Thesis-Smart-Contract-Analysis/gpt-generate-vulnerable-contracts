# Insufficient Gas Griefing

## Mô tả

Xảy ra khi smart contract không kiểm tra xem nó có đủ gas để gọi đến smart contract khác hay không. Kẻ tấn công có thể cung cấp thiếu gas nhằm khiến cho lời gọi đến smart contract khác bị thất bại và làm kết quả của smart contract bị sai lệch.

Ví dụ:

```sol
/*
 * @source: https://consensys.github.io/smart-contract-best-practices/known_attacks/#insufficient-gas-griefing
 * @author: ConsenSys Diligence
 * Modified by Kaden Zipfel
 */

pragma solidity ^0.5.0;

contract Relayer {
  
  uint transactionId;

  struct Tx {
    bytes data;
    bool executed;
  }

  mapping (uint => Tx) transactions;

  function relay(Target target, bytes memory _data) public returns(bool) {
    // replay protection; do not call the same transaction twice
    require(transactions[transactionId].executed == false, 'same transaction twice');
    transactions[transactionId].data = _data;
    transactions[transactionId].executed = true;
    transactionId += 1;

    (bool success, ) = address(target).call(abi.encodeWithSignature("execute(bytes)", _data));
    return success;
  }
  
}

contract Target {
  
  function execute(bytes memory _data) public {
    // Execute contract code
  }
  
}
```

Trong ví dụ trên, smart contract `Relayer` thực hiện chuyển tiếp lời gọi hàm đến smart contract `Target` thông qua hàm `relay`. Cụ thể, hàm `relay` dùng hàm `call` để gọi đến hàm `execute` của smart contract `Target`.

Kẻ tấn công có thể chỉ cung cấp lượng gas vừa đủ để thực thi hàm `relay` nhưng không đủ để thực thi hàm `execute`. Khi đó, hàm `execute` sẽ gây ra ngoại lệ hết gas (out-of-gas exception). Nếu `Relayer` không kiểm tra và hoàn trả giao dịch dựa trên giá trị trả về của hàm `call` thì có thể làm ảnh hưởng đến kết quả thực thi của smart contract.

## Cách khắc phục

Kiểm tra xem lượng gas được cung cấp có đủ để thực thi lời gọi hàm đến smart contract khác hay không. 

Ví dụ @oualid_2022_smart-contract-gas-griefing-attack:

```sol
pragma solidity ^0.5.0;

contract Relayer {
  uint public estimatedGasValue = 1000000;
  uint public gasNeededBetweenCalls = 5000;
  
  uint transactionId;

  struct Tx {
    bytes data;
    bool executed;
  }

  mapping (uint => Tx) transactions;

  function relay(Target target, bytes memory _data) public returns(bool) {
    // replay protection; do not call the same transaction twice
    require(transactions[transactionId].executed == false, 'same transaction twice');
    transactions[transactionId].data = _data;
    transactions[transactionId].executed = true;
    transactionId += 1;

    uint gasAvailable = gasleft() - gasNeededBetweenCalls;
    require(gasAvailable - gasAvailable/64 >= estimatedGasValue, "not enough gas provided");
    
    (bool success, ) = address(target).call(abi.encodeWithSignature("execute(bytes)", _data));
    return success;
  }
  
}
```

Trong ví dụ trên, giá trị `estimatedGasValue` là lượng gas ước lượng cần để thực thi hàm `execute` còn giá trị `gasNeededBetweenCalls` là lượng gas cần dùng để thực hiện hai dòng lệnh trước lời gọi hàm `call`. Lý do trừ đi `gasAvailable/64` là vì 1/64 lượng gas khả dụng trong smart contract sẽ được giữ lại ở `Relayer` @eip-150-and-the-63-64-rule-for-gas.

Ngoài ra, nên giới hạn danh sách người dùng tin cậy có thể thực thi các hàm chuyển tiếp trong smart contract.
