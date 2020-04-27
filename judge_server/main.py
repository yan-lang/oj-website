"""
评测分发服务器(负载均衡服务器)
现阶段不分发, 直接轮寻查找是否有submission需要评测, 有直接遍历评测
"""

import logging
from datetime import datetime
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from table import Submission, GradeUnit, GradeReport
from ycc_grader.grader.lex import LexerGrader
from ycc_grader.grader.common.report import AbstractReport

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Judge Server")


def grade_submission(submission, session):
    logger.info("Start grading")
    grader = LexerGrader(test_code_dir='ycc_grader/public/code/lexer', test_gold_dir='ycc_grader/public/golden/lexer')
    reports: [AbstractReport] = grader.run(submission.submitted_file)

    grade_units = []
    grade = 0
    total_grade = 0
    for report in reports:
        grade_units.append(GradeUnit(name=report.report_name,
                                     grade=report.grade, total_grade=report.total_grade,
                                     detail=report.detail))
        grade += report.grade
        total_grade += report.total_grade

    grade_report = GradeReport(is_passed=grade == total_grade,
                               grade=int(100 * (grade / total_grade)), total_grade=100,
                               submission_id=submission.id,
                               units=grade_units)
    session.add(grade_report)
    logger.info("Grade done")


if __name__ == '__main__':
    # 初始化数据库连接: password 为自己数据库密码
    # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
    logger.info("Connecting database")
    engine = create_engine('sqlite:///../web_server/db.sqlite3')
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    logger.info("Connected")

    while True:
        sleep(2)
        submissions = session.query(Submission).filter(Submission.status == Submission.SUBMITTED)
        for submission in submissions:
            logger.info("Found submission {0}/{1}...".format(submission.id, submission.submitted_file[:20]))
            submission.last_grade_time = datetime.now()
            grade_submission(submission, session)
            submission.status = Submission.GRADED
            session.commit()

    # 关闭Session:
    session.close()
