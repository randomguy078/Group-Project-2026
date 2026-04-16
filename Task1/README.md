## Library Management System - Group 46 Task 1

## Our group members

- CHAN CHI LONG 14262858 (Group Leader)
- LIU PAK HON 14263450
- WONG WANG CHI 13878108

## Features

- Return book and Borrow book
-	Book searching
-	Student data and penalty management
-	Popular books checker
- Payment logs
- Penalty checker
-	Data storage system

## Introduction Video
https://drive.google.com/file/d/168R6nwMbi7oi5VJ-eFdDBBDZhBA5YTWd/preview



## System default username and password

- Username: admin
- Password: admin

## System structure

Make sure all the files below existed in the **exact same folder**:

* `main.py` - Run this file to start the program.
* `auth.py` - The login UI.
* `gui_main.py` - Core functions and UI.
* `data_manager.py` - Generating Book ID, load and save data to the library_data.pkl file.
* `library_data.pkl` - *(Auto-generated)* This file will be created automatically after you entered any student/book data to the system.

## Quick Start

Requirements:
1. Python version: 3.7 or higher

Install and Run the system:

1. Download the system folder to your computer, then run the following command in the command prompt.

    ```shell
    cd path/to/the/system/folder
    ```
2. Run the following command.

    For Windows:

    ```shell
    python main.py
    ```

    For MacOS/Linux:

    ```shell
    python3 main.py
    ```

## How to use the system
1. Enter the username and password.
2. You will see the borrow books page after you have logged in
3. Press the **Books** tab and enter the ISBN, Name, Author and Category of your book(s).
4. Press the **Students** tab and enter the Student ID and the name of the student. (Student ID format is s + 7 digits) 
