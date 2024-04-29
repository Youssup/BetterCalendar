import React from 'react';

function App() {
  const runApp = () => {
    window.location.href = 'http://127.0.0.1:5000/run';
  };

  return (
    <div className="App">
      <button className="btn btn-primary" onClick={runApp}>
        Log in with Google
      </button>
    </div>
  );
}

export default App;