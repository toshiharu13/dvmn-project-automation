from datetime import datetime

from models import StudentLevels

from .models import (PMWorkTime, ProjectManagers, Projects, Students,
                     StudentsToCommands, StudentsWorkTime, Teams)


def distribution_by_teams(skill):
    students_schedule = []
    skills = StudentLevels.objects.get(level_name=skill)
    students_group = skills.students.all()
    for student in students_group:

        student_work_time = StudentsWorkTime.objects.get(student=student)
        if student_work_time.student.is_in_team == False:
            student_work_intervals = []
            works_to = str(student_work_time.works_to)
            student_work_intervals.append(works_to)
            works_from = str(student_work_time.works_from)
            FMT = "%H:%M:%S"
            works_to = datetime.strptime(works_to, FMT)
            works_from = datetime.strptime(works_from, FMT)
            timedelta = works_to - works_from
            half_hour = datetime.strptime("00:30:00", FMT)
            if timedelta.seconds > 1800:
                while works_to != works_from:
                    half_hour_interval = works_to - half_hour
                    half_hour_interval = str(half_hour_interval)
                    works_to = str(half_hour_interval)
                    works_to = datetime.strptime(works_to, FMT)
                    student_work_intervals.append(half_hour_interval)
            student_work_interval = {"student": student_work_time.student, "student_work_intervals": student_work_intervals}
            students_schedule.append(student_work_interval)
    students_schedule = sorted(students_schedule, key=lambda k: k['student_work_intervals']) 

    try:
        student_with_worst_schedule = students_schedule[0]
    except IndexError:
        logging.error("Все ученики распределены по командам!")
        exit()
    worst_schedule = student_with_worst_schedule["student_work_intervals"][0]
    line_up = []
    for student_schedule in students_schedule:
        if worst_schedule in student_schedule["student_work_intervals"]:
            line_up.append(student_schedule["student"])
    project = Projects.objects.first()
    project_manager = ProjectManagers.objects.first()
    new_team = Teams.objects.create(name="Команда1", project=project, project_manager=project_manager)
    students = [StudentsToCommands(team=new_team, student=student_to_commands) for student_to_commands in line_up]
    students_to_commands = StudentsToCommands.objects.bulk_create(students)
    for student in students_to_commands:
        student = Students.objects.get(telegram_id=student.student.telegram_id)
        student.is_in_team = True
        student.save()



def distribution_by_teams_groups():
    skills = list(StudentLevels.objects.values_list("level_name", flat=True))
    for skill in skills:
        distribution_by_teams(skill)

distribution_by_teams_groups()