import React from 'react';
import ReactDOM from 'react-dom';
import App from './Containers/App';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Provider } from "react-redux";
import { BrowserRouter } from 'react-router-dom';
import configureStore from "./Store/index";

const store = configureStore();

ReactDOM.render(
  <Provider store={store}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </Provider>,
  document.getElementById('root')
);
