import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { loadAPIWeather } from "../Action";
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
                        <th>Country</th>
                        <th>City</th>
                        <th>Temperature, C</th>
                        <th>Condition</th>
                    </tr>
                </thead>
                <tbody className="Tbody">
                    {weatherRecords}
                </tbody>
            </Table>
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
