-- MySQL Rideshare App Database Schema
-- CPSC 408 Assignment 05
-- Based on ER Diagram and 3NF Normalization

-- Create database
CREATE DATABASE IF NOT EXISTS rideshare_db;
USE rideshare_db;

-- Drop tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS RIDE;
DROP TABLE IF EXISTS DRIVER;
DROP TABLE IF EXISTS RIDER;
DROP TABLE IF EXISTS USER;

-- USER Entity
-- Stores all user authentication and basic information
CREATE TABLE USER (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_number VARCHAR(20),
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- DRIVER Entity
-- Stores driver-specific information and vehicle details
-- Relationship: USER → DRIVER (1:1, optional)
CREATE TABLE DRIVER (
    driver_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    license_number VARCHAR(50) NOT NULL,
    license_expiry DATE,
    vehicle_make VARCHAR(50),
    vehicle_model VARCHAR(50),
    vehicle_year INT,
    vehicle_color VARCHAR(30),
    license_plate VARCHAR(20),
    insurance_number VARCHAR(50),
    driver_mode ENUM('active', 'inactive') DEFAULT 'inactive',
    registration_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_driver_mode (driver_mode),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- RIDER Entity
-- Stores rider-specific information and payment preferences
-- Relationship: USER → RIDER (1:1, optional)
CREATE TABLE RIDER (
    rider_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    payment_info VARCHAR(100),
    preferred_payment VARCHAR(50),
    credit_card_last4 VARCHAR(4),
    default_location VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- RIDE Entity
-- Stores ride information linking drivers and riders
-- Relationships: DRIVER → RIDE (1:M), RIDER → RIDE (1:M)
CREATE TABLE RIDE (
    ride_id INT AUTO_INCREMENT PRIMARY KEY,
    driver_id INT NOT NULL,
    rider_id INT NOT NULL,
    pickup_location VARCHAR(200) NOT NULL,
    pickup_address VARCHAR(255),
    pickup_latitude DECIMAL(10, 8),
    pickup_longitude DECIMAL(11, 8),
    dropoff_location VARCHAR(200) NOT NULL,
    dropoff_address VARCHAR(255),
    dropoff_latitude DECIMAL(10, 8),
    dropoff_longitude DECIMAL(11, 8),
    pickup_time DATETIME,
    dropoff_time DATETIME,
    ride_status ENUM('pending', 'in_progress', 'completed', 'cancelled') DEFAULT 'pending',
    rating INT CHECK (rating >= 1 AND rating <= 5),
    rating_comment TEXT,
    fare_amount DECIMAL(10, 2),
    distance_miles DECIMAL(8, 2),
    duration_minutes INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (driver_id) REFERENCES DRIVER(driver_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (rider_id) REFERENCES RIDER(rider_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_driver_id (driver_id),
    INDEX idx_rider_id (rider_id),
    INDEX idx_ride_status (ride_status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Verify tables created
SHOW TABLES;

