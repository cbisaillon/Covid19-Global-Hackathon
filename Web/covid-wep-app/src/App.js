import React from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Feed from './components/Feed';
import Navbar from './components/Navbar';

function App() {
  return (
    <div>
      <Navbar />
      <Feed />
    </div> 
  );
}

export default App;
