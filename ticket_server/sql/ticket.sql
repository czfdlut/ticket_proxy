/*
 Navicat Premium Data Transfer

 Source Server         : sssss
 Source Server Type    : MySQL
 Source Server Version : 50643
 Source Host           : localhost:3306
 Source Schema         : ticket_proxy

 Target Server Type    : MySQL
 Target Server Version : 50643
 File Encoding         : 65001

 Date: 04/03/2019 10:43:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ------------------------------------
-- Table structure for ticket's infoes
-- ------------------------------------
DROP TABLE IF EXISTS `ticket`;
CREATE TABLE `ticket`  (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `train_id` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '车次编号',
  `train_name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '车次名称',
  `start_station_id` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '始发车站编号',
  `start_station_name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '始发车站名称',
  `arrival_station_id` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '到达车站编号',
  `arrival_station_name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '到达车站名称',
  `via_station` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '途经站信息',
  `start_datetime` datetime(0) NULL COMMENT '始发时间',
  `arrival_datetime` datetime(0) NULL COMMENT '到达时间',
  `seat_type` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '座位席别',
  `ticket_price` float(11, 0) NOT NULL COMMENT '票价',
  `ticket_count` int(11) NOT NULL DEFAULT 0 COMMENT '余票数量',
  `status` int(11) NULL DEFAULT NULL COMMENT '售票状态',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 142 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
