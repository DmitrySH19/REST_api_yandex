PRAGMA journal_mode = MEMORY;
PRAGMA synchronous = OFF;
PRAGMA foreign_keys = OFF;
PRAGMA ignore_check_constraints = OFF;
PRAGMA auto_vacuum = NONE;
PRAGMA secure_delete = OFF;
BEGIN TRANSACTION;


CREATE TABLE `couriers` (
`id` INTEGER NOT NULL,
`courier_type` TEXT NOT NULL,
PRIMARY KEY (`id`)
);

CREATE TABLE `regions` (
`id` INTEGER NOT NULL,
`courier_id` INTEGER NOT NULL,
`region` INTEGER NOT NULL,
PRIMARY KEY (`id`),
FOREIGN KEY (`courier_id`) REFERENCES `couriers` (`id`)
);

CREATE TABLE `working_hours` (
`id` INTEGER NOT NULL,
`courier_id` INTEGER NOT NULL,
`start_hours`  TEXT NOT NULL,
`end_hours` TEXT NOT NULL,
PRIMARY KEY (`id`),
FOREIGN KEY (`courier_id`) REFERENCES `couriers` (`id`)
);

CREATE TABLE `orders` (
`order_id` INTEGER NOT NULL,
`weight` float(10, 2) NOT NULL,
`region` INTEGER NOT NULL,
PRIMARY KEY (`order_id`)
);

CREATE TABLE `delivery_hours` (
`id` INTEGER NOT NULL,
`order_id` INTEGER NOT NULL,
`start_hours` TEXT NOT NULL,
`end_hours` TEXT NOT NULL,
PRIMARY KEY (`id`),
FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
);

CREATE TABLE `complete_order_id` (
`order_id` INTEGER NOT NULL,
`courier_id` INTEGER DEFAULT -1 NOT NULL,
`assign_time` TEXT  NULL,
`complete_time` TEXT NULL,
PRIMARY KEY (`order_id`)
);



COMMIT;
PRAGMA ignore_check_constraints = ON;
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;