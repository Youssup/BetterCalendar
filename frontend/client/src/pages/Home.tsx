import React from 'react';

function Home() {
  const runApp = () => {
    window.location.href = 'http://127.0.0.1:5000/run';
  };

  return (
    <div className="flex justify-center">
      <button className="btn btn-primary" onClick={runApp}>
        Run the application
      </button>
    </div>
  );
}

export default Home;