from schema import *
from asyncio.windows_events import NULL
from logging import exception
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.sql import select

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
                s = Student(name=name, email=email, universityid=id) #suppose we have the class Student
                ses.add(s)
                ses.commit()
                return s.universityid
    
    def addQuestion(self, title, content):
        '''The teacher adds questions by providing the title and the content (input of addQuestion function).
        It checks if the content of the question is empty, if so, it raises an exception'''
        if not content.isalnum():
            raise Exception("Content must be provided")
        else:
            with self.newSession() as ses:
                q = Question(title = title, content = content)
                ses.add(q)
                ses.commit()
                return q.questionid


    def addTask(self, questionids, title, content):
        ''''The teacher adds tasks by providing ta list with the questionids, title and content (input of addTask function).'''
        with self.newSession() as ses:
            t = Task(title = title, content = content)
            ses.add(t)
            ses.commit() #commit to create the taskid 
            for i in questionids: #iterating over each questionid
                task_question = Task_question(questionid = i, taskid = t.taskid)
                ses.add(task_question)
                ses.commit()
            return t.taskid
    
    def addAssignment(self, universityid, taskid ):
        '''The teacher adds assignment by providing the universityid, which is the studentid and taskid (input of addAssignemnt function).
        It checks if the tasks have questions, if not raises an exception.'''
        query = select(Task_question).where(Task_question.taskid == taskid)
        result = self._engine.execute(query)
        if len(result.all()) == 0:
            raise exception('Does not make sence to add assignement of a task with no questions')
        else:
            with self.newSession() as ses:
                a = Assignment(universityid = universityid, taskid = taskid)
                ses.add(a)
                ses.commit()
                print("New assignment added")
                return a.assignmentid
    
    def newSubmission(self,assignmentid):
        ''''A student adds new submission by providing the assignmentid (input of the newsubmission function).'''
        with self.newSession() as ses:
            s = Submission(assignmentid = assignmentid)
            ses.add(s)
            ses.commit()
            return s.submissionid
    
    def addAnswer(self, content, questionid, submissionid):
        '''A student adds answers by providing the content, questionid, and submissionid (input of the addAnswer function).
        It checks if the submissionid has an ongoing evaluation request. If so, changes will be ignored.'''
        query = select(EvaluationRequest).where(EvaluationRequest.submissionid == submissionid)
        result = self._engine.execute(query)
        if not len(result.all()) == 0:
            print("Evaluation request has been requested for this submission. Answers will be not be added")
            pass
        else:
            with self.newSession() as ses:
                an = Answers(content = content, questionId = questionid, submissionid = submissionid)
                ses.add(an)
                ses.commit()
                return an.answerid

    def commitSubmission(self, submissionid):
        '''A student commits a submission by providing the submissionid (input of the commitSubmission function).'''
        ## TO DO: use submissionid > assignmentid > universityid to check if the universityid already has a submissionid to their name ##
        # if select(Student).where()
        #     pass
        # else:
        with self.newSession() as ses:
            cs = EvaluationRequest(submissionid = submissionid)
            ses.add(cs)
            ses.commit()
            print("New submission")
            return cs.requestid

    def newEvaluation(self, requestid):
        '''The teacher adds new evaluation by providing the requestid (input of the newEvaluation function).'''
        with self.newSession() as ses:
            e = Evaluation(requestid = requestid)
            ses.add(e)
            ses.commit()
            return e.evaluationid
    
    def addScore(self, score, evaluationid, answerid):
        '''The teacher adds scores by providing the score, evaluationid and answerid (input of the addScore function).
        If the evaluation is finished, any further scores added will be ignored'''
        q = select(EvaluationFinished).where(EvaluationFinished.evaluationid == evaluationid)
        result = self._engine.execute(q)
        if not len(result.all()) == 0:
            print("The evaluation is finalized, scores added to the evaluation will be ignored")
            pass
        elif score<1 or score>10:
            raise Exception("Score must be between 1 and 10")
        else:
            with self.newSession() as ses:
                sc = Scores(value = score, evaluationid = evaluationid, answerid = answerid)
                ses.add(sc)
                ses.commit()
                return sc.scoreid
    
    def commitEvaluation(self, evaluationid):
        '''The teacher adds commited evaluations by providing the evaluationid (input of the commitEvaluation function).'''
        with self.newSession() as ses:
            ev = EvaluationFinished(evaluationid = evaluationid)
            ses.add(ev)
            ses.commit()
            print("Submission evaluated")
            return ev.finishedid


        




    

        



        
        
    



