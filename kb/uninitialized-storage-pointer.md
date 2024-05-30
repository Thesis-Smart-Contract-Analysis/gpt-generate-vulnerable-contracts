# Uninitialized Storage Pointer

## Bố cục lưu trữ của Solidity <storage-layout>

Trước khi phân tích lỗ hổng, ta cần hiểu về cách Solidity lưu các biến `storage`. Nói một cách đơn giản, các biến `storage` được Solidity lưu liên tiếp ở trong các khe lưu trữ (slot). Có tổng cộng $2^{256}$ khe lưu trữ, mỗi khe lưu trữ có kích thước 32 byte và được đánh số từ 0 đến $2^{256} - 1$ @voitier_2023_exploring-the-storage-layout-in-solidity-and-how-to-access-state-variables, @a2018_understanding-ethereum-smart-contract-storage. 

Xét ví dụ sau:

```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

contract StorageLayout {
  uint256 x = 1; // slot 0
  uint256 y = 2; // slot 1
  uint256 z = 3; // slot 2
}
```

Do mỗi biến `x`, `y` và `z` đều có kích thước là 32 byte nên chúng được lưu trong từng slot riêng biệt. 

Trong trường hợp kích thước của các biến là nhỏ và vừa đủ một slot, chúng sẽ được đặt cạnh nhau. Ví dụ:

```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

// contract address: 0xeBa088B4182EC4261FA4fd2526F58995Dc1Ec117

contract StorageLayout {
    uint16 x = 1;
    uint16 y = 2;
    uint16 z = 3;
}
```

Khi dùng hàm `web3.eth.getStorageAt(contractAddress, slotPosition)` của thư viện web3.js để truy vấn giá trị được lưu ở slot 0, ta thu được giá trị sau:

```sol
slot[0] = 0x0000000000000000000000000000000000000000000000000000000300020001
```

Có thể thấy, ba biến `x`, `y` và `z` được đặt cạnh nhau. Ngoài ra, giá trị lưu ở slot 0 cũng được ABI-encode @abi-specification bằng cách đệm thêm các số 0.

Trong trường hợp các biến không thể lưu vừa trong một slot, chúng sẽ được lưu vào nhiều slot. Ví dụ:

```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

contract StorageLayout {
    uint16 x = 1;
    uint256 y = 2;
    uint16 z = 3;
}
```

Giá trị của các biến lưu trong các slot là:

```sol
slot[0] = 0x0000000000000000000000000000000000000000000000000000000000000001
slot[1] = 0x0000000000000000000000000000000000000000000000000000000000000002
slot[2] = 0x0000000000000000000000000000000000000000000000000000000000000003
```

## Mô tả

Các biến cục bộ có vị trí dữ liệu (data location) là `storage` bên trong hàm nếu không được khởi tạo có thể trỏ đến các biến trạng thái có vị trí dữ liệu là `storage` trong smart contract. Điều này có thể dẫn đến việc giá trị của các biến trạng thái bị sửa đổi thông qua các biến cục bộ. 

Xét smart contract sau:

```sol
// A Locked Name Registrar
contract NameRegistrar {

  bool public unlocked = false;  // registrar locked, no name updates
  
  struct NameRecord { // map hashes to addresses
    bytes32 name;
    address mappedAddress;
  }
  
  mapping(address => NameRecord) public registeredNameRecord; // records who registered names
  mapping(bytes32 => address) public resolve; // resolves hashes to addresses
  
  function register(bytes32 _name, address _mappedAddress) public {
    // set up the new NameRecord
    NameRecord newRecord;
    newRecord.name = _name;
    newRecord.mappedAddress = _mappedAddress;
    
    resolve[_name] = _mappedAddress;
    registeredNameRecord[msg.sender] = newRecord;
    
    require(unlocked); // only allow registrations if contract is unlocked
  }
}
```

Smart contract này có duy nhất một hàm là `register`. Khi biến trạng thái `unlocked` có giá trị là `true`, smart contract cho phép người dùng đăng ký tên và địa chỉ tương ứng với tên đó vào mapping `registeredNameRecord`. Câu lệnh `require` ở cuối hàm giúp hoàn trả giao dịch nếu `unlocked` có giá trị là `false`.

Dựa trên cơ chế lưu các biến `storage` của Solidity thì slot 0 sẽ lưu biến `unlocked`, slot 1 lưu biến `registeredNameRecord` và slot 2 lưu biến `resolve` #footnote[Ta bỏ qua việc mapping không thực sự được lưu ở một slot mà thay vào đó là các phần tử của nó được lưu ở các slot không liền kề nhau.].

Như đã biết, vị trí dữ liệu mặc định cho các biến có kiểu tham chiếu chẳng hạn như struct, mảng hoặc mapping là `storage`. Việc không khai báo vị trí dữ liệu cho biến `newRecord` bên trong hàm `register` làm cho nó có vị trí dữ liệu là `storage`. Do là một biến `storage` và không được khởi tạo, `newRecord` sẽ đóng vai trò là một con trỏ và trỏ đến slot 0. 

Cụ thể hơn, trường `name` và `mappedAddress` sẽ lần lượt trỏ đến biến `unlocked` và biến `registeredNameRecord`. Việc gán giá trị cho trường `name` khi đó cũng sẽ làm thay đổi giá trị của biến `unlocked`. Bằng cách chọn giá trị `_name` sao cho có bit cuối là 1, kẻ tấn công có thể gọi thực thi hàm `register` để thay đổi biến `unlocked` thành `true`.

## Cách khắc phục

Kiểm tra xem biến cục bộ thuộc kiểu tham chiếu có nhất thiết phải là `storage` hay không (thường là không vì điều này làm tăng chi phí thực hiện smart contract do việc ghi vào biến `storage` tiêu thụ rất nhiều gas). Nếu cần thiết thì nên khai báo vị trí dữ liệu tường minh là `storage`. Nếu không thì nên sử dụng vị trí dữ liệu là `memory`.

Kể từ phiên bản 0.5.0, vấn đề này đã được giải quyết do các biến `storage` chưa được khởi tạo sẽ không được biên dịch.


