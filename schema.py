import urllib.request    # needed for download of the example database
import shutil            # needed for unziping of the example database
import os                # for checking existence/removing of a file

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

base = declarative_base()
class Task(base):
    _tablename_ = "Task"
    taskID = Column(Integer,primary_key=True)
    title = Column(string(50))
    content = Column(string(50))
    assignment_r = relationship("Assignment")
    task_q_r = relationship("Task_question")
    
class Assignment(base):
    _tablename_ = "Assignment"
    assignmentID = Column(Integer,primary_key=True)
    universityID = Column(ForeignKey('Student.universityID'), nullable=True)
    taskID = Column(ForeignKey('Task.taskID'), nullable=True)
    submission_r = relationship("Submission")
    
class Task_question(base):
    _tablename_ = "Task_question"
    taskID = Column(ForeignKey('Task.taskID'), nullable=True)
    questionID = Column(ForeignKey('Question.QuestionID'), nullable=True)

class Student(base):
    _tablename_ = "Student"
    universityID = Column(Integer,primary_key=True)
    name = Column(string)
    email = Column(string)
    sttudent_r = relationship("Assignment")
    
class Submission(base):
    _tablename_ = "Submission"
    submissionID = Column(Integer,primary_key=True)
    assignmentID = Column(ForeignKey('Assignment.AssignmentID'), nullable=True)
    eval_r = relationship("EvaluationRequest")
    answers_r = relationship("Answers")
    
class EvaluationRequest(base):
    _tablename_ = "EvaluationRequest"
    requestID = Column(Integer,primary_key=True)
    submissionID = Column(ForeignKey('Submission.submissionID'), nullable=True)
    eval_r = relationship("Evaluation")
    
class Question(base):
    _tablename_ = "Question"
    questionID = Column(Integer,primary_key=True)
    title = Column(String(50))
    content = Column(string(50))
    task_q_r = relationship("Task_question")
    answer_r = relationship("Answer")
    
class Answers(base):
    _tablename_ = "Answers"
    answerID = Column(Integer,primary_key=True)
    content = Column(string(1000))
    questionId = Column(ForeignKey('Question.QuestionID'), nullable=True)
    sumissionID = Column(Integer)
    scores_r = relationship("Scores")
    
class Evaluation(base):
    _tablename_ = "Evaluation"
    evaluationID = Column(Integer, primary_key = True)
    requestID = Column(ForeignKey('EvaluationRequest.requestID'), nullable=True)
    evaluation_f_r = relationship("EvaluationFinished")
    scores_r = relationship("Scores")
class Scores(base):
    _tablename_ = "Scores"
    scoreID = Column(Integer, primary_key = True)
    value = Column(Integer)
    answerID Column(ForeignKey('Answers.answerId'),nullable = True)
    evaluationID = Column(Integer)
    
class EvaluationFinished(base):
    _tablename_ = "EvaluationFinished"
    finishedID = Column(Integer, primary_key = True)
    evaluationId = Column(ForeignKey('Evaluation.evaluationID'),nullable = True)