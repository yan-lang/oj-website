# Judge Server

```sql
select *
from oj_submission s
where not exists (select * from oj_gradereport report where report.submission_id = s.id)
```

```python
# 打印类型和对象的name属性:
for submission in submissions:
    print(submission)
    
units = [GradeUnit(name="基础", grade=70, total_grade=100, detail="test"),
         GradeUnit(name="综合", grade=20, total_grade=100, detail="test")]
report = GradeReport(is_passed=False, grade=80, total_grade=100, submission_id=13, units=units)
session.add(report)
    
reports = session.query(GradeReport).all()
for report in reports:
    print(report, report.units)
    
units = session.query(GradeUnit).all()
print(units)
```