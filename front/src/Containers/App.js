import React from 'react';
import './App.css';
import StatisticsComponents from '../Components/statistic';
import WeatherComponent from '../Components/weather';
import LoadWeather from '../Components/loadWeather';
import { Switch, Route, Link } from "react-router-dom";

function App() {
    return (
        <div>
          <h1>Welcome, to weather app.</h1>
          <br/>
          <LoadWeather/>
          <ul>
            <li><Link to="/weather">Weather</Link> - to watch weather in cities.</li>
            <li><Link to="/statistic">Statistic</Link> - to watch weather report.</li>
          </ul>
          <Switch>
            <Route path="/weather" component={WeatherComponent}/>
            <Route path="/statistic" component={StatisticsComponents}/>
          </Switch>
        </div>
    );
}

export default App;
