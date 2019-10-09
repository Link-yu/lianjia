CREATE TABLE `ershoufang` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `area` varchar(255) DEFAULT NULL,
  `area_in` varchar(255) DEFAULT NULL,
  `elevator` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `price` int(11) NOT NULL,
  `room_maininfo` varchar(255) DEFAULT NULL,
  `room_subinfo` varchar(255) DEFAULT NULL,
  `room_type` varchar(255) DEFAULT NULL,
  `sale_time` varchar(255) DEFAULT NULL,
  `unit_price` int(11) DEFAULT NULL,
  `xiaoqu_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `chengjiao` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `area` varchar(255) DEFAULT NULL,
  `floor` varchar(255) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `room_info` varchar(255) DEFAULT NULL,
  `sale_price` int(11) NOT NULL,
  `sale_time` datetime DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  `xiaoqu_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `xiaoqu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `address` varchar(255) DEFAULT NULL,
  `building` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `cityCode` int(11) DEFAULT NULL,
  `company` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `number` varchar(255) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `property_company` varchar(255) DEFAULT NULL,
  `property_fee` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;