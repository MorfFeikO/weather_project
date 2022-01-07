import React from "react";
import { useDispatch } from "react-redux";
import { loadAPIData } from "../Action";
import { GET_STATISTIC_URL, GET_WEATHER_URL } from "../Constants";


export default function LoadWeather(props) {
    const dispatch = useDispatch();

    let handleOnClick = (e) => {
        e.preventDefault();
        console.log('handledOnClick');
        dispatch(loadAPIData(GET_WEATHER_URL));
        dispatch(loadAPIData(GET_STATISTIC_URL));
    }

    return (
        <div><button onClick={handleOnClick}>Update weather</button></div>
    );
}
