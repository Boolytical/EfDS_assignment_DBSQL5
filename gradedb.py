from os.path import exists
from schema import *
from asyncio.windows_events import NULL
from logging import exception
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.sql import select

class Gradedb:
    def __init__(self, fileName, mustExist):
        """Initializes an object for the Gradedb class. Based on the given arguments checks if 
        the file exists or not and acts accordingly.

        Args:
            fileName (string): the name of the .db file
            mustExist (boolean): Whether the file exists or not.

        Raises:
            Exception: If the file does not exists and mustExist argument is True
            Exception: If the file exists and mustExist argument is False
        """
        file_exists = exists(fileName)
        if not file_exists and mustExist:
            raise Exception("Argument mustExist was set to True but the database file does not exist")
        if not mustExist and file_exists:
            raise Exception("Argument mustExist was set to False but the database file exists. If you want \
                to create a new database, please remove the .db file or give a different name")
        
        addr = "sqlite:///" + fileName
        self._engine = create_engine(addr,echo=False)
        if not mustExist:
            # gets the classes from the schema file and creates the database
            base.metadata.create_all(self._engine)
        self._sessionMaker = sessionmaker(bind=self._engine)
    
    def newSession(self):
        """Gives a session to the database.

        Returns:
            sqlalchemy.orm.session.Session: A session to the database
        """
        return self._sessionMaker()

    def checkUniId(self, id):
        """Checks if the university id is provided in the correct format.

        Args:
            id (string): University id

        Raises:
            Exception: When the first character is not "S"
            Exception: When the rest characters are not numeric

        Returns:
            Boolean: True if the univresity id is correct
        """
        if not id[0] == "S":
            raise Exception("University id not given correctly. Format: S#######")
        else:
            if not id[1:].isnumeric():
                raise Exception("University id hmust had 6 digits after S")
        return True

    def addStudent(self, name, email, id):
        """The teacher adds the students to the database.

        Args:
            name (string) : Name
            email (string) : Email
            id (string) : University id

        Raises:
            Exception: When students with no name are provided

        Returns:
            string: university id
        """
        if not all(x.isalpha() or x.isspace() for x in name):
            raise Exception("Name must be provided")
        self.checkUniId(id)
        with self.newSession() as ses:
            s = Student(name=name, email=email, universityid=id) #suppose we have the class Student
            ses.add(s)
            ses.commit()
            return s.universityid
    
    def addQuestion(self, title, content):
        """The teacher adds questions to the database.

        Args:
            title (string) : The title of the question
            content (string) : The content of the question

        Raises:
            Exception: When the questions have not content.

        Returns:
            integer: Question id
        """
        if len(content) == 0:
            raise Exception("Content must be provided")
        else:
            with self.newSession() as ses:
                q = Question(title = title, content = content)
                ses.add(q)
                ses.commit()
                return q.questionid


    def addTask(self, questionids, title, content):
        """The teacher adds tasks to the database and assigns multiple questions to it.

        Args:
            questionids (list) : A list with the question id(integer)
            title (string) : The title of the question
            content (string) : The content of the question

        Returns:
            integer: Task id
        """
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
        """A teacher adds an Assignment to the database. An Assignment is one Task given to one Student.

        Args:
            universityid (integer) : University id
            taskid (integer) : Task id

        Raises:
            exception: When a task has no questions.

        Returns:
            integer: Assignment id
        """
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
        """A student add New Submission to the database.

        Args:
            assignmentid (integer): Assignment id

        Returns:
            integer: Submission id
        """
        with self.newSession() as ses:
            s = Submission(assignmentid = assignmentid)
            ses.add(s)
            ses.commit()
            return s.submissionid
    
    def addAnswer(self, content, questionid, submissionid):
        """A student adds answers to their questions. It checks if the submissionid has an ongoing evaluation request. 
        If so, changes will be ignored.

        Args:
            content (string) : The content of the answer
            questionid (integer) : Question id
            submissionid (integer) : Submission id

        Returns:
            integer: Answer id
        """
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
        """A student commits a submission.

        Args:
            submissionid (integer) : Submission id

        Returns:
            integer: Request id
        """
        with self.newSession() as ses:
            cs = EvaluationRequest(submissionid = submissionid)
            ses.add(cs)
            ses.commit()
            print("New submission")
            return cs.requestid

    def newEvaluation(self, requestid):
        """The teacher adds new evaluation to the database.

        Args:
            requestid (integer): Rdquest id

        Returns:
            integer: Evaluation id
        """
        with self.newSession() as ses:
            e = Evaluation(requestid = requestid)
            ses.add(e)
            ses.commit()
            return e.evaluationid
    
    def addScore(self, score, evaluationid, answerid):
        """The teacher adds scores to the database.

        Args:
            score (integer): The score of the assignment
            evaluationid (integer): Evaluation id
            answerid (integer): Answer id

        Raises:
            Exception: When the evaluation is finished, any further scores added will be ignored

        Returns:
            integer: Score id
        """
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
        """The teacher adds commited evaluations to the database.

        Args:
            evaluationid (integer): Evaluation id

        Returns:
            integer: Evaluation finished id
        """
        with self.newSession() as ses:
            ev = EvaluationFinished(evaluationid = evaluationid)
            ses.add(ev)
            ses.commit()
            print("Submission evaluated")
            return ev.finishedid

