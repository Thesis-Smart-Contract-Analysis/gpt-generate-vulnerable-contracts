# Right-To-Left Override Control Character

## Mô tả

Kẻ xấu có thể sử dụng ký tự ghi đè phải sang trái (right-to-left override) có điểm mã (code point) là U+202E để thay đổi chiều hiển thị của các ký tự. 

Ký tự này thường được dùng để che giấu phần mở rộng thực sự của tập tin nhằm đánh lừa người dùng. Ví dụ, khi sử dụng nó trong chuỗi `my-text.'U+202E'cod.exe` thì giá trị được hiển thị sẽ là `my-text.exe.doc` @u202e.

Ở trong mã nguồn, ký tự U+202E có thể được sử dụng để thay đổi thứ tự của các đối số:

```sol
/*
 * @source: https://youtu.be/P_Mtd5Fc_3E
 * @author: Shahar Zini
 */
pragma solidity ^0.5.0;

contract GuessTheNumber {
  
  // ...
  
  function guess(uint n) payable public {
    require(msg.value == 1 ether);

    uint p = address(this).balance;
    checkAndTransferPrize(/*The prize‮/*rebmun desseug*/n , p/*‭
            /*The user who should benefit */,msg.sender);
  }
  
  // ...
}
```

Trong ví dụ trên, thoạt nhìn thì có vẻ như biến `p` là đối số đầu tiên còn biến `n` là đối số thứ hai của hàm `checkAndTransferPrize`. Tuy nhiên, do tác dụng của ký tự U+202E, thứ tự thực sự của hai đối số này đã bị đảo ngược

Thứ tự gốc của chúng là:

#figure(
  image("/ethereum/imgs/Right-To-Left-Override.png"),
  caption: [Sử dụng ký tự U+202E để thay đổi thứ tự hiển thị của các đối số],
)

Với U+202D là ký tự ghi đè trái sang phải, được dùng để khôi phục chiều hiển thị.

## Cách khắc phục

Cần loại bỏ ký tự ghi đè phải sang trái trong mã nguồn.
