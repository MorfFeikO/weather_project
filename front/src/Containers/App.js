import React from 'react';
import StatisticsComponents from '../Components/statistic';
import WeatherComponent from '../Components/weather';
import { Switch, Route, Link } from "react-router-dom";
import Nav from "react-bootstrap/Nav";
import { LinkContainer } from "react-router-bootstrap";
import Welcome from '../Components/Welcome';

function App() {
    return (
        <div>
          <Welcome/>
          <Nav justify variant="tabs" defaultActiveKey="/">
            <LinkContainer to="/">
              <Nav.Link>
                Home
              </Nav.Link>
            </LinkContainer>
            <LinkContainer to="/weather">
              <Nav.Link>
                Weather report
              </Nav.Link>
            </LinkContainer>
            <LinkContainer to="/statistic">
              <Nav.Link>Statistic</Nav.Link>
            </LinkContainer>
          </Nav>
          <Switch>
            <Route path="/weather" component={WeatherComponent}/>
            <Route path="/statistic" component={StatisticsComponents}/>
          </Switch>
        </div>
    );
}

export default App;
