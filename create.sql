DROP TABLE if exists Questions;
CREATE TABLE Questions(
  title VARCHAR(50),
  content VARCHAR(50),
  questionid INTEGER, 
  PRIMARY KEY (questionid));

DROP TABLE if exists Tasks;
CREATE TABLE Tasks(
  title VARCHAR(50),
  content VARCHAR(50),
  questionid INTEGE NOT NULL, 
  taskid INTEGER NOT NULL,
  PRIMARY KEY (taskid));
  
DROP TABLE IF EXISTS Tasks_questions;
CREATE TABLE Task_questions(
  taskid INTEGER NOT NULL,
  questionid INTEGER NOT NULL,
  FOREIGN KEY (taskid) REFERENCES Tasks,
  FOREIGN KEY (questionid) REFERENCES Questions.
  PRIMARY KEY (taskid, questionid));
  
DROP TABLE IF EXISTS Assignments;
CREATE TABLE Assignments(
  universityid INTEGER NOT NULL,
  taskid INTEGER NOT NULL,
  assignmentid INTEGER NOT NULL,
  FOREIGN KEY (taskid) REFERENCES Tasks, 
  PRIMARY KEY (assignmentid)); 

DROP TABLE IF EXISTS Students;
CREATE TABLE Students(
  name VARCHAR(50), 
  email VARCHAR(50),
  universityid INTEGER NOT NULL,
  PRIMARY KEY (universityID));
  
DROP TABLE IF EXISTS Submissions; 
CREATE TABLE Submissions(
  assignmentid INTEGER NOT NULL,
  submissionid INTEGER NOT NULL, 
  PRIMARY KEY (submissionid), 
  FOREIGN KEY (assignmentid) REFERENCES Assignments); 
  
DROP TABLE IF EXISTS Answers;
CREATE TABLE Answers(
  content VARCHAR(50), 
  questionid INTEGER NOT NULL,
  submissionid INTEGER NOT NULL, 
  answerid INTEGER NOT NULL, 
  Primary KEY (answerid), 
  FOREIGN KEY (questionid) REFERENCES Questions,
  FOREIGN KEY (submissionid) REFERENCES Submissions);

DROP TABLE IF EXISTS EvaluationRequest;
CREATE TABLE EvaluationRequest(
  submissionid INTEGER NOT NULL, 
  requestid INTEGER NOT NULL,
  PRIMARY KEY (requestid),
  FOREIGN KEY (submissionid) REFERENCES Submissions ON UPDATE NO ACTION);

-- Make sure that the ON UPDATE NO ACTION can be added on scores
DROP TABLE IF EXISTS Evaluation;
CREATE TABLE Evaluation(
  evaluationid INTEGER NOT NULL,
  requestid INTEGER NOT NULL, 
  PRIMARY KEY (evaluationid));

DROP TABLE IF EXISTS Scores;
CREATE TABLE Scores(
  value INTEGER NOT NULL, 
  CHECK (value BETWEEN 1 AND 10),
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
