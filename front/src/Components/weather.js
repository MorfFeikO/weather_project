import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { loadAPIWeather } from "../Action";

export default function WeatherComponent(props) {
    const records = useSelector(state => state.weather.records);
    const dispatch = useDispatch();

    let loadData = () => dispatch(loadAPIWeather());

    useEffect(() => {
        loadData();
    }, []);

    let weatherRecords = records.map((record, index) => {
        return (<WeatherRecord record={record} key={index}/>);
    });
    return (<div>
            <table>
                <thead>
                    <tr>
                        <th>Country</th>
                        <th>City</th>
                        <th>Temperature, C</th>
                        <th>Condition</th>
                    </tr>
                </thead>
                <tbody>
                    {weatherRecords}
                </tbody>
            </table>
        </div>);
}


function WeatherRecord(props) {
    let {record} = props
    return (
        <tr>
            <th>{record.country}</th>
            <th>{record.city}</th>
            <th>{record.temperature}</th>
            <th>{record.condition}</th>
        </tr>
    );
}
