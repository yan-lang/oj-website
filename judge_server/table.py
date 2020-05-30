from sqlalchemy import (Column, String, Integer, DateTime, SmallInteger,
                        Boolean, Text, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# 创建对象的基类:
Base = declarative_base()


class Assignment(Base):
    __tablename__ = 'oj_assignment'

    id = Column(Integer, primary_key=True)
    grader = Column(SmallInteger)

    LEXER_GRADER = 0
    PARSER_GRADER = 1
    SEMANTIC_GRADER = 2
    IR_GRADER = 3


class Submission(Base):
    __tablename__ = 'oj_submission'

    id = Column(Integer, primary_key=True)
    submitted_time = Column(DateTime)
    submitted_file = Column(String(300))
    status = Column(SmallInteger)
    last_grade_time = Column(DateTime)

    assignment_id = Column(Integer, ForeignKey("oj_assignment.id"))

    assignment = relationship("Assignment")

    SUBMITTED = 0
    GRADING = 1
    GRADED = 2

    def __repr__(self):
        return "{0}: {1} - status={2}: {3}".format(self.id, self.submitted_time,
                                                   self.status, self.last_grade_time)


class GradeUnit(Base):
    __tablename__ = 'oj_gradeunit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    grade = Column(Integer)
    total_grade = Column(Integer)
    detail = Column(Text)

    report_id = Column(Integer, ForeignKey("oj_gradereport.id"))

    report = relationship("GradeReport", back_populates="units")

    def __repr__(self):
        return "{0}({1}) - {2}/{3} -> report({4}) -> detail({5})".format(self.id, self.name,
                                                                         self.grade, self.total_grade,
                                                                         self.report_id, self.detail[:10])


class GradeReport(Base):
    __tablename__ = 'oj_gradereport'

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_passed = Column(Boolean)
    grade = Column(Integer)
    total_grade = Column(Integer)
    submission_id = Column(Integer)

    units = relationship("GradeUnit", order_by=GradeUnit.id, back_populates="report")

    def __repr__(self):
        return "{0}({1}) - {2}/{3} -> submission({4})".format(self.id,
                                                              self.is_passed,
                                                              self.grade,
                                                              self.total_grade,
                                                              self.submission_id)
