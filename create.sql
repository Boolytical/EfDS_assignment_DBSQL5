DROP TABLE if exists Question;
CREATE TABLE Question(
  title VARCHAR(50) NOT NULL,
  content VARCHAR(50) NOT NULL,
  questionid INTEGER, 
  PRIMARY KEY (questionid));

DROP TABLE if exists Task;
CREATE TABLE Task(
  title VARCHAR(50) NOT NULL,
  content VARCHAR(50) NOT NULL,
  questionid INTEGER NOT NULL, 
  taskid INTEGER NOT NULL,
  PRIMARY KEY (taskid));
  
DROP TABLE IF EXISTS Task_question;
CREATE TABLE Task_question(
  taskid INTEGER NOT NULL,
  questionid INTEGER NOT NULL,
  FOREIGN KEY (taskid) REFERENCES Task ON UPDATE RESTRICT ON DELETE RESTRICT,
  FOREIGN KEY (questionid) REFERENCES Question ON UPDATE RESTRICT ON DELETE RESTRICT,
  PRIMARY KEY (taskid, questionid));
  
DROP TABLE IF EXISTS Assignment;
CREATE TABLE Assignment(
  universityid INTEGER NOT NULL,
  taskid INTEGER NOT NULL,
  assignmentid INTEGER NOT NULL,
  FOREIGN KEY (taskid) REFERENCES Task, 
  PRIMARY KEY (assignmentid)); 
  
CREATE TRIGGER IF NOT EXISTS NEW_ASSIGNMENT
AFTER INSERT ON Assignment
BEGIN 
	PRINT('New assignment has been added') 
END;

DROP TABLE IF EXISTS Student;
CREATE TABLE Student(
  name VARCHAR(50), 
  email VARCHAR(50),
  universityid INTEGER NOT NULL,
  PRIMARY KEY (universityID));
  
DROP TABLE IF EXISTS Submission; 
CREATE TABLE Submission(
  assignmentid INTEGER NOT NULL,
  submissionid INTEGER NOT NULL, 
  PRIMARY KEY (submissionid), 
  FOREIGN KEY (assignmentid) REFERENCES Assignment); 
  
CREATE TRIGGER IF NOT EXISTS NEW_SUBMISSION
AFTER INSERT ON Submission
BEGIN 
	PRINT('New submission has been added') 
END;
  
DROP TABLE IF EXISTS Answers;
CREATE TABLE Answers(
  content VARCHAR(50), 
  questionid INTEGER NOT NULL,
  submissionid INTEGER NOT NULL, 
  answerid INTEGER NOT NULL, 
  Primary KEY (answerid), 
  FOREIGN KEY (questionid) REFERENCES Question,
  FOREIGN KEY (submissionid) REFERENCES Submission);

DROP TABLE IF EXISTS EvaluationRequest;
CREATE TABLE EvaluationRequest(
  submissionid INTEGER NOT NULL, 
  requestid INTEGER NOT NULL,
  PRIMARY KEY (requestid),
  FOREIGN KEY (submissionid) REFERENCES Submission ON UPDATE NO ACTION);

-- Make sure that the ON UPDATE NO ACTION can be added on scores
-- or make a INSTEAD OF trigger so the table scores isn't changed
DROP TABLE IF EXISTS Evaluation;
CREATE TABLE Evaluation(
  evaluationid INTEGER NOT NULL,
  requestid INTEGER NOT NULL, 
  PRIMARY KEY (evaluationid));

DROP TABLE IF EXISTS Score;
CREATE TABLE Score(
  value INTEGER NOT NULL CHECK (value BETWEEN 1 AND 10), 
  scoreid INTEGER NOT NULL,
  answerid INTEGER NOT NULL, 
  evaluationid INTEGER NOT NULL, 
  PRIMARY KEY (scoreid), 
  FOREIGN KEY (answerid) REFERENCES Answers, 
  FOREIGN KEY (evaluationid) REFERENCES Evaluation);

DROP TABLE IF EXISTS EvaluationFinished;
CREATE TABLE EvaluationFinished(
  finishedid INTEGER NOT NULL, 
  evaluationid INTEGER NOT NULL,
  PRIMARY KEY (finishedid), 
  FOREIGN KEY (evaluationid) REFERENCES Evaluation);

CREATE TRIGGER IF NOT EXISTS SUBMISSION_EVALUATED
AFTER INSERT ON EvaluationFinished
BEGIN 
	PRINT('Your submission has been evaluated') 
END;
