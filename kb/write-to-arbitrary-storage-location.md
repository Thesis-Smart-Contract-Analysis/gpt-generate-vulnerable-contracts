# Write to Arbitrary Storage Location

## Mô tả

Smart contract cần phải đảm bảo rằng các vị trí lưu trữ dữ liệu nhạy cảm chỉ có thể được truy cập và chỉnh sửa bởi địa chỉ của người dùng hoặc smart contract mà đã được phân quyền. Nếu một kẻ tấn công có khả năng thay đổi giá trị của bất kỳ vị trí lưu trữ nào thì có thể vượt qua xác thực và thay đổi giá trị của các biến trạng thái.

Ví dụ @solidity-array-overflow:

```sol
pragma solidity ^0.4.17; 

contract ArrayLengthManipulation{
  
  uint256 target = 10;
  uint256[] array = [9,8];

  function modifyArray (uint256 _index, uint256 _value){
    array[_index] = _value;
  }

  function popLength() public{
    // cause overflow
    array.length--;
  }

  function getLength() constant returns(uint256){
    return array.length;
  }

}
```

Mục tiêu của kẻ tấn công là thay đổi giá trị của biến `target`.

Trước tiên, kẻ tấn công sẽ gọi hàm `popLength` 3 lần để giảm kích thước #footnote[Trước phiên bản 0.6.0, kích thước của mảng động có thể được điều chỉnh thông qua thuộc tính `length` của mảng] của mảng `array` xuống $-1 = 2^{256} - 1$ (giá trị dạng thập lục phân là `0xff..ff`). Lúc đó, kích thước của mảng bằng với kích thước của mảng các slot (tính luôn cả slot lưu kích thước mảng). Điều này khiến cho chỉ số của các phần tử trong mảng cũng là chỉ số của các slot (bố cục lưu trữ theo các slot được đề cập trong phần @storage-layout[]).

Do `array` được lưu ở slot 1, chỉ số slot lưu dữ liệu của phần tử đầu tiên là giá trị băm Keccak-256 của chuỗi `0x0000000000000000000000000000000000000000000000000000000000000001`:

```
0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6
```

Các phần tử của mảng nằm ở slot `0xff..ff` trở đi sẽ bị chồng chéo. Ví dụ, chỉ số `0xff..ff` sẽ tương ứng với chỉ số $2^{256} mod 2^{256} = 0$, chỉ số `0xff..ff + 1` sẽ tương ứng với chỉ số $2^{256} + 1 mod 2^{256} = 1$, ...

Minh họa: 

#figure(
  image("imgs/Write to arbitrary storage location.png"),
  caption: [Chồng chéo không gian lưu trữ]
)

Trong hình minh họa trên, hai slot cuối cùng sẽ bị chồng chéo với slot 0 và slot 1. Kẻ tấn công sẽ cần phải tìm chỉ số mảng tương ứng với slot cần thay đổi giá trị. Cụ thể, chỉ số mảng tương ứng với slot 0 sẽ là:

```
0xff..ff - 0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6 + 0
```

Công thức tổng quát:

$
i = 2^{256} - i_a + i_b
$

Với:
- $i$ là chỉ số mảng cần tìm.
- $i_a$ là chỉ số slot của phần tử đầu tiên trong mảng.
- $i_b$ là chỉ số slot của biến cần thay đổi giá trị.

Sau khi có được chỉ số mảng thì kẻ tấn công sẽ gọi hàm `modifyArray` để thay đổi giá trị của biến `target` thông qua mảng `array`.

## Cách khắc phục

Cần phải đảm bảo rằng việc thay đổi giá trị của một cấu trúc dữ liệu không làm thay đổi dữ liệu của các cấu trúc dữ liệu khác.

Ngoài ra, đối với ví dụ ở trên, kể từ phiên bản 0.6.0, thuộc tính `length` của mảng động chỉ có thể đọc chứ không thể ghi.
