# Timestamp Dependency <timestamp-dependency>

## Mô tả

Smart contract có thể sử dụng các thuộc tính của block chẳng hạn như `block.timestamp` hoặc `block.number` làm điều kiện để thực thi một hành động nào đó. Tuy nhiên, việc smart contract phụ thuộc vào các giá trị này là không an toàn:
- Trong trường hợp của `block.timestamp`, miner có thể thay đổi nhãn thời gian#footnote[Tất nhiên là không được nhỏ hơn nhãn thời gian của block trước đó hoặc quá xa trong tương lai (không quá 900 giây - tương ứng với 15 phút @luu_2016_making).] của block nên giá trị của nó có thể không như lập trình viên smart contract mong đợi.
- Trường hợp của `block.number` cũng tương tự, giá trị này có thể biến thiên nhanh hơn hoặc chậm đi tùy thuộc vào thời gian đào một block trong mạng blockchain. Mà thời gian đào một block không cố định và có thể thay đổi vì nhiều lý do chẳng hạn như blockchain tổ chức lại sau khi fork.

Ví dụ:

```sol
pragma solidity ^0.5.0;

contract TimedCrowdsale {

  event Finished();
  event notFinished();

  // Sale should finish exactly at January 1, 2019
  function isSaleFinished() private returns (bool) {
    return block.timestamp >= 1546300800;
  }

  function run() public {
    if (isSaleFinished()) {
      emit Finished();
    } else {
      emit notFinished();
    }
  }

}
```

Smart contract trên sử dụng điều kiện `block.timestamp >= 1546300800` để phát ra sự kiện `Finished`. Giả sử thời gian hiện tại là 1546300000 (cách thời điểm kết thúc 800 giây và nhỏ hơn giới hạn 900 giây của Ethereum). Kẻ tấn công có thể làm cho sự kiện `Finished` được phát ra sớm hơn bằng cách gán nhãn thời gian cho block là thời điểm kết thúc (1546300800).

## Cách khắc phục

- Lập trình viên cần chú ý đến tính khả biến của các thuộc tính liên quan đến block khi sử dụng trong smart contract.
- Sử dụng Oracle #footnote[Là một loại công nghệ cho phép smart contract kết nối đến thế giới bên ngoài, thường là để lấy các số ngẫu nhiên hoặc dữ liệu thời gian thực] nếu có nhu cầu sinh số ngẫu nhiên (tương tự như phần @weak-sources-of-randomness-from-chain-attributes-remediation[]).
  

