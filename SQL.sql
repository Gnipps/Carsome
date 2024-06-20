-- Q1: Display student’s ID and name who at least have one similar course with student ID “01”. 
SELECT DISTINCT s.s_name, s.s_id from student s
INNER join score sc on s.s_id = sc.s_id
INNER JOIN course c on sc.c_id = c.c_id
INNER JOIN score sc2 ON c.c_id = sc2.c_id
WHERE EXISTS (
    SELECT 1
    FROM Score sc2
    WHERE sc2.s_id = '01'  
    AND sc2.c_id = sc.c_id
);

-- Q2: Create segment for course score [100-85], [85-70], [70-60], [<60] and count number of students under those segments for all courses, column to display also are course ID and course name.
SELECT c.c_id AS course_id,
    c.c_name AS course_name,
    SUM(CASE WHEN sc.s_score >= 85 AND sc.s_score <= 100 THEN 1 ELSE 0 END) AS `100-85`,
    SUM(CASE WHEN sc.s_score >= 70 AND sc.s_score < 85 THEN 1 ELSE 0 END) AS `85-70`,
    SUM(CASE WHEN sc.s_score >= 60 AND sc.s_score < 70 THEN 1 ELSE 0 END) AS `70-60`,
    SUM(CASE WHEN sc.s_score < 60 THEN 1 ELSE 0 END) AS `<60`
FROM Course c
INNER JOIN Score sc ON c.c_id = sc.c_id
GROUP BY c.c_id, c.c_name
ORDER BY c.c_id;

-- Q3: Display student ID, course ID and student score where student has the same score but in different course.
SELECT 
    s1.s_id AS student_id,
    s1.c_id AS course_id1,
    s2.c_id AS course_id2,
    s1.s_score AS student_score
FROM Score s1
JOIN Score s2 
ON s1.s_id = s2.s_id
    AND s1.s_score = s2.s_score
    AND s1.c_id < s2.c_id;

-- Q4: Query for the top 2 highest in scoring from each course and display column course ID, course name, student name and student score.
SELECT rs.c_id AS course_id,
    c.c_name AS course_name,
    s.s_name AS student_name,
    rs.s_score AS student_score
FROM 
    (SELECT s.c_id, s.s_id, s.s_score, 
    RANK() OVER (PARTITION BY s.c_id ORDER BY s.s_score DESC) AS score_rank
    FROM score s
    ORDER BY s_score DESC, s_id ASC) rs
JOIN course c ON rs.c_id = c.c_id
JOIN student s ON rs.s_id = s.s_id
WHERE rs.score_rank <= 2
ORDER BY rs.c_id, rs.score_rank, s.s_name;

-- Q5: Query for all student’s information that has registered for all courses
WITH TotalCourses AS (
    SELECT COUNT(*) AS course_count
    FROM Course
),
StudentCourseCounts AS (
    SELECT s.s_id,COUNT(DISTINCT sc.c_id) AS courses_registered
    FROM score sc
    JOIN student s ON sc.s_id = s.s_id
    GROUP BY s.s_id
)
SELECT s.*
FROM student s
JOIN StudentCourseCounts scc ON s.s_id = scc.s_id
JOIN TotalCourses tc ON scc.courses_registered = tc.course_count
ORDER BY s.s_id;