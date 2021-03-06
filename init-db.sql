-- phpMyAdmin SQL Dump
-- version 4.5.3.1
-- http://www.phpmyadmin.net
--
-- 主機: localhost
-- 產生時間： 2016 年 01 月 23 日 10:42
-- 伺服器版本: 10.1.10-MariaDB-log
-- PHP 版本： 7.0.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `pda-score`
--

-- --------------------------------------------------------

--
-- 資料表結構 `Admins`
--

CREATE TABLE `Admins` (
  `FBID` varchar(20) NOT NULL,
  `AdminName` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 資料表結構 `Player`
--

CREATE TABLE `Player` (
  `PlayerID` int(4) NOT NULL,
  `TeamID` int(11) NOT NULL,
  `FBID` varchar(20) NOT NULL,
  `CardName` varchar(50) NOT NULL,
  `FBName` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 資料表結構 `Score`
--

CREATE TABLE `Score` (
  `ScoreID` int(11) NOT NULL,
  `ScoreDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ScoreUploaderID` varchar(20) NOT NULL,
  `PlayerID` int(11) NOT NULL,
  `SongID` int(11) NOT NULL,
  `ImageHash` char(40) NOT NULL,
  `ImageExt` varchar(10) NOT NULL,
  `Rate` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 資料表結構 `Songs`
--

CREATE TABLE `Songs` (
  `SongID` int(11) NOT NULL,
  `SongName` varchar(50) NOT NULL,
  `SongLevel` varchar(10) NOT NULL,
  `SongStars` float NOT NULL,
  `isSpecSong` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 已匯出資料表的索引
--

--
-- 資料表索引 `Admins`
--
ALTER TABLE `Admins`
  ADD PRIMARY KEY (`FBID`);

--
-- 資料表索引 `Player`
--
ALTER TABLE `Player`
  ADD PRIMARY KEY (`PlayerID`),
  ADD UNIQUE KEY `FBID` (`FBID`),
  ADD KEY `TeamID` (`TeamID`);

--
-- 資料表索引 `Score`
--
ALTER TABLE `Score`
  ADD PRIMARY KEY (`ScoreID`),
  ADD KEY `PlayerID` (`PlayerID`),
  ADD KEY `SongID` (`SongID`);

--
-- 資料表索引 `Songs`
--
ALTER TABLE `Songs`
  ADD PRIMARY KEY (`SongID`);

--
-- 在匯出的資料表使用 AUTO_INCREMENT
--

--
-- 使用資料表 AUTO_INCREMENT `Player`
--
ALTER TABLE `Player`
  MODIFY `PlayerID` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;
--
-- 使用資料表 AUTO_INCREMENT `Score`
--
ALTER TABLE `Score`
  MODIFY `ScoreID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- 使用資料表 AUTO_INCREMENT `Songs`
--
ALTER TABLE `Songs`
  MODIFY `SongID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
--
-- 已匯出資料表的限制(Constraint)
--

--
-- 資料表的 Constraints `Score`
--
ALTER TABLE `Score`
  ADD CONSTRAINT `Score_ibfk_1` FOREIGN KEY (`SongID`) REFERENCES `Songs` (`SongID`),
  ADD CONSTRAINT `Score_ibfk_2` FOREIGN KEY (`PlayerID`) REFERENCES `Player` (`PlayerID`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
