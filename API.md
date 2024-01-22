## Methods
### Get All Programs
```
from degreescaper import get_all_programs

print(get_all_programs())
```
Returns:
A dictionary containing the following:
```
{'Major': ['Minor', 'BS', 'MS', 'PhD'],...}
```
### Get Concentrations/Threads for Program
```
from degreescaper import get_concentrations

print(get_concentrations(program, degree))
```
Parameters:
- `program` - Program name
- `degree` - Degree type

Returns:
A list containing the following:
```
['Concentration 1', 'Concentration 2', ...]
```
### Get Courses for Program
```
from degreescaper import get_courses

print(get_courses(program, degree))
```
Parameters:
- `program` - Program name
- `degree` - Degree type

Returns:
A list containing the following:
```
['Course 1', 'Course 2', ...]
```
### Get Courses For Program with Concentration/Thread
```
from degreescaper import get_courses

print(get_courses(program, degree, concentration))
```
Parameters:
- `program` - Program name
- `degree` - Degree type
- `concentration` - Concentration/Thread type

Returns:
A list containing the following:
```
['Course 1', 'Course 2', ...]
```
### Get All Bachelors Programs
```
from degreescaper import get_bachelors_programs

print(get_bachelors_programs())
```
Returns:
A list containing the following:
```
['Program 1', 'Program 2', ...]
```
### Get All Masters Programs
```
from degreescaper import get_masters_programs

print(get_masters_programs())
```
Returns:
A list containing the following:
```
['Program 1', 'Program 2', ...]
```
### Get All Doctoral Programs
```
from degreescaper import get_doctoral_programs

print(get_doctoral_programs())
```
Returns:
A list containing the following:
```
['Program 1', 'Program 2', ...]
```
### Get All Minors Programs
```
from degreescaper import get_minors_programs

print(get_minors_programs())
```
Returns:
A list containing the following:
```
['Program 1', 'Program 2', ...]
```
### Get Total Credit Hours Required for Program
```
from degreescaper import get_total_credit_hours

print(get_total_credit_hours(program, degree))
```
Returns:
An integer containing the following:
```
24
```