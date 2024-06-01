# Incorrect Inheritance Order

## Đa kế thừa trong Solidity

Solidity hỗ trợ đa kế thừa nên nếu một smart contract kế thừa nhiều smart contract thì có thể dẫn đến vấn đề kim cương (Diamon Problem): nếu có hai hoặc nhiều smart contract cơ sở cùng định nghĩa một hàm, hàm nào sẽ được gọi sử dụng trong smart contract dẫn xuất? 

Giả sử có smart contract `A` như sau @on-crowdsales-and-multiple-inheritance:

```sol
contract A {
  
  function f() {
    somethingA();
  }
  
}
```

Smart contract `B` và `C` kế thừa `A`. Hai smart contract này đều ghi đè hàm `f`:

```sol
contract B is A {

  function f() {
    somethingB();
    super.f();
  }
  
}

contract C is A {
  
  function f() {
    somethingC();
    super.f();
  }
  
}
```

Cuối cùng, smart contract `D` kế thừa `B` và `C`:

```sol
contract D is B, C {
  
  function f() { 
    somethingD();
    super.f();
  }
  
}
```

Câu hỏi đặt ra là: khi `D` gọi hàm `f`, hàm `f` trong `B` hay hàm `f` trong `C` sẽ được gọi?

Solidity xử lý vấn đề này bằng cách sử dụng tuyến tính hóa siêu lớp C3 đảo ngược @multiple-inheritance-and-linearization để thiết lập độ ưu tiên cho các smart contract.

Nói một cách đơn giản, khi một hàm được sử dụng trong smart contract dẫn xuất mà có nhiều định nghĩa trong các smart contract cơ sở, Solidity sẽ tìm kiếm định nghĩa của hàm trong các smart contract cơ sở từ phải sang trái (từ cụ thể đến tổng quát) và sẽ sử dụng định nghĩa đầu tiên mà nó tìm thấy.

Trong ví dụ trên, Solidity sẽ gọi hàm theo thứ tự sau:

```sol
somethingD(); 
somethingC(); 
somethingB(); 
somethingA();
```

Hàm `f` của smart contract `C` sẽ được ưu tiên hơn hàm `f` của smart contract `B` do `C` được khai báo sau (cụ thể hơn). Ngoài ra, mặc dù smart contract `C` không kế thừa smart contract `B`, hàm `f` của `B` vẫn được gọi thông qua `super.call()` trong hàm `f` của `C`.

## Mô tả

Do mỗi smart contract cơ sở đều có độ ưu tiên, việc không quan tâm thứ tự kế thừa có thể dẫn đến những hành vi không mong muốn của smart contract.

## Cách khắc phục

Khi sử dụng đa kế thừa, cần cẩn thận trong việc sắp xếp thứ tự kế thừa của các smart contract cơ sở mà có các hàm giống nhau. Nguyên tắc chung là kế thừa các smart contract từ tổng quát đến cụ thể.
