import React from "react";
import LoadWeather from '../Components/loadWeather';
import "./componentTables.css"

export default function() {
    return (
        <div className="welcome">
          <h1>Welcome, to weather app.</h1>
          <br/>
          <LoadWeather/>
          <h4>Click "update" button to get fresh weather.</h4>
          <br/>
        </div>
    );
}
