my sql 1 pract




1. Create the "Student" table and display the data
sql
Copy code
CREATE TABLE Student (
    student_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    age INT,
    grade CHAR(1),
    major VARCHAR(50)
);

-- Inserting data into the table
INSERT INTO Student (student_id, first_name, last_name, age, grade, major)
VALUES 
(1, 'John', 'Doe', 20, 'A', 'Computer Science'),
(2, 'Jane', 'Smith', 21, 'A', 'Computer Science'),
(3, 'Alex', 'Johnson', 22, 'B', 'Mathematics'),
(4, 'Emily', 'Davis', 23, 'A', 'Physics'),
(5, 'David', 'Duck', 21, 'C', 'Biology'),
(6, 'Don', 'Dev', 22, 'B', 'Mathematics');

-- Display the table
SELECT * FROM Student;
2. Change the name of student "Jane" to "Jenne"
sql
Copy code
UPDATE Student
SET first_name = 'Jenne'
WHERE first_name = 'Jane';
3. Find Students with a Specific Grade "A"
sql
Copy code
SELECT * FROM Student
WHERE grade = 'A';
4. Count the Number of Students in Each Major
sql
Copy code
SELECT major, COUNT(*) AS number_of_students
FROM Student
GROUP BY major;
5. Order Students by Age in Ascending Order
sql
Copy code
SELECT * FROM Student
ORDER BY age ASC;
6. Find the Oldest Student and the Youngest Student
Oldest Student:

sql
Copy code
SELECT * FROM Student
ORDER BY age DESC
LIMIT 1;
Youngest Student:

sql
Copy code
SELECT * FROM Student
ORDER BY age ASC
LIMIT 1;
7. Update a Student's Major (for student_id=2)
sql
Copy code
UPDATE Student
SET major = 'Data Science'
WHERE student_id = 2;
8. Delete a Student Record of student_id=6
sql
Copy code
DELETE FROM Student
WHERE student_id = 6;
9. Count the Number of Students in Each Major where grade = 'A'
sql
Copy code
SELECT major, COUNT(*) AS number_of_students
FROM Student
WHERE grade = 'A'
GROUP BY major;
10. Count the Number of Students in Each Grade having count greater than 2
sql
Copy code
SELECT grade, COUNT(*) AS student_count
FROM Student
GROUP BY grade
HAVING COUNT(*) > 2;
