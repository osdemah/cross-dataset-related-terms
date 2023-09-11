import 'bootstrap/dist/css/bootstrap.css';
import './App.css';
import './Client.js';
import React, { useState } from 'react';
import {getRelatedTerms} from "./Client";

function App() {
  const [term, setTerm] = useState(null);
  const [relatedTerms, setRelatedTerms] = useState([]);

  function handleChange(event) {
    setTerm(event.target.value);
  }

  function handleSubmit(event) {
      setRelatedTerms([])
      getRelatedTerms(term).then(res => {
          const data = res.data;
          setRelatedTerms(data);
      })
    event.preventDefault();
  }

  return (
      <div className="container">
          <div className="row justify-content-center mt-3">
              <div className="input-group w-auto">
                  <input
                      type="text"
                      className="form-control"
                      placeholder="Enter a term"
                      onChange={handleChange}
                  />
                  <button onClick={handleSubmit} className="btn btn-primary" type="button" id="button-lookup" data-mdb-ripple-color="dark">
                      Lookup
                  </button>
              </div>
          </div>
          <div className="row justify-content-center my-3">
              <div className="col col-lg-3">
              <table className="table">
                  <thead>
                  <tr>
                      <th scope="col">related term</th>
                      <th scope="col">weight</th>
                  </tr>
                  </thead>
                  <tbody>
                  {relatedTerms.map(d => (
                      <tr>
                          <td>{d.relatedTerm}</td>
                          <td>{parseFloat(d.weight).toFixed(2)}</td>
                      </tr>))}
                  </tbody>
              </table>
                  </div>
          </div>
      </div>
  );
}

export default App;
