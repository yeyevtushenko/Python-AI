--1. Виведіть усі можливі пари рядків викладачів і груп.
SELECT Teachers.Name, Groups.Name
FROM Teachers
CROSS JOIN Groups;

SELECT Faculties.Name, Departments.Name, Faculties.Financing, Departments.Financing
FROM Faculties
INNER JOIN Departments ON Faculties.Id = Departments.FacultyId
WHERE Departments.Financing > Faculties.Financing;

SELECT Curators.Surname, Groups.Name AS GroupName
FROM Curators
INNER JOIN GroupsCurators ON Curators.Id = GroupsCurators.CuratorId
INNER JOIN Groups ON GroupsCurators.GroupId = Groups.Id;

SELECT Teachers.Name, Teachers.Surname
FROM Teachers
JOIN Lectures ON Lectures.TeacherId = Teachers.Id
JOIN GroupsLectures ON GroupsLectures.LectureId = Lectures.Id
JOIN Groups ON Groups.Id = GroupsLectures.GroupId
WHERE Groups.Name = 'P107';

SELECT Teachers.Surname, Faculties.Name
FROM Teachers
JOIN TeacherDepartment ON TeacherDepartment.TeacherId = Teachers.Id
JOIN Faculties ON Faculties.Id = TeacherDepartment.FacultyId;

SELECT Departments.Name, Groups.Name
FROM Departments
JOIN Groups ON Groups.DepartmentId = Departments.Id;

SELECT Subjects.Name
FROM Subjects
JOIN Lectures ON Lectures.SubjectId = Subjects.Id
JOIN Teachers ON Teachers.Id = Lectures.TeacherId
WHERE Teachers.Name = 'Samantha' AND Teachers.Surname = 'Adams';


SELECT DISTINCT Departments.Name
FROM Subjects
JOIN SubjectsDepartments ON Subjects.Id = SubjectsDepartments.SubjectId
JOIN Departments ON Departments.Id = SubjectsDepartments.DepartmentId
WHERE Subjects.Name = 'Database Theory';

SELECT Groups.Name
FROM Groups
JOIN Departments ON Departments.Id = Groups.DepartmentId
JOIN Faculties ON Faculties.Id = Departments.FacultyId
WHERE Faculties.Name = 'Computer Science';

SELECT Groups.Name, Faculties.Name
FROM Groups
JOIN Departments ON Departments.Id = Groups.DepartmentId
JOIN Faculties ON Faculties.Id = Departments.FacultyId
WHERE Groups.Year = 5;

SELECT Teachers.Name || ' ' || Teachers.Surname AS "Teacher Name",
       Subjects.Name AS "Subject",
       Groups.Name AS "Group"
FROM Lectures
JOIN Teachers ON Teachers.Id = Lectures.TeacherId
JOIN Subjects ON Subjects.Id = Lectures.SubjectId
JOIN GroupsLectures ON GroupsLectures.LectureId = Lectures.Id
JOIN Groups ON Groups.Id = GroupsLectures.GroupId
WHERE Lectures.LectureRoom = 'B103';
