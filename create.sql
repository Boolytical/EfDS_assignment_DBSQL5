DROP TABLE IF EXISTS Student;
CREATE TABLE Student(
  st_name VARCHAR(50) NOT NULL, 
  email VARCHAR(50) UNIQUE NOT NULL,
  universityid INTEGER NOT NULL,
  PRIMARY KEY (universityID));
  
DROP TABLE if exists Question;
CREATE TABLE Question(
  title VARCHAR(50) NOT NULL,
  content VARCHAR(50) NOT NULL,
  questionid INTEGER PRIMARY KEY AUTOINCREMENT 
  );

DROP TABLE if exists Task;
CREATE TABLE Task(
  title VARCHAR(50) NOT NULL,
  content VARCHAR(50) NOT NULL,
  taskid INTEGER PRIMARY KEY AUTOINCREMENT
  );
  --check if the intermidiate table Task_question is correct
DROP TABLE IF EXISTS Task_question;
CREATE TABLE Task_question(
  taskid INTEGER NOT NULL,
  questionid INTEGER NOT NULL ,
  FOREIGN KEY (taskid) REFERENCES Task ON UPDATE RESTRICT ON DELETE RESTRICT,
  FOREIGN KEY (questionid) REFERENCES Question ON UPDATE RESTRICT ON DELETE RESTRICT,
  PRIMARY KEY (taskid, questionid));
  
DROP TABLE IF EXISTS Assignment;
CREATE TABLE Assignment(
  universityid INTEGER NOT NULL,
  taskid INTEGER NOT NULL,
  assignmentid INTEGER PRIMARY KEY AUTOINCREMENT,
  FOREIGN KEY (taskid) REFERENCES Task ON UPDATE RESTRICT ON DELETE RESTRICT, 
  FOREIGN KEY (universityid) REFERENCES Student ON UPDATE RESTRICT ON DELETE RESTRICT
  ); 
  -- i am not sure if the trigger has the option of print, couldnt find anything about it 
CREATE TRIGGER IF NOT EXISTS NEW_ASSIGNMENT
AFTER INSERT ON Assignment
BEGIN 
	PRINT 'New assignment has been added'; 
END;


DROP TABLE IF EXISTS Submission; 
CREATE TABLE Submission(
  assignmentid INTEGER NOT NULL,
  submissionid INTEGER PRIMARY KEY AUTOINCREMENT, 
  FOREIGN KEY (assignmentid) REFERENCES Assignment ON UPDATE RESTRICT ON DELETE RESTRICT); 
  
CREATE TRIGGER IF NOT EXISTS NEW_SUBMISSION
AFTER INSERT ON Submission
BEGIN 
	PRINT 'New submission has been added';
END;
  
DROP TABLE IF EXISTS Answers;
CREATE TABLE Answers(
  content VARCHAR(50), 
  questionid INTEGER NOT NULL,
  submissionid INTEGER NOT NULL, 
  answerid INTEGER PRIMARY KEY AUTOINCREMENT, 
  FOREIGN KEY (questionid) REFERENCES Question ON UPDATE RESTRICT ON DELETE RESTRICT,
  FOREIGN KEY (submissionid) REFERENCES Submission ON UPDATE RESTRICT ON DELETE RESTRICT);

-- doesnt make sense to allow updates on sumbsission while there is an evaluation request (I chenge it to restrict)
DROP TABLE IF EXISTS EvaluationRequest;
CREATE TABLE EvaluationRequest(
  submissionid INTEGER NOT NULL, 
  requestid INTEGER PRIMARY KEY AUTOINCREMENT,
  FOREIGN KEY (submissionid) REFERENCES Submission ON UPDATE RESTRICT ON DELETE RESTRICT);

-- Make sure that the ON UPDATE NO ACTION can be added on scores
-- or make a INSTEAD OF trigger so the table scores isn't changed
DROP TABLE IF EXISTS Evaluation;
CREATE TABLE Evaluation(
  evaluationid INTEGER NOT NULL,
  requestid INTEGER PRIMARY KEY AUTOINCREMENT);

DROP TABLE IF EXISTS Score;
CREATE TABLE Score(
  value INTEGER NOT NULL CHECK (value BETWEEN 1 AND 10), 
  scoreid INTEGER PRIMARY KEY AUTOINCREMENT,
  answerid INTEGER NOT NULL, 
  evaluationid INTEGER NOT NULL, 
  FOREIGN KEY (answerid) REFERENCES Answers, 
  FOREIGN KEY (evaluationid) REFERENCES Evaluation);

DROP TABLE IF EXISTS EvaluationFinished;
CREATE TABLE EvaluationFinished(
  finishedid INTEGER PRIMARY KEY AUTOINCREMENT, 
  evaluationid INTEGER NOT NULL,
  FOREIGN KEY (evaluationid) REFERENCES Evaluation ON UPDATE RESTRICT ON DELETE RESTRICT);

CREATE TRIGGER IF NOT EXISTS SUBMISSION_EVALUATED
AFTER INSERT ON EvaluationFinished
BEGIN 
	PRINT 'Your submission has been evaluated';
END;

CREATE TRIGGER IF NOT EXISTS COMMITED_SUBMISSION
BEFORE INSERT on Answers
BEGIN 
SELECT CASE
WHEN NOT((SELECT submissionid FROM EvaluationRequest WHERE submissionid == NEW.submissionid) ISNULL)
THEN RAISE(ABORT, 'Cannot add answer to a submission which is commited')
END;
END;

CREATE TRIGGER IF NOT EXISTS SCORES_ADDED
BEFORE INSERT ON Score
BEGIN
SELECT CASE
WHEN NOT ((SELECT evaluationid FROM EvaluationFinished WHERE evaluationid == NEW.evaluationid) ISNULL)
THEN RAISE(ABORT, 'Cannot add score to an evaluation which is finished')
END;
END;
