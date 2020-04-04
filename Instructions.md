#### Send_emails.py works by relative path. It assumes the user has the folder with this utility as a subdirecory of a main folder with the following structure

```
Main_folder		
	├───Automated_email	
  │   ├───names.txt
  │   ├───Letter_everyone.txt
  │   ├───Letter_notreceived.txt
  │   ├───Letter_received.txt
	├───Week10	
	│   ├───student_1
	│   ├───student_2
	│   ├───student_3
	│   ├───student_4
	│   ├───student_5
	│   ├───student_19
	│   ├───student_20
	│   ├───student_21
	│   ├───student_22
	│   ├───ZZ_student_23
	│   ├───ZZ_student_24
	│   ├───ZZ_student_25
	│   ├───ZZ_student_26
	│   ├───ZZ_student_27
	└───week11	
	    ├───student_1
	    ├───student_2
	    ├───student_20
	    ├───student_21
	    ├───student_22
	    ├───ZZ_student_23
	    ├───ZZ_student_24
	    ├───ZZ_student_25
	    ├───ZZ_student_26
	   ...	
```
The script will be called using two arguments. The first one is the name of the subfolder that contains the folders of each student. The folders of students that start with ZZ_ are those that didn't provide an assignment for that particular homework (in this case week11). The program is run in bash or windows prompt as follows:
```bash
python Send_emails.py week11 status
```
will email all the students in the names.txt file 
