-- phpMyAdmin SQL Dump
-- version 3.3.8.1
-- http://www.phpmyadmin.net
--
-- 主机: w.rdc.sae.sina.com.cn:3307
-- 生成日期: 2012 年 10 月 31 日 15:39
-- 服务器版本: 5.5.23
-- PHP 版本: 5.2.9

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `app_pylabs`
--

-- --------------------------------------------------------

--
-- 表的结构 `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- 转存表中的数据 `auth_group`
--


-- --------------------------------------------------------

--
-- 表的结构 `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_425ae3c4` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- 转存表中的数据 `auth_group_permissions`
--


-- --------------------------------------------------------

--
-- 表的结构 `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=28 ;

--
-- 转存表中的数据 `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add permission', 1, 'add_permission'),
(2, 'Can change permission', 1, 'change_permission'),
(3, 'Can delete permission', 1, 'delete_permission'),
(4, 'Can add group', 2, 'add_group'),
(5, 'Can change group', 2, 'change_group'),
(6, 'Can delete group', 2, 'delete_group'),
(7, 'Can add user', 3, 'add_user'),
(8, 'Can change user', 3, 'change_user'),
(9, 'Can delete user', 3, 'delete_user'),
(10, 'Can add content type', 4, 'add_contenttype'),
(11, 'Can change content type', 4, 'change_contenttype'),
(12, 'Can delete content type', 4, 'delete_contenttype'),
(13, 'Can add session', 5, 'add_session'),
(14, 'Can change session', 5, 'change_session'),
(15, 'Can delete session', 5, 'delete_session'),
(16, 'Can add site', 6, 'add_site'),
(17, 'Can change site', 6, 'change_site'),
(18, 'Can delete site', 6, 'delete_site'),
(19, 'Can add poll', 7, 'add_poll'),
(20, 'Can change poll', 7, 'change_poll'),
(21, 'Can delete poll', 7, 'delete_poll'),
(22, 'Can add choice', 8, 'add_choice'),
(23, 'Can change choice', 8, 'change_choice'),
(24, 'Can delete choice', 8, 'delete_choice'),
(25, 'Can add log entry', 9, 'add_logentry'),
(26, 'Can change log entry', 9, 'change_logentry'),
(27, 'Can delete log entry', 9, 'delete_logentry');

-- --------------------------------------------------------

--
-- 表的结构 `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- 转存表中的数据 `auth_user`
--

INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`) VALUES
(1, 'root', '', '', 'sae@sina.com', 'pbkdf2_sha256$10000$24Z4xOfUCbbs$8W7HXan50vIdPiECMXk8E63mp5KkX7cxaDUx3SO8q4Y=', 1, 1, 1, '2012-10-31 07:25:52', '2012-10-30 06:06:28');

-- --------------------------------------------------------

--
-- 表的结构 `auth_user_groups`
--

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_403f60f` (`user_id`),
  KEY `auth_user_groups_425ae3c4` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- 转存表中的数据 `auth_user_groups`
--


-- --------------------------------------------------------

--
-- 表的结构 `auth_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_403f60f` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- 转存表中的数据 `auth_user_user_permissions`
--


-- --------------------------------------------------------

--
-- 表的结构 `django_admin_log`
--

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_403f60f` (`user_id`),
  KEY `django_admin_log_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- 转存表中的数据 `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `user_id`, `content_type_id`, `object_id`, `object_repr`, `action_flag`, `change_message`) VALUES
(1, '2012-10-30 06:18:15', 1, 7, '1', 'Poll object', 1, ''),
(2, '2012-10-30 07:08:39', 1, 7, '1', 'Poll object', 3, ''),
(3, '2012-10-30 07:10:39', 1, 7, '2', 'Poll object', 1, ''),
(4, '2012-10-30 07:13:02', 1, 7, '3', 'Poll object', 1, ''),
(5, '2012-10-30 08:00:07', 1, 7, '3', 'Poll object', 2, 'Changed question.'),
(6, '2012-10-31 02:10:18', 1, 7, '4', 'Poll object', 1, '');

-- --------------------------------------------------------

--
-- 表的结构 `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10 ;

--
-- 转存表中的数据 `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES
(1, 'permission', 'auth', 'permission'),
(2, 'group', 'auth', 'group'),
(3, 'user', 'auth', 'user'),
(4, 'content type', 'contenttypes', 'contenttype'),
(5, 'session', 'sessions', 'session'),
(6, 'site', 'sites', 'site'),
(7, 'poll', 'polls', 'poll'),
(8, 'choice', 'polls', 'choice'),
(9, 'log entry', 'admin', 'logentry');

-- --------------------------------------------------------

--
-- 表的结构 `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_3da3d3d8` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('008ad7e03862e1629e6daae522b2c966', 'NjBkMmM1YjZiNzc3Zjk4ZjM4ZDg2NjlmNWQzMTM4ZjdiMWNmMWY4MDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n', '2012-11-13 06:16:18'),
('06d2ada6d5dc0420b6c7a3065f5b1c75', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:58:46'),
('b3c87ecbc2782d39f2d566fd13d49f9f', 'NjBkMmM1YjZiNzc3Zjk4ZjM4ZDg2NjlmNWQzMTM4ZjdiMWNmMWY4MDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n', '2012-11-13 07:56:32'),
('410b45fe33d441e1967a8bea227a720f', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:58:48'),
('314bda20732bf0bb56151571c819db61', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:58:49'),
('454f6334a73fea0d5788b3bad6d58b8a', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:58:50'),
('5b2f4a831f481b5fa26474a0f3e25ac5', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:58:51'),
('87aff8f07792b206b99ebe92821700e8', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:58:51'),
('912a49c543d76ba48650386b2c17f7b5', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:58:52'),
('752957b0702ce16986ffadd7332caef2', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:58:53'),
('aa9fb069f2800565f7e0998ab4e380df', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:58:54'),
('b64e0a0614bd6fd61b6b777d6e773e98', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:58:54'),
('5a1f7dd0a06f1a8bc211086f7e301920', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:59:33'),
('ac3ad8cfe330726bc8e8e2d3def571cb', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:59:33'),
('4c313aac8989ddd596999673f1a43e6f', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:59:34'),
('118233d5be7f4063fcc98cad822b52af', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:59:35'),
('e6e018f3fc08914fab634fff165563b6', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:59:35'),
('6b5f51469ffa3156dc1829b2bf3fb49b', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:59:36'),
('e429be9a654e6aeabe767b36c8528de5', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:59:36'),
('0719c46deecbdacdcd7ba9859c648f3d', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:59:36'),
('b9563822341436355e372e75286677dc', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:59:37'),
('ee3837677cfe9bcdf7d3520f06717c53', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:59:37'),
('c79e79a0a7c2ddd91eaec21120044fa4', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:59:37'),
('16e0a5777a3ee20e3c11ad02760569b1', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 01:59:37'),
('4ebbd66c3f3a5e85ac3188524fdc555c', 'ZWE2OWYzNmYwNjc2MjY0OGVmNjJjOTc4YzUwNjk0MTlmZGY5NWZjMDqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n', '2012-11-14 02:00:07'),
('3a45a6128f11119ef31417ea806cb075', 'NjBkMmM1YjZiNzc3Zjk4ZjM4ZDg2NjlmNWQzMTM4ZjdiMWNmMWY4MDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n', '2012-11-14 07:25:52'),
('4268b618f958a05f61931dd6eab3f098', 'gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjhhNjFmYjExYjZmNjY3ZmI0NWI0NjU4Y2E0\nZGE3YzJi\n', '2012-11-14 15:38:47'),
('4d50416d7e4b8f7f20e242182ae8fdb8', 'gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjhhNjFmYjExYjZmNjY3ZmI0NWI0NjU4Y2E0\nZGE3YzJi\n', '2012-11-14 15:38:49'),
('39a905326781e4eff970e7ae342407f8', 'gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLjhhNjFmYjExYjZmNjY3ZmI0NWI0NjU4Y2E0\nZGE3YzJi\n', '2012-11-14 15:38:52');

-- --------------------------------------------------------

--
-- 表的结构 `django_site`
--

CREATE TABLE IF NOT EXISTS `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- 转存表中的数据 `django_site`
--

INSERT INTO `django_site` (`id`, `domain`, `name`) VALUES
(1, 'example.com', 'example.com');

-- --------------------------------------------------------

--
-- 表的结构 `polls_choice`
--

CREATE TABLE IF NOT EXISTS `polls_choice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `poll_id` int(11) NOT NULL,
  `choice` varchar(200) NOT NULL,
  `votes` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `polls_choice_763e883` (`poll_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

--
-- 转存表中的数据 `polls_choice`
--

INSERT INTO `polls_choice` (`id`, `poll_id`, `choice`, `votes`) VALUES
(1, 2, 'Jaime', 1),
(2, 2, 'Tryion', 3),
(3, 2, 'Ned Stark', 3),
(4, 3, 'yes', 3),
(5, 3, 'no', 4),
(6, 4, 'Stark', 2),
(7, 4, 'Targaren', 1),
(8, 4, 'Lannister', 1);

-- --------------------------------------------------------

--
-- 表的结构 `polls_poll`
--

CREATE TABLE IF NOT EXISTS `polls_poll` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question` varchar(200) NOT NULL,
  `pub_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- 转存表中的数据 `polls_poll`
--

INSERT INTO `polls_poll` (`id`, `question`, `pub_date`) VALUES
(2, 'Which character do you like best?', '2012-10-30 20:10:26'),
(3, 'Do you think the queue Cercei is totally a nuts?', '2012-10-30 20:12:58'),
(4, 'Which house do you think will win the Iron Throne in the end?', '2012-10-31 02:10:44');
