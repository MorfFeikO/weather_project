import React from 'react';
import './App.css';
import StatisticsComponents from '../Components/statistic';
import WeatherComponent from '../Components/weather';
import LoadWeather from '../Components/loadWeather';

function App() {
    return (<table>

      <br/>
      <tbody>
        <tr>
          <th><WeatherComponent/></th>
          <th><StatisticsComponents/></th>
        </tr>
      </tbody>
      </table>);


}

export default App;
