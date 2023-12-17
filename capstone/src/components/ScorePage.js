import axios from "axios";
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

function ScorePage(){
    const location=useLocation();
    const navigate=useNavigate();
    const username=new URLSearchParams(location.search).get('username')
    const type=new URLSearchParams(location.search).get('type')
    const {state:answers}=location;
    const [questions,setQuestions]=useState([]);
    const [user_answers,setUserAnswers]=useState([]);
    const [actual_answers,setActualAnswers]=useState([]);
    const [score,updateScore]=useState(0);

    const saveQuizData = async () => {
      try {
        const response = await axios.post('http://localhost:5000/api/saveQuizData', {
          username: username,  // Replace with the actual username or retrieve it from user authentication
          score: score,
          quesType:"TrueFalse"
        });
        console.log(response.data);
      } catch (error) {
        console.error('Error saving quiz data', error.message);
      }
      navigate("/home")
    };
  
    const goback = () => {
      navigate('/home');
    };
    const getData=async()=>{
        await axios.post(`http://127.0.0.1:5001/check_answers`,{answers}).then((response)=>{
            console.log("getting")
            console.log(response.data)
            setQuestions(response.data.questions)
            setActualAnswers(response.data.actual_answer)
            setUserAnswers(response.data.user_answer)
            updateScore(response.data.score)
        })
    }
    useEffect(()=>{
        getData();
    },[answers])
   return <div className="login-container">
    <center>
      <h1>Quiz Over!! Your Score Acquired is : {score}</h1>
    </center>
   <h3>Preview your answers here:</h3>
   
      {questions.map((ques,index)=>(
        <div key={index}>
          <h4>Question {index+1}: {ques.question}</h4>
          {type=="MCQ"?(
            <ol>
              <li>{ques.A}</li>
              <li>{ques.B}</li>
              <li>{ques.C}</li>
              <li>{ques.D}</li>
            </ol>
          ):(
            <></>
          )}
          {
            type=="TrueFalse"?(
              <div>
              <h3>Answer: {actual_answers[index]?"True":"False"}</h3>
              <h3> {user_answers[index] !== null ? (
        `Your Answer: ${user_answers[index] ? "True" : "False"}`
      ) : (
        "Your Answer: "
      )}</h3>
              </div>
              ):(

              <div>
                <h3>Answer: {actual_answers[index]}</h3>
                <h3>Your Answer: {user_answers[index]}</h3>
                <h5>Explanation: {ques.explanation}</h5>
               </div>             
              
                )
              }

        </div>
      ))}
    <button onClick={saveQuizData}>Save Quiz Data</button>
    <button onClick={goback}>Go Back to Main Menu</button>
 </div>
}
export default ScorePage;