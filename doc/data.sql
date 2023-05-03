-- 创建商城订单表
CREATE TABLE mall_order (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_number VARCHAR(20) NOT NULL,
    order_status ENUM('待付款', '待发货', '待收货', '已完成', '已取消') NOT NULL,
    payment_amount DECIMAL(10, 2) NOT NULL,
    payment_method ENUM('支付宝', '微信支付', '银行卡') NOT NULL,
    create_time DATETIME NOT NULL,
    update_time DATETIME NOT NULL
);

-- 插入示例数据
INSERT INTO mall_order (
    user_id, order_number, order_status, payment_amount, payment_method, create_time, update_time
) VALUES (
    1, '20230502000001', '待付款', 100.00, '支付宝', '2023-05-02 10:00:00', '2023-05-02 10:00:00'
);

INSERT INTO mall_order (
    user_id, order_number, order_status, payment_amount, payment_method, create_time, update_time
) VALUES (
    2, '20230502000002', '待发货', 250.00, '微信支付', '2023-05-02 10:05:00', '2023-05-02 10:10:00'
);

INSERT INTO mall_order (
    user_id, order_number, order_status, payment_amount, payment_method, create_time, update_time
) VALUES (
    1, '20230502000003', '待收货', 120.00, '银行卡', '2023-05-02 10:15:00', '2023-05-02 10:20:00'
);

INSERT INTO mall_order (
    user_id, order_number, order_status, payment_amount, payment_method, create_time, update_time
) VALUES (
    3, '20230502000004', '已完成', 80.00, '支付宝', '2023-05-02 10:30:00', '2023-05-02 10:45:00'
);
