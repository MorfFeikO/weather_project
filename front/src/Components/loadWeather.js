import React from "react";
import { useDispatch } from "react-redux";
import { updateAPIData } from "../Action";

export default function LoadWeather(props) {
    const dispatch = useDispatch();

    let handleOnClick = (e) => {
        e.preventDefault();
        console.log('handledOnClick');
        dispatch(updateAPIData());
    }

    return (
        <div><button onClick={handleOnClick}>Update weather</button></div>
    );
}
