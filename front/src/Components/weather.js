import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { loadAPIWeather } from "../Action";
import WeatherRecord from "./weatherRecord";
import Table from "react-bootstrap/Table";
import "./componentTables.css";

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
    return (<div className="Weather-table">
            <Table striped bordered hover className="Weather-table">
                <thead className="Theader">
                    <tr>
                        <th id="countryHead">Country</th>
                        <th id="cityHead">City</th>
                        <th id="temperatureHead">Temperature, C</th>
                        <th id="conditionHead">Condition</th>
                    </tr>
                </thead>
                <tbody className="Tbody">
                    {weatherRecords}
                </tbody>
            </Table>
        </div>);
}
