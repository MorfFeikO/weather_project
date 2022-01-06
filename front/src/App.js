import React from 'react';
import './App.css';
import StatiticsComponents from './statistic';
import WeatherComponent from './weather';

function App(props) {
    return (<table>
      <br/>
      <tbody>
        <tr>
          <th><WeatherComponent/></th>
          <th><StatiticsComponents/></th>
        </tr>
      </tbody>
      </table>);


}

export default App;
