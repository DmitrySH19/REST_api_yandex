CREATE TABLE `couriers` (
  `id` int(10) NOT NULL,
  `courier_type` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `regions` (
  `courier_id` int(10) NOT NULL,
  `region` int(10) NOT NULL,
  `id` int(10) AUTO_INCREMENT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `table2_courires_rfjdc67qw_foreign` FOREIGN KEY (`courier_id`) REFERENCES `couriers` (`id`)
);

CREATE TABLE `working_hours` (
  `id` int(10)  AUTO_INCREMENT NOT NULL,
  `courier_id` int(10) NOT NULL,
  `start_hours`  varchar(10) NOT NULL,
  `end_hours` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `table3_courires_op8xjh4l0_foreign` FOREIGN KEY (`courier_id`) REFERENCES `couriers` (`id`)
);

CREATE TABLE `orders` (
  `order_id` int(10) NOT NULL,
  `weight` float(10, 2) NOT NULL,
  `region` int(10) NOT NULL,
  PRIMARY KEY (`order_id`)
);

CREATE TABLE `delivery_hours` (
  `id` int(10) AUTO_INCREMENT NOT NULL,
  `order_id` int(10) NOT NULL,
  `start_hours` varchar(6) NOT NULL,
  `end_hours` varchar(6) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `table5_orders_mfn33fi02_foreign` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
);

CREATE TABLE `complete_order_id` (
  `order_id` int(10) NOT NULL,
  `courier_id` int(10) DEFAULT -1 NOT NULL,
  `assign_time` varchar(30)  NULL,
  `complete_time` varchar(30) NULL,
  PRIMARY KEY (`order_id`)
);