-- Drop existing tables if they exist
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS programs CASCADE;
DROP TABLE IF EXISTS colleges CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create users table
CREATE TABLE IF NOT EXISTS users
(
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Create colleges table
CREATE TABLE IF NOT EXISTS colleges
(
    college_code VARCHAR(20) PRIMARY KEY,
    college_name VARCHAR(255) NOT NULL
);

-- Create programs table with foreign key constraint
CREATE TABLE IF NOT EXISTS programs
(
    program_code VARCHAR(20) PRIMARY KEY,
    program_name VARCHAR(255) NOT NULL,
    college_code VARCHAR(20),
    CONSTRAINT program_college_code_fkey FOREIGN KEY (college_code)
        REFERENCES colleges (college_code)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- Create students table with foreign key constraint
CREATE TABLE IF NOT EXISTS students
(
    id_number VARCHAR(9) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(6) NOT NULL,
    year_level SMALLINT NOT NULL,
    program_code VARCHAR(20),
    CONSTRAINT student_program_code_fkey FOREIGN KEY (program_code)
        REFERENCES programs (program_code)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_colleges_college_code ON college(college_code);
CREATE INDEX IF NOT EXISTS idx_programs_program_code ON programs(program_code);
CREATE INDEX IF NOT EXISTS idx_students_id_number ON students(id_number);

