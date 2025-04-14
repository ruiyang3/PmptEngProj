CREATE TABLE tb1 (
    one TEXT,
    two INTEGER
);

CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT
);

CREATE TABLE designations (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    title TEXT,
    descriptions TEXT
);

CREATE TABLE schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    title TEXT,
    time_in TEXT,
    time_out TEXT
);

CREATE TABLE leaves (
    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    employee_id INTEGER REFERENCES employees(id) NOT DEFERRABLE,
    start_date TEXT,
    end_date TEXT,
    type TEXT,
    reason TEXT
);

CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    employee_id INTEGER REFERENCES employees(id) NOT DEFERRABLE,
    title TEXT,
    time TEXT,
    date TEXT
);

CREATE TABLE overtime (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    employee_id INTEGER REFERENCES employees(id),
    duration INTEGER,
    date TEXT
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    designation_id INTEGER REFERENCES designations(id),
    schedule_id INTEGER REFERENCES schedules(id),
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    gender TEXT
);
