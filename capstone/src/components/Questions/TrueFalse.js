import React, { useEffect, useState } from "react";
import axios from "axios";
import { useLocation, useNavigate, } from "react-router-dom";
import QuestionNavigation from "./QuestionNavigation"; // Import the QuestionNavigation component

function TrueFalse() {
  const navigate=useNavigate();
  const location = useLocation();
  const type = new URLSearchParams(location.search).get('type');
  const difficulty = new URLSearchParams(location.search).get('difficulty');
  const username = new URLSearchParams(location.search).get('username');
  const [question_bank, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState(Array(10).fill(null)); // Initialize answers with 15 null values
  const [selectedAnswer, setSelectedAnswer] = useState(null); // State to track the selected answer

  const questions = async () => {
    const response = await axios.get(`http://127.0.0.1:5001/random_question?type=${type}&difficulty=${difficulty}`);
    setQuestions(response.data);
    console.log(response.data)
  }

  const handleNextQuestion = () => {
    if (currentQuestion < 9) {
      // Store the selected answer before moving to the next question
      if (selectedAnswer !== null) {
        const updatedAnswers = [...answers];
        updatedAnswers[currentQuestion] = selectedAnswer;
        setAnswers(updatedAnswers);
        setSelectedAnswer(null); // Clear the selected answer
      }
      setCurrentQuestion(currentQuestion + 1);
    }
  }
  const handlePreviousQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  }

  const handleAnswerSubmit = (answer) => {
    const updatedAnswers = [...answers];
    updatedAnswers[currentQuestion] = answer;
    setAnswers(updatedAnswers);
    console.log(updatedAnswers)
    // handleNextQuestion(); // Automatically go to the next question
    setSelectedAnswer(answer); // Highlight the selected answer

  }

  const handleQuizSubmit = () => {
    console.log("answers",answers)
    navigate(`/ScorePage?username=${username}&type=${type}`,{state:answers})    
  }

  const answerButtonStyle = {
    selected: {
      backgroundColor: "#3498db",
      color: "white",
    },
    unselected: {
      backgroundColor: "#27ae60", // or "#FFFFFF" for white
      color: "white",
    },
  };
  

  useEffect(() => {
    questions();
  }, [type, difficulty]);

  if (question_bank.length === 0) {
    return <p>Loading...</p>;
  }

  const currentQuestionData = question_bank[currentQuestion];
  return (
    <>
    <div className="login-container">
      <h3>Question {currentQuestion + 1}</h3>
      <p>{currentQuestionData.question}</p>

      {/* Add some margin between the question and the buttons */}
      <div style={{ marginBottom: "80px" }}>
        <button
          style={
            answers[currentQuestion] === "True" ? answerButtonStyle.selected : answerButtonStyle.unselected
          }
          onClick={() => handleAnswerSubmit(true)}
          >
          True
        </button>
        <button
          style={
            answers[currentQuestion] === "False" ? answerButtonStyle.selected : answerButtonStyle.unselected
          }
          onClick={() => handleAnswerSubmit(false)}
          >
          False
        </button>
      
      </div>

      {/* Add some margin between the question and the navigation panel */}
     


      {/* Add some margin between the question and the Previous/Next buttons */}
      <div style={{ marginTop: "20px" }}>
        <button onClick={handlePreviousQuestion}>Previous Question</button>
        <button onClick={handleNextQuestion}>Next Question</button>
      </div>
      {currentQuestion === 9 && (
        <button onClick={handleQuizSubmit}>Submit Quiz</button>
        )}
    </div>
    <div style={{ marginBottom: "20px" }}>
        <QuestionNavigation
          totalQuestions={question_bank.length}
          currentQuestion={currentQuestion}
          setCurrentQuestion={setCurrentQuestion}
          selectedAnswers={answers}
          />
      </div>

        </>
  );
}
export default TrueFalse;
