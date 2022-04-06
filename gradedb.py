from asyncio.windows_events import NULL
from curses.ascii import isalnum, isalpha
from logging import exception
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

class Gradedb:
    def __init__(self, fileName):
         addr = "sqlite:///" + fileName
         self._engine = create_engine(addr,echo=False)
         self._sessionMaker = sessionmaker(bind=self._engine)
    
    def newSession(self):
        return self._sessionMaker()

    def addStudent(self, name, email, id):
        '''The teacher adds the student's name, email and id to the database (input of addStudent function).
        It checks if there is a student with no name, if so, it raises an exception'''
        if not name.isalpha():
            raise Exception("Name must be provided")
        else:
            with self.newSession() as ses:
                s = Student(Name = name, Email = email, UniversityId=id) #suppose we have the class Student
                ses.add(s)
                ses.commit()
                return s.universityID
    
    def addQuestion(self, title, content):
        '''The teacher adds questions by providing the title and the content (input of addQuestion function).
        It checks if the content of the question is empty, if so, it raises an exception'''
        if not content.isalnum():
            raise Exception("Content must be provided")
        else:
            with self.newSession() as ses:
                q = Question(Title = title, Text = content)
                ses.add(q)
                ses.commit()
                return q.questionid


    def addTask(self, questionid, title, content):
        ''''The teacher adds tasks by providing the questionid, title and content (input of addTask function).'''
        with self.newSession() as ses:
            t = Task(Questions = questionid, Title = title, Text = content)
            ses.add(t)
            ses.commit()
            return t.taskid
    
    def addAssignment(self, universityid, taskid ):
        '''The teacher adds assignment by providing the universityid, which is the studentid and taskid (input of addAssignemnt function).
        It checks if the tasks have questions, if not raises an exception.'''
        if select(Task).where(Task.questionid) == NULL:
            raise exception('Does not make sence to add assignement of a task with no questions')
        else:
            with self.newSession() as ses:
                a = Assignment(Student = universityid, Task = taskid)
                ses.add(a)
                ses.commit()
                print("New assignment added")
                return a.assignmentid
    
    def newSubmission(self,assignmentid):
        ''''The teacher adds new submission by providing the assignmentid (input of the newsubmission function).'''
        with self.newSession() as ses:
            s = Submission(Assignment = assignmentid)
            ses.add(s)
            ses.commit()
            return s.submissionid
    
    def addAnswer(self, content, questionid, submissionid):
        '''The teacher adds answers by providing the content, questionid, and submissionid (input of the addAnswer function).
        It checks if the submissionid has an ongoing evaluation request. If so, changes will be ignored.'''
        if select(EvaluationRequest).where(EvaluationRequest.submissionid) != NULL:
            print("Evaluation request has been requested for this submission. Answers will be not be added")
            pass
        else:
            with self.newSession() as ses:
                an = Answer(Text = content, Question = questionid, Submission = submissionid)
                ses.add(an)
                ses.commit()
                return an.answerid

    def commitSubmission(self, submissionid):
        '''The teacher adds commited submissions by providing the submissionid (input of the commitSubmission function).'''
        ## TO DO: use submissionid > assignmentid > universityid to check if the universityid already has a submissionid to their name ##
        # if select(Student).where()
        #     pass
        # else:
        with self.newSession() as ses:
            cs = EvaluationRequest(Submission = submissionid)
            ses.add(cs)
            ses.commit()
            print("New submission")
            return cs.requestid

    def newEvaluation(self, requestid):
        '''The teacher adds new evaluation by providing the requestid (input of the newEvaluation function).'''
        with self.newSession() as ses:
            e = Evaluation(EvaluationRequest = requestid)
            ses.add(e)
            ses.commit()
            return e.evaluationid
    
    def addScore(self, score, evaluationid, answerid):
        '''The teacher adds scores by providing the score, evaluationid and answerid (input of the addScore function).
        If the evaluation is finished, any further scores added will be ignored'''
        if select(EvaluationFinished).where(EvaluationFinished.evaluationid) != NULL:
            print("The evaluation is finalized, scores added to the evaluation will be ignored")
            pass
        elif score<1 or score>10:
            raise Exception("Score must be between 1 and 10")
        else:
            with self.newSession() as ses:
                sc = Score(Value = score, Evaluation = evaluationid, Answer = answerid)
                ses.add(sc)
                ses.commit()
                return sc.scoreid
    
    def commitEvaluation(self, evaluationid):
        '''The teacher adds commited evaluations by providing the evaluationid (input of the commitEvaluation function).'''
        with self.newSession() as ses:
            ev = EvaluationFinished(Evaluation=evaluationid)
            ses.add(ev)
            ses.commit()
            print("Submission evaluated")
            return ev.finishedid


        




    

        



        
        
    



