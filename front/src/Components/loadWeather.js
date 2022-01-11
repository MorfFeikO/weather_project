import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { useLocation } from "react-router-dom";
import { updateAPIData } from "../Action";
import Spinner from "react-bootstrap/Spinner";
import Button from "react-bootstrap/Button";

export default function LoadWeather(props) {
    const dispatch = useDispatch();
    const location = useLocation();
    const updating = useSelector(state => state.updater.loading);

    let handleOnClick = function(e) {
        e.preventDefault();
        dispatch(updateAPIData(location.pathname));
    }

    let updateLoading = updating
        ? (<span><Spinner animation="border"/></span>)
        : null

    return (
        <div>
            <Button variant="info" onClick={handleOnClick}>Update weather</Button>
            {updateLoading}
        </div>
    );
}
