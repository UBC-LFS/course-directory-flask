# LFS Course Directory (with Flask)
This project displays the courses available in the selected session alongside the most recent available syllabus.


# Notes for maintaining this project:
Last updated: 2023-05-18
## Updating the syllabuses
When adding new syllabuses, ensure that the points below remain consistent. Not doing so may result in syllabuses not properly displaying:
1. All syallbuses are stored in the `templates/CourseDirectory` folder
2. Each subfolder in `templates/CourseDirectory` is named based on the session name (e.g. `2022W1`)
3. Within the session folder, there should be another subfolder named after the course.
4. Inside the course folder, there should be an `index.html` file and maybe a `source` folder containing the syllabus if the syllabus is not the `index.html` file

## Notes for developers
### What does each file do?

### Potential future errors
1. All data for courses are retrieved from `https://courses.students.ubc.ca/cs/servlets/SRVCourseSchedule?`, if this API changes the way the data is formatted, the functions to retrieve and format the data may stop working