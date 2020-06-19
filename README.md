# Hassio component evn_mientrung

Custom component này dùng để tạo sensor cho chỉ số đồng hồ điện theo tháng của EVN Miền trung
![Entity](https://i.imgur.com/DBCmbiH.png)

## Features
* Thông tin người đăng ký
* Địa chỉ
* Chỉ số công tơ chưa thanh toán(tính từ thời điểm thanh toán tiền đến hiện tại)
* Chỉ số công tơ tổng tháng trước
* Thời điểm chốt số điện tháng trước
* Chỉ số công tơ hiện tại
* Thời điểm đo chỉ số cuối cùng
* Mã số đồng hồ điện
* Model đồng hồ điện
* Trạm điện quản lý


## Install

Để cài đặt tính năng này, vui lòng clone code về và đặt thư mục custom_component vào trong thư mục /config mặc định của hass


## Setup

```yaml
# configuration.yaml

evn_mientrung:
  evn_id: PP03000391234
  scan_interval_minute: 15
```

Configuration variables:
- **evn_id** (*Required*): Mã số người dùng trên hóa đơn tiền điện.
- **scan_interval_minute** (*Optional*): Thời gian lấy chỉ số định kỳ(mặc định 15). Mỗi ngày chỉ số chỉ cập nhật vài lần nên vui lòng đặt thời gian lớn hơn 15 phút để tránh quá tải cho máy chủ cung cấp 
