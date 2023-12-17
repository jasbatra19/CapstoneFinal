import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate, BrowserRouter } from 'react-router-dom';
import Login from './components/Login';
import Home from './components/Home';
import MCQ from './components/Questions/MCQ';
import TrueFalse from './components/Questions/TrueFalse';
import OneLiner from './components/Questions/OneLiner';
import OneWord from './components/Questions/OneWord';
import Random from './components/Questions/Random';
import Result from './components/Result';
import Difficulty_level from './components/Difficulty_page';
import ScorePage from './components/ScorePage';
import { useAuth0 } from "@auth0/auth0-react";
import axios from 'axios';

const App = () => {
  const {user,isAuthenticated}=useAuth0();
  useEffect(()=>{
    if(isAuthenticated){
      console.log("hello")
      console.log(user.email)
      axios.post("http://localhost:5000/api/register",{username:user.email,password:""}).then((res)=>{
        if(res.data.success==="False"){
        }
      })
     }
  },[isAuthenticated,user])
  return (
    <BrowserRouter>
      <Routes>
      <Route
        path="/login"
        element={isAuthenticated ? <Navigate to="/home" /> : <Login />}
      />
      <Route path="/home" element={isAuthenticated ? <Home username={user.email} /> : <Navigate to="/login" />} />
      <Route path="/MCQ" element={isAuthenticated ? <MCQ/> : <Navigate to="/home" />} />
      <Route path="/TrueFalse" element={isAuthenticated ? <TrueFalse/> : <Navigate to="/home" />} />
      <Route path="/OneWord" element={isAuthenticated ? <OneWord/> : <Navigate to="/home" />} />
      <Route path="/OneLiner" element={isAuthenticated ? <OneLiner/> : <Navigate to="/home" />} />
      <Route path="/Random" element={isAuthenticated ? <Random/> : <Navigate to="/home" />} />
      <Route path="/Result" element={isAuthenticated ? <Result/> : <Navigate to="/home" />} />
      <Route path="/Difficulty" element={isAuthenticated ? <Difficulty_level/> : <Navigate to="/home" />} />
      <Route path="/ScorePage" element={isAuthenticated ? <ScorePage/> : <Navigate to="/home" />} />
      <Route path="*" element={isAuthenticated ? <Navigate to="/home" /> : <Login />}/>
      </Routes>
    </BrowserRouter>
  );
};

export default App;