# Ethereum

## Tổng quan

Ethereum là một chuỗi khối công khai mã nguồn mở. Thường được biết đến với đồng tiền điện tử của chính nó, Ether (ETH) và được dùng để chạy các hợp đồng thông minh đa mục đích (general-purpose smart contract).

## Ngôn Ngữ Lập Trình Hợp Đồng Thông Minh

Hợp đồng thông minh trong Ethereum thường được viết bằng Solidity – một ngôn ngữ lập trình miền chuyên biệt (DSL) được phát triển bởi Ethereum Network dựa trên 3 loại ngôn ngữ lập trình: C++, Python và JavaScript  @kim_2020_analysis. Solidity là ngôn ngữ hướng hợp đồng (contract-oriented) và có thể xem mỗi hợp đồng trong Solidity như là một lớp trong mô hình lập trình hướng đối tượng (object-oriented programming paradigm).

Mỗi hợp đồng trong Solidity có thể bao gồm những thành phần sau @kim_2020_analysis:
- Biến trạng thái: có thể xem như là các biến toàn cục ở trong một hợp đồng và chúng sẽ được lưu vĩnh viễn trong bộ nhớ của hợp đồng cũng như là của chuỗi khối.
- Hàm: có thể đọc và chỉnh sửa các biến trạng thái.
- Sự kiện: giúp hợp đồng gửi thông báo đến các ứng dụng bên ngoài về sự thay đổi trạng thái xảy ra ở trong hợp đồng.
- Bộ điều chỉnh (modifier): giúp đảm bảo một số điều kiện trước khi thực thi hàm.

Ngoài Solidity, hợp đồng thông minh trong Ethereum còn có thể được viết bằng các ngôn ngữ sau: Vyper, Yul, Yul+ và FE @smart-contract-languages.

## Máy Ảo Ethereum

Ethereum vận hành một máy ảo có tên là máy ảo Ethereum (Ethereum Virtual Machine - EVM), bao gồm một ngăn xếp để chứa các mã lệnh (opcode) và dữ liệu để thực thi các chỉ thị, một bộ nhớ byte-addressed (một byte sẽ có một địa chỉ độc nhất) và một không gian lưu trữ vĩnh viễn theo dạng khóa - giá trị (key - value) có kích thước 32 byte @kim_2020_analysis.

EVM hoạt động dựa trên một tài nguyên có tên là "gas". Mỗi mã lệnh sẽ tiêu hao một lượng gas nhất định. Các nút khởi tạo giao dịch mà có liên quan đến hợp đồng thông minh trong chuỗi khối sẽ gán cho giao dịch một giá gas. Thợ đào sẽ nhận được một lượng Ether từ nút khởi tạo giao dịch bằng với giá gas nhân với lượng gas cần để thực thi hợp đồng thông minh @kim_2020_analysis. Giá gas càng cao thì thợ đào sẽ càng ưu tiên thực thi giao dịch @atzei_2017_a.

Thợ đào sẽ thực thi hợp đồng thông minh đến khi nó kết thúc. Trong trường hợp xảy ra ngoại lệ, toàn bộ lượng gas còn lại sẽ được trả về cho nút khởi tạo giao dịch @atzei_2017_a.

Việc sử dụng gas giúp giảm thiểu các tấn công từ chối dịch vụ gây ra bởi các giao dịch có chứa các tính toán tốn thời gian @atzei_2017_a.

## Bytecode

EVM sẽ biên dịch các ngôn ngữ lập trình bậc cao chẳng hạn như Solidity thành bytecode #footnote[Là dạng biểu diễn trung gian giữa mã nguồn bậc cao và mã máy bậc thấp.]. Bytecode có 255 mã lệnh #footnote[Tính đến thời điểm tháng 5 năm 2024 @evm-opcodes.] và biểu diễn các chỉ thị thực thi dưới dạng stack-based @kim_2020_analysis. Như vậy, về bản chất, một hợp đồng thông minh là một chuỗi các các chỉ thị mà sẽ được thực thi bởi EVM @wohrer_2018_smart.

EVM bytecode của một hợp đồng bao gồm hai thành phần là mã khởi tạo và mã thực thi @kim_2020_analysis. Mã khởi tạo (creation code) bao gồm dãy các chỉ thị của hàm tạo và chỉ được thực thi một lần duy nhất khi hợp đồng được tạo ra. Mã thực thi (runtime code) là mã sẽ được triển khai và lưu ở trên chuỗi khối. Nó có một địa chỉ định danh tài khoản 160-bit duy nhất @wohrer_2018_smart và một bộ nhớ riêng.

Khi một nút gọi hàm bằng cách gửi lên mạng lưới một giao dịch có chứa dữ liệu giao dịch (transaction data) #footnote[Dữ liệu giao dịch của giao dịch gọi hàm thường có những thông tin sau: địa chỉ của hợp đồng thông minh, nguyên mẫu hàm, giá trị của các đối số, giới hạn gas và giá gas.], EVM sẽ trỏ bộ đếm chương trình (program counter) đến hàm ở trong bytecode dựa vào 4 byte đầu tiên trong dữ liệu giao dịch @kim_2020_analysis. Cụ thể hơn, 4 byte này là giá trị băm của nguyên mẫu hàm. Trong trường hợp giao dịch không dùng để thực thi hợp đồng thông minh mà chỉ gửi Ether thì nguyên mẫu hàm là rỗng @atzei_2017_a.

## Các lỗ hổng

Bởi vì tính chất tự nhiên của chuỗi khối, các hợp đồng thông minh sau khi được triển khai lên chuỗi khối không thể được chỉnh sửa @kushwaha_2022_systematic. Do đó, cần phải xem xét các lỗ hổng có trong hợp đồng thông minh một cách cẩn thận trước khi triển khai lên chuỗi khối và đưa vào sử dụng.

Các lỗ hổng trong hợp đồng thông minh của Ethereum thường được phân loại dựa trên ba nguyên nhân chính @kushwaha_2022_systematic @atzei_2017_a:
- Ngôn ngữ lập trình của hợp đồng thông minh.
- Các tính năng của máy ảo Ethereum.
- Các thiết kế của chuỗi khối.

### Ngôn ngữ lập trình

#include "function-or-state-variable-default-visibility.typ"
#include "integer-overflow-underflow.typ"
#include "outdated-compiler-version.typ"
#include "floating-compiler-version.typ"
#include "unchecked-return-value.typ"
#include "access-control-management.typ"
#include "re-entrancy.typ"
#include "uninitialized-storage-pointer.typ"
#include "assert-and-require-violation.typ"
#include "use-of-deprecated-solidity-functions.typ"
#include "delegatecall-to-untrusted-callee.typ"
#include "denial-of-service-with-failed-call.typ"
#include "authorization-through-tx.origin.typ"
#include "signature-malleability.typ"
#include "incorrect-constructor-name.typ"
#include "shadowing-state-variables.typ"
#include "weak-sources-of-randomness-from-chain-attributes.typ"
#include "missing-protection-against-signature-replay-attacks.typ"
#include "lack-of-proper-signature-verification.typ"
#include "write-to-arbitrary-storage-location.typ"
#include "incorrect-inheritance-order.typ"
#include "insufficient-gas-griefing.typ"
#include "arbitrary-jump-with-function-type-variable.typ"
#include "denial-of-service-with-block-gas-limit.typ"
#include "typographical-error.typ"
#include "right-to-left-override-control-unicode.typ"
#include "unexpected-balance.typ"
#include "hash-collisons-with-multiple-variable-length-arguments.typ"
#include "frozen-ether.typ"
#include "call-to-the-unknown.typ"
// #include "dynamic-library.typ"
#include "hiding-malicious-code-with-external-contract.typ"
#include "double-constructor.typ"
#include "built-in-symbol-shadowing.typ"
#include "identity-verification.typ"

### Ethereum Virtual Machine

#include "immutable-bugs.typ"
#include "ether-lost-in-transfer.typ"
#include "stack-size-limit.typ"
#include "function-selector-clashing.typ"
#include "message-call-with-hardcoded-gas-amount.typ"
#include "short-address.typ"

### Blockchain

#include "transaction-ordering-dependency.typ"
#include "timestamp-dependency.typ"
#include "unencrypted-private-data-on-chain.typ"
#include "untrustworthy-data-feeds.typ"
