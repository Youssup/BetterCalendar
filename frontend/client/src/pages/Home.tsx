import React, { useState } from 'react';
import axios from 'axios';

function Home() {
  const [variation, setVariation] = useState('');
  const [defaultLocation, setDefaultLocation] = useState('');

  const handleSubmit = (e: { preventDefault: () => void; }) => {
    e.preventDefault();
    axios.get('http://localhost:5000/runOnApp', {
      params: {
        variation: variation,
        defaultLocation: defaultLocation
      }
    })
      .then((response: { data: number; }) => {
        console.log(response.data);
        window.open(response.data.toString(), '_blank');
      })
      .catch((error: any) => {
        console.error('There was an error!', error);
        window.open('There was an error!' + error.data.toString(), '_blank');
      });
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div className="flex justify-center">
          <input type="number" value={variation} onChange={(e) => setVariation(e.target.value)} placeholder="variation" className="input input-bordered w-full max-w-xs mt-4" />
        </div>
        <div className="flex justify-center">
          <input type="text" value={defaultLocation} onChange={(e) => setDefaultLocation(e.target.value)} placeholder="default location" className="input input-bordered w-full max-w-xs mt-4" />
        </div>
        <div className="flex justify-center">
          <button className="btn btn-primary mt-4" type='submit'>
            Run on App
          </button>
        </div>
      </form>
    </div>

  );
}

export default Home;