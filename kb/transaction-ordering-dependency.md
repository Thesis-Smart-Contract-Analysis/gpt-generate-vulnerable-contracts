# Transaction Ordering Dependency

Các tên gọi khác: Race Condition, Front Running.

## Mô tả

Miner thường ưu tiên chọn những giao dịch có phí gas cao để cho vào các block. Điều này khiến cho thứ tự gửi lên của các giao dịch không giống với thứ tự thực thi của chúng. 

Lỗ hổng này xảy ra khi kẻ tấn công (có thể là miner) theo dõi danh sách các giao dịch đang chờ được thực thi ở trong blockchain và phát hiện ra một giao dịch nào đó có lợi hoặc gây bất lợi cho kẻ tấn công. Bằng cách tạo ra một giao dịch có phí gas cao hơn, kẻ tấn công có thể thu lợi hoặc hủy bỏ sự bất lợi nhờ vào việc miner luôn chọn những giao dịch có phí gas cao để thực thi.

Ví dụ @manning_2018_sigpsoliditysecurityblog:

```sol
contract FindThisHash {
  
  bytes32 constant public hash = 0xb5b5b97fafd9855eec9b41f74dfb6c38f5951141f9a3ecd7f44d5479b630ee0a;

  constructor() public payable {} // load with ether

  function solve(string solution) public {
    // If you can find the pre image of the hash, receive 1000 ether
    require(hash == sha3(solution));
    msg.sender.transfer(1000 ether);
  }
  
}
```

Trong ví dụ trên, smart contract đưa ra một bài toán là tìm tiền ảnh cho giá trị băm `0xb5b5b97fafd9855eec9b41f74dfb6c38f5951141f9a3ecd7f44d5479b630ee0a` với phần thưởng là 1000 ETH.

Giả sử có một người dùng nào đó tìm ra lời giải là `Ethereum!` và gọi hàm `solve` để nhận phần thưởng. Kẻ tấn công đang theo dõi danh sách các giao dịch sẽ kiểm tra tính đúng đắn của lời giải này và tạo ra một giao dịch có chứa lời giải với phí gas cao hơn giao dịch của nạn nhân.

Miner sẽ thực thi giao dịch của kẻ tấn công trước do nó có phí gas cao và điều này khiến cho kẻ tấn công nhận được 1000 ETH từ smart contract.

## Cách khắc phục

Có thể thiết lập mức gas tối đa cho một giao dịch nhằm ngăn chặn việc người dùng sử dụng giao dịch với phí gas cao để có lợi thế hơn những người dùng khác. 

Tuy nhiên, cách này không thể ngăn chặn được những kẻ tấn công là miner bởi vì họ có thể sắp xếp thứ tự của các giao dịch một cách tùy ý mà không quan tâm đến phí gas. Giải pháp cho vấn đề này là sử dụng mô hình commit-reveal được đề cập ở trong @weak-sources-of-randomness-from-chain-attributes-remediation. 

Cụ thể, mỗi người chơi chỉ gửi lên giá trị băm của lời giải. Bằng cách này, miner không thể sắp xếp các giao dịch do không biết được lời giải thực sự bên trong các giao dịch. Sau khi giao dịch có chứa giá trị băm được đóng vào khối ở trên blockchain, người dùng có thể tiết lộ lời giải để smart contract so khớp với giá trị băm trước đó nhằm quyết định người chiến thắng. 

Dẫu vậy, mô hình commit-reveal cũng không thể che giấu giá trị ETH được gửi cùng với giao dịch và giá trị này có thể là một phần của lời giải cho bài toán của smart contract. Trong trường hợp cần che giấu lượng ETH được gửi cùng giao dịch, có thể sử dụng kỹ thuật Submarine Sends @submarine-sends.
