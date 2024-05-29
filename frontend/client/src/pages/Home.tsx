import React from 'react';

function Home() {
  const runApp = () => {
    window.open('http://127.0.0.1:5000/run', '_blank', 'noopener,noreferrer');
  };
return (
  <div>
      <div className="flex justify-center">
        <button className="btn btn-primary" onClick={runApp}>
          Run the program
        </button>
      </div>
      <div className="flex justify-center">
        <input id="variation" type="text" className="input input-bordered w-full max-w-xs mt-4"/>
      </div>
      <div className="flex justify-center">
        <input id="defaultLocation" type="text" className="input input-bordered w-full max-w-xs mt-4"/>
      </div>
    </div>
);
}

export default Home;