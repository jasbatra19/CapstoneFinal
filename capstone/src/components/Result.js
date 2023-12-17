// QuizHistory.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';
import BarChart from './Charts/Barchart';

function Result() {
    const navigate=useNavigate();
    const location = useLocation();
    const username = new URLSearchParams(location.search).get('username');
    const [quizHistory, setQuizHistory] = useState([]);
    const goback = () => {
      navigate('/home');
    };
    useEffect(() => {
        const fetchQuizHistory = async () => {
            try {
                const response = await axios.get(`http://localhost:5000/api/user_quiz_data/${username}`);
                setQuizHistory(response.data);
            } catch (error) {
                console.error('Error fetching quiz history', error.message);
            }
        };

        fetchQuizHistory();
    }, [username]);

    const barChartData = [['Date', 'Score'], ...quizHistory.map((entry) => [entry.date, entry.score])];
    console.log(barChartData);

    return (
        <div style={styles.container}>
            <h2 style={styles.heading}>Quiz History for {username}</h2>
            <BarChart data={barChartData} />
            <div className="button-container">
          <button onClick={() => goback()}>Go Back to Main Menu</button>
        </div> 
        </div>
    );
}

const styles = {
    container: {
        textAlign: 'center',
        padding: '20px',
        margin:'50px',
    },
    heading: {
        color:'#3498db', // Change the color to your preference
        fontSize: '24px',
        marginBottom: '15px',
    },
};

export default Result;
