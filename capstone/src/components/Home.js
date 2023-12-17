import { useNavigate } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import "../App.css";

function Home({ username }) {
  const navigate = useNavigate();
  const { logout, user } = useAuth0();

  const handleButton = (type) => {
    if (type === "Result") navigate(`/Result?username=${username}`, { replace: true });
    else navigate(`/Difficulty?type=${type}&username=${username}`);
  };

  return (
    <div className="center">
      <div className="home-container">
        <h1 className="main-title">PLACE ME ASSIST</h1>
       
        <div className="content">
          <h1>Welcome, {username}!</h1>
          <h3>Revising concepts made easy!</h3>
          <p className="home-description">
            Explore a variety of interactive quizzes and resources to enhance your learning experience.
          </p>
          <div className="button-container">
            <button onClick={() => handleButton("Result")}>SHOW PAST RESULTS</button>
            <button onClick={() => handleButton("MCQ")}>MCQs</button>
            <button onClick={() => handleButton("TrueFalse")}>True False</button>
            <button onClick={() => handleButton("OneLiner")}>One Liners</button>
            <button onClick={() => handleButton("OneWord")}>One Word</button>
            <button onClick={() => handleButton("Random")}>Random</button>
          </div>
        </div>
        <div className="button-container">
          <button onClick={() => logout()}>Logout</button>
        </div>  
      </div>
      
    </div>
  );
}

export default Home;
