-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 03, 2026 at 10:50 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sistem_material`
--

-- --------------------------------------------------------

--
-- Table structure for table `keuangan`
--

CREATE TABLE `keuangan` (
  `id` int(11) NOT NULL,
  `tipe` varchar(20) DEFAULT NULL,
  `material_id` int(11) DEFAULT NULL,
  `cabang` varchar(25) DEFAULT NULL,
  `jenis_truck` varchar(25) DEFAULT NULL,
  `kubikasi` float DEFAULT NULL,
  `jumlah` bigint(20) DEFAULT NULL,
  `keterangan` varchar(100) DEFAULT NULL,
  `metode` varchar(15) DEFAULT NULL,
  `tanggal` date DEFAULT NULL,
  `status` varchar(25) DEFAULT 'Draft'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `keuangan`
--

INSERT INTO `keuangan` (`id`, `tipe`, `material_id`, `cabang`, `jenis_truck`, `kubikasi`, `jumlah`, `keterangan`, `metode`, `tanggal`, `status`) VALUES
(1, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 4.5, 1100000, NULL, 'Cash', '2026-03-12', 'Final'),
(2, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-03-12', 'Final'),
(3, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 200, 48889000, NULL, 'Cash', '2026-03-12', 'Final'),
(4, 'pengeluaran', NULL, 'Tuban', NULL, NULL, 200000, 'solar 10 liter', NULL, '2026-03-12', 'Final'),
(5, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-03-12', 'Final'),
(6, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-03-12', 'Final'),
(7, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-03-12', 'Final'),
(8, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-03-12', 'Final'),
(9, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-03-12', 'Final'),
(10, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-03-12', 'Final'),
(11, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-03-12', 'Final'),
(12, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-03-12', 'Final'),
(13, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 123, 30067000, NULL, 'Cash', '2026-03-13', 'Draft'),
(14, 'pemasukan', 1, 'Mahendradatta', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-03-12', 'Final'),
(15, 'pemasukan', 1, 'Mahendradatta', 'Engkel', 2.5, 611000, NULL, 'Cash', '2026-03-12', 'Final'),
(16, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-03-13', 'Draft'),
(17, 'pemasukan', 3, 'Tuban', 'Dump Truck Besar', 300, 60000000, NULL, 'Transfer', '2026-03-12', 'Final'),
(18, 'pemasukan', 3, 'Mahendradatta', 'Dump Truck Besar', 300, 60000000, NULL, 'Cash', '2026-03-12', 'Final'),
(19, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-04-11', 'Final'),
(20, 'pemasukan', 1, 'Tuban', 'Dump Truck Kecil', 4.5, 1100000, NULL, 'Cash', '2026-04-14', 'Draft'),
(21, 'pengeluaran', NULL, 'Tuban', NULL, NULL, 200000, 'sollar 20 liter', NULL, '2026-04-14', 'Draft'),
(22, 'pemasukan', 1, 'Mahendradatta', 'Dump Truck Besar', 6, 1467000, NULL, 'Transfer', '2026-04-17', 'Final'),
(23, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-04-20', 'Final'),
(24, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 4.5, 1100000, NULL, 'Cash', '2026-04-20', 'Final'),
(25, 'pemasukan', 1, 'Tuban', 'Engkel', 2.5, 611000, NULL, 'Transfer', '2026-04-20', 'Final'),
(26, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-04-20', 'Final'),
(27, 'pemasukan', 3, 'Tuban', 'Dump Truck Besar', 12, 2400000, NULL, 'Cash', '2026-04-20', 'Final'),
(28, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-04-20', 'Final'),
(29, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-04-20', 'Final'),
(30, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-04-20', 'Final'),
(31, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-04-20', 'Final'),
(32, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-04-20', 'Final'),
(33, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-04-20', 'Final'),
(34, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-04-20', 'Final'),
(35, 'pengeluaran', NULL, 'Tuban', NULL, NULL, 100000, 'solar 10 liter', NULL, '2026-04-20', 'Final'),
(36, 'pemasukan', 1, 'Mahendradatta', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-04-20', 'Final'),
(37, 'pemasukan', 2, 'Tuban', 'Dump Truck Besar', 400, 88889000, NULL, 'Cash', '2026-04-30', 'Draft'),
(38, 'pemasukan', 1, 'Mahendradatta', 'Dump Truck Besar', 12, 2933000, NULL, 'Cash', '2026-04-30', 'Final'),
(39, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 4.5, 1100000, NULL, 'Cash', '2026-04-30', 'Draft'),
(40, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 1, 244000, NULL, 'Cash', '2026-04-30', 'Draft'),
(41, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 1, 244000, NULL, 'Cash', '2026-04-30', 'Draft'),
(42, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 1, 244000, NULL, 'Cash', '2026-04-30', 'Draft'),
(43, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 1, 244000, NULL, 'Cash', '2026-04-30', 'Draft'),
(44, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 1, 244000, NULL, 'Cash', '2026-04-30', 'Draft'),
(45, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 1, 244000, NULL, 'Cash', '2026-04-30', 'Draft'),
(46, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 1, 244000, NULL, 'Cash', '2026-04-30', 'Draft'),
(47, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 1, 244000, NULL, 'Cash', '2026-04-30', 'Draft'),
(48, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 1, 244000, NULL, 'Cash', '2026-04-30', 'Draft'),
(49, 'pemasukan', 1, 'Mahendradatta', 'Dump Truck Besar', 40, 9778000, NULL, 'Cash', '2026-04-30', 'Final'),
(50, 'pemasukan', 1, 'Mahendradatta', 'Dump Truck Besar', 10, 2444000, NULL, 'Transfer', '2026-04-30', 'Final'),
(51, 'pengeluaran', NULL, 'Tuban', NULL, NULL, 120000, 'sollar 20 liter', NULL, '2026-04-30', 'Draft'),
(52, 'pengeluaran', NULL, 'Tuban', NULL, NULL, 20000, 'Solar', NULL, '2026-04-30', 'Draft'),
(53, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 12, 2933000, NULL, 'Transfer', '2026-05-03', 'Final'),
(54, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 4, 978000, NULL, 'Cash', '2026-05-03', 'Final'),
(55, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 4, 978000, NULL, 'Cash', '2026-05-03', 'Final'),
(56, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 4, 978000, NULL, 'Cash', '2026-05-03', 'Final'),
(57, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 4, 978000, NULL, 'Cash', '2026-05-03', 'Final'),
(58, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 4, 978000, NULL, 'Cash', '2026-05-03', 'Final'),
(59, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 4, 978000, NULL, 'Cash', '2026-05-03', 'Final'),
(60, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 4, 978000, NULL, 'Cash', '2026-05-03', 'Final'),
(61, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 4, 978000, NULL, 'Cash', '2026-05-03', 'Final'),
(62, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 4, 978000, NULL, 'Cash', '2026-05-03', 'Final'),
(63, 'pemasukan', 1, 'Tuban', 'Dump Truck Besar', 4, 978000, NULL, 'Cash', '2026-05-03', 'Final'),
(64, 'pengeluaran', NULL, 'Tuban', NULL, NULL, 200000, 'sollar 20 liter', NULL, '2026-05-03', 'Final');

-- --------------------------------------------------------

--
-- Table structure for table `kirim_stok`
--

CREATE TABLE `kirim_stok` (
  `id` int(11) NOT NULL,
  `material_id` int(11) DEFAULT NULL,
  `cabang` varchar(25) DEFAULT NULL,
  `jumlah` int(11) DEFAULT NULL,
  `status` varchar(25) DEFAULT NULL,
  `jumlah_truck` int(11) DEFAULT NULL,
  `total_kubik` double DEFAULT NULL,
  `tanggal` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kirim_stok`
--

INSERT INTO `kirim_stok` (`id`, `material_id`, `cabang`, `jumlah`, `status`, `jumlah_truck`, `total_kubik`, `tanggal`) VALUES
(1, 1, 'Tuban', NULL, 'Dikonfirmasi', 20, 200, '2026-02-25'),
(2, 1, 'Tuban', NULL, 'Dikonfirmasi', 10, 100, '2026-02-25'),
(3, 4, 'Mahendradatta', NULL, 'Dikonfirmasi', 10, 100, '2026-02-25'),
(4, 5, 'Tuban', NULL, 'Dikonfirmasi', 10, 100, '2026-02-25'),
(5, 3, 'Mahendradatta', NULL, 'Dikonfirmasi', 10, 100, '2026-02-25'),
(6, 2, 'Mahendradatta', NULL, 'Dikonfirmasi', 10, 100, '2026-02-25'),
(7, 1, 'Tuban', NULL, 'Dikonfirmasi', 5, 50, '2026-02-25'),
(8, 5, 'Tuban', NULL, 'Dikonfirmasi', 5, 50, '2026-02-25'),
(9, 2, 'Tuban', NULL, 'Dikonfirmasi', 5, 50, '2026-02-25'),
(10, 1, 'Tuban', NULL, 'Dikonfirmasi', 30, 300, '2026-02-25'),
(11, 4, 'Tuban', NULL, 'Dikonfirmasi', 10, 100, '2026-02-25'),
(12, 5, 'Tuban', NULL, 'Dikonfirmasi', 2, 20, '2026-02-25'),
(13, 1, 'Tuban', NULL, 'Dikonfirmasi', 1, 5, '2026-02-25'),
(14, 2, 'Tuban', NULL, 'Dikonfirmasi', 12, 120, '2026-02-25'),
(15, 2, 'Mahendradatta', NULL, 'Dikonfirmasi', 12, 120, '2026-02-25'),
(16, 6, 'Tuban', NULL, 'Dikonfirmasi', 10, 100, '2026-02-25'),
(17, 1, 'Tuban', NULL, 'Dikonfirmasi', 12, 120, '2026-02-25'),
(18, 2, 'Mahendradatta', NULL, 'Dikonfirmasi', 20, 200, '2026-02-25'),
(19, 1, 'Tuban', NULL, 'Dikonfirmasi', 12, 120, '2026-02-25'),
(20, 1, 'Mahendradatta', NULL, 'Dikonfirmasi', 12, 120, '2026-02-25'),
(21, 2, 'Mahendradatta', NULL, 'Dikonfirmasi', 12, 120, '2026-02-25'),
(23, 1, 'Tuban', NULL, 'Dikonfirmasi', 12, 120, '2026-02-25'),
(26, 1, 'Tuban', NULL, 'Dikonfirmasi', 12, 120, '2026-03-01'),
(27, 1, 'Tuban', NULL, 'Dikonfirmasi', 12, 123, '2026-03-01'),
(28, 3, 'Tuban', NULL, 'Dikonfirmasi', 12, 120, '2026-03-01'),
(29, 1, 'Tuban', NULL, 'Dikonfirmasi', 4, 40, '2026-03-01'),
(30, 2, 'Tuban', NULL, 'Dikonfirmasi', 12, 120, '2026-03-02'),
(31, 2, 'Mahendradatta', NULL, 'Dikonfirmasi', 12, 120, '2026-03-08'),
(32, 3, 'Tuban', NULL, 'Dikonfirmasi', 12, 120, '2026-03-10'),
(34, 1, 'Tuban', NULL, 'Dikonfirmasi', 25, 250, '2026-03-12'),
(35, 1, 'Tuban', NULL, 'Dikonfirmasi', 1, 15, '2026-03-12'),
(36, 3, 'Tuban', NULL, 'Dikonfirmasi', 25, 250, '2026-03-12'),
(37, 3, 'Mahendradatta', NULL, 'Dikonfirmasi', 25, 250, '2026-03-12'),
(38, 1, 'Tuban', NULL, 'Dikonfirmasi', 24, 240, '2026-03-14'),
(40, 1, 'Tuban', NULL, 'Dikonfirmasi', 10, 100, '2026-04-14'),
(42, 2, 'Tuban', NULL, 'Dikonfirmasi', 12, 120, '2026-04-28'),
(43, 3, 'Mahendradatta', NULL, 'Dikonfirmasi', 12, 120, '2026-04-30'),
(44, 3, 'Tuban', NULL, 'Dikonfirmasi', 12, 120, '2026-04-30'),
(45, 2, 'Tuban', NULL, 'Dikonfirmasi', 5, 50, '2026-04-30'),
(47, 4, 'Mahendradatta', NULL, 'Dikonfirmasi', 12, 120, '2026-04-30'),
(48, 1, 'Tuban', NULL, 'Menunggu', 6, 60, '2026-05-03'),
(49, 2, 'Tuban', NULL, 'Menunggu', 3, 30, '2026-05-03'),
(50, 11, 'Tuban', NULL, 'Menunggu', 12, 120, '2026-05-03');

-- --------------------------------------------------------

--
-- Table structure for table `material`
--

CREATE TABLE `material` (
  `id` int(11) NOT NULL,
  `nama` varchar(50) DEFAULT NULL,
  `harga` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `material`
--

INSERT INTO `material` (`id`, `nama`, `harga`) VALUES
(1, 'Pasir Halus', 1100000),
(2, 'Pasir Pasang', 1000000),
(3, 'Pasir Cor', 900000),
(4, 'Koral 1/2', 1100000),
(5, 'Koral 2/3', 1000000),
(11, 'Batu Kali', 1400000);

-- --------------------------------------------------------

--
-- Table structure for table `stok_cabang`
--

CREATE TABLE `stok_cabang` (
  `id` int(11) NOT NULL,
  `material_id` int(11) DEFAULT NULL,
  `lokasi` varchar(25) DEFAULT NULL,
  `jumlah` int(11) DEFAULT NULL,
  `total_kubik` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stok_cabang`
--

INSERT INTO `stok_cabang` (`id`, `material_id`, `lokasi`, `jumlah`, `total_kubik`) VALUES
(1, 1, 'Tuban', 34, 643.5),
(2, 4, 'Mahendradatta', NULL, 206.5),
(3, 5, 'Tuban', NULL, 139),
(4, 3, 'Mahendradatta', NULL, 165.5),
(5, 2, 'Mahendradatta', NULL, 255.5),
(6, 2, 'Tuban', NULL, 51),
(7, 4, 'Tuban', NULL, 0),
(9, 1, 'Mahendradatta', NULL, 25.5),
(11, 3, 'Tuban', NULL, 298),
(12, 2, 'Pusat', NULL, 2030),
(13, 3, 'Pusat', NULL, 260),
(14, 1, 'Pusat', NULL, 100),
(15, 4, 'Pusat', NULL, 30),
(16, 11, 'Pusat', NULL, 130);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(25) DEFAULT NULL,
  `password` varchar(12) DEFAULT NULL,
  `role` varchar(12) DEFAULT NULL,
  `cabang` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`, `cabang`) VALUES
(1, 'admin', '123', 'admin', 'Pusat'),
(2, 'tuban', '123', 'cabang', 'Tuban'),
(3, 'mahendra', '123', 'cabang', 'Mahendradatta');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `keuangan`
--
ALTER TABLE `keuangan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `kirim_stok`
--
ALTER TABLE `kirim_stok`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `material`
--
ALTER TABLE `material`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stok_cabang`
--
ALTER TABLE `stok_cabang`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `keuangan`
--
ALTER TABLE `keuangan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT for table `kirim_stok`
--
ALTER TABLE `kirim_stok`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `material`
--
ALTER TABLE `material`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `stok_cabang`
--
ALTER TABLE `stok_cabang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
