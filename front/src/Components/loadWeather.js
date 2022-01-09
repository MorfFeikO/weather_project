import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { useLocation } from "react-router-dom";
import { loadAPIStatistic, loadAPIWeather, updateAPIData } from "../Action";

const action = {
    "/weather": loadAPIWeather,
    "/statistic": loadAPIStatistic,
}

export default function LoadWeather(props) {
    const dispatch = useDispatch();
    const location = useLocation();
    const updating = useSelector(state => state.updater.loading);

    let handleOnClick = async function(e) {
        e.preventDefault();
        await dispatch(updateAPIData());
        if (location.pathname in Object.keys(action)) {
            let actionFunc = action[location.pathname]
            await dispatch(actionFunc());
        }
    }

    let updateLoading = updating
        ? (<div>Updating data from server</div>)
        : null

    return (
        <div>
            <button onClick={handleOnClick}>Update weather</button>
            <span>{updateLoading}</span>
        </div>
    );
}
