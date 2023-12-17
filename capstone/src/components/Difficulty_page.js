import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

function Difficulty_level() {
  const navigate = useNavigate();
  const location = useLocation();
  const type = new URLSearchParams(location.search).get("type");
  const username = new URLSearchParams(location.search).get("username");

  const handleDiff = (difficulty) => {
    navigate(`/${type}?username=${username}&difficulty=${difficulty}&type=${type}`);
  };

  const buttonContainerStyle = {
    display: "flex",
    justifyContent: "center",
    marginTop: "150px", // Adjust the margin as needed
  };

  const buttonStyle = {
    color:"black",
    margin: "0 10px", // Adjust the margin between buttons as needed
  };

  return (
    <div style={buttonContainerStyle}>
      <h3>Select Difficulty Levels:</h3>
      <button style={buttonStyle} onClick={() => handleDiff("easy")}>
        Easy
      </button>
      <button style={buttonStyle} onClick={() => handleDiff("medium")}>
        Medium
      </button>
      <button style={buttonStyle} onClick={() => handleDiff("hard")}>
        Hard
      </button>
    </div>
  );
}

export default Difficulty_level;
