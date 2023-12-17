import "../App.css"; // Import the CSS file
import { useAuth0 } from "@auth0/auth0-react";
import React from "react";

function Login() {
  const { user, loginWithRedirect, isAuthenticated, logout } = useAuth0();
  console.log("Current user: ", user);

  const handleLogin = () => {
    if (!isAuthenticated) {
      loginWithRedirect();
    } else {
      console.log("I am logged in !!");
      window.location.replace("http://localhost:3000/login");
    }
  };

  return (
    <div className="login-container">
      {isAuthenticated ? (
        <button className="logout-btn" onClick={(e) => logout()}>
          Logout
        </button>
      ) : (
        <div className="login-content">
          <h1>PlaceMe Assist</h1>
          <h3>
            Welcome to PlaceMe Assist, your one-stop solution for revision success! We offer a variety of interactive features and resources to help you learn and remember key concepts. Sign up for a free account today and start improving your skills!
          </h3>
          <h3>Interview preparation made easy!</h3>

          <div className="benefits-container">
            <h4>Explore the Benefits:</h4>
            <ul>
              <li>Interactive quizzes designed to challenge and expand your knowledge.</li>
              <li>Personalized learning paths tailored to meet your unique needs.</li>
              <li>Convenient access to a diverse range of educational resources—all in one place.</li>
            </ul>
          </div>

          <button className="login-btn" onClick={handleLogin}>
            <b>
            Login with Redirect
            </b>
          </button>
        </div>
      )}
    </div>
  );
}

export default Login;
