import React, { useEffect, useState } from "react";
import axios from "axios";
import { useLocation, useNavigate } from "react-router-dom";
import QuestionNavigation from "./QuestionNavigation"; // Import the QuestionNavigation component

const OneWord = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const type = new URLSearchParams(location.search).get('type');
  const difficulty = new URLSearchParams(location.search).get('difficulty');
  const username = new URLSearchParams(location.search).get('username');
  const [question_bank, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState(Array(10).fill(null)); // Initialize answers with 15 null values
  const [selectedAnswer, setSelectedAnswer] = useState(""); // State to track the selected answer
  
  const questions = async () => {
    const response = await axios.get(`http://127.0.0.1:5001/random_question?type=${type}&difficulty=${difficulty}`);
    setQuestions(response.data);
    console.log(response.data);
  };

  const handleNextQuestion = () => {
    if (currentQuestion < 9) {
      if (selectedAnswer !== null) {
        const updatedAnswers = [...answers];
        updatedAnswers[currentQuestion] = selectedAnswer;
        setAnswers(updatedAnswers);
        // setSelectedAnswer(""); // Clear the selected answer
      }
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleAnswerChange = (e) => { 
    setSelectedAnswer(e.target.value);
  };

  const handleSpeechRecognition = () => {
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
      const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onresult = (event) => {
        const result = event.results[0][0].transcript;
        setSelectedAnswer(result);
      };

      recognition.onend = () => {
        recognition.stop();
      };

      recognition.start();
    } else {
      alert('Speech recognition is not supported in your browser.');
    }
  };

  const handleQuizSubmit = () => {
    const updatedAnswers = [...answers];
    updatedAnswers[currentQuestion] = selectedAnswer;
    setAnswers(updatedAnswers);
    navigate(`/ScorePage?username=${username}&type=${type}`, { state: answers });
  };
  
  const handleAnswerSubmit = (answer) => {
    const updatedAnswers = [...answers];
    updatedAnswers[currentQuestion] = answer;
    setAnswers(updatedAnswers);
    console.log(updatedAnswers)
    // handleNextQuestion(); // Automatically go to the next question
    setSelectedAnswer(answer); // Highlight the selected answer

  }

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

      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Enter your answer"
          value={selectedAnswer}
          onChange={handleAnswerChange}
        />
        <button onClick={handleSpeechRecognition}>Speech Input</button>
        <button
          
          onClick={() => handleAnswerSubmit(selectedAnswer)}
        >
          Save
        </button>
      </div>

      



{/* Buttons for next previous */}
      <div style={{ marginTop: "20px" }}>
        <button onClick={handlePreviousQuestion}>Previous Question</button>
        <button onClick={handleNextQuestion}>Next Question</button>
      </div>
      {currentQuestion === 9 && (
        <button onClick={handleQuizSubmit}>Submit Quiz</button>
      )}
    </div>
    {/* Navigation bar */}
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
};

export default OneWord;
