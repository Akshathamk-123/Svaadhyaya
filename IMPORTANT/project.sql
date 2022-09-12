-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 05, 2020 at 09:14 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project`
--

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `uid` int(11) DEFAULT NULL,
  `eid` int(11) DEFAULT NULL,
  `person1` varchar(255) DEFAULT NULL,
  `person2` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`uid`, `eid`, `person1`, `person2`) VALUES
(1, 1, 'Epsilon Gamma', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `pid` int(11) DEFAULT NULL,
  `contact1` decimal(10,0) DEFAULT NULL,
  `contact2` decimal(10,0) DEFAULT NULL,
  `contact3` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contact`
--

INSERT INTO `contact` (`pid`, `contact1`, `contact2`, `contact3`) VALUES
(1, '9924161231', '1231231221', '12312434');

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `eid` int(11) NOT NULL,
  `etype` varchar(255) NOT NULL,
  `edate` date NOT NULL,
  `etier` int(11) NOT NULL,
  `ecost` int(11) NOT NULL,
  `evenue` varchar(255) NOT NULL,
  `emax_people` int(11) NOT NULL,
  `especial` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `event`
--

INSERT INTO `event` (`eid`, `etype`, `edate`, `etier`, `ecost`, `evenue`, `emax_people`, `especial`) VALUES
(1, 'Birthday', '2020-06-27', 3, 35000, 'Sunrays Hall, Santacruz (W), Mumbai', 34, 'Theme of decoration should be blue.');

-- --------------------------------------------------------

--
-- Table structure for table `has`
--

CREATE TABLE `has` (
  `uid` int(11) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `has`
--

INSERT INTO `has` (`uid`, `pid`) VALUES
(1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `personal`
--

CREATE TABLE `personal` (
  `pid` int(11) NOT NULL,
  `fname` varchar(255) NOT NULL,
  `mname` varchar(255) NOT NULL,
  `lname` varchar(255) NOT NULL,
  `dob` date NOT NULL,
  `gender` varchar(20) NOT NULL,
  `address` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `personal`
--

INSERT INTO `personal` (`pid`, `fname`, `mname`, `lname`, `dob`, `gender`, `address`) VALUES
(1, 'Alpha', 'Beta', 'Gamma', '2020-06-01', 'Male', 'Mumbai, Maharashtra, India');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `uid` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `last_login` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`uid`, `username`, `email`, `password`, `last_login`) VALUES
(1, 'ABC', 'abc@xyz.com', 'e99a18c428cb38d5f260853678922e03', '2020-06-05 18:12:45'),
(2, 'XYZ', 'xyz@abc.com', '613d3b9c91e9445abaeca02f2342e5a6', '2020-06-05 13:53:52');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD KEY `books_ibfk_1` (`uid`),
  ADD KEY `books_ibfk_2` (`eid`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD KEY `contact_ibfk_1` (`pid`);

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`eid`);

--
-- Indexes for table `has`
--
ALTER TABLE `has`
  ADD KEY `has_ibfk_1` (`uid`),
  ADD KEY `has_ibfk_2` (`pid`);

--
-- Indexes for table `personal`
--
ALTER TABLE `personal`
  ADD PRIMARY KEY (`pid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`uid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `event`
--
ALTER TABLE `event`
  MODIFY `eid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `personal`
--
ALTER TABLE `personal`
  MODIFY `pid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `books`
--
ALTER TABLE `books`
  ADD CONSTRAINT `books_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `books_ibfk_2` FOREIGN KEY (`eid`) REFERENCES `event` (`eid`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `contact`
--
ALTER TABLE `contact`
  ADD CONSTRAINT `contact_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `personal` (`pid`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `has`
--
ALTER TABLE `has`
  ADD CONSTRAINT `has_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `has_ibfk_2` FOREIGN KEY (`pid`) REFERENCES `personal` (`pid`) ON DELETE CASCADE ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;