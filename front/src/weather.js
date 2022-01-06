import React, {useState, useEffect} from "react";


const GET_WEATHER_URL = "http://localhost:8004/api/weather"

// const defProp = {
//     records: [
//         {country: "Ukraine", city: "Odessa", temperature: "2", condition: "sunny"},
//         {country: "Ukraine", city: "Lviv", temperature: "23", condition: "rainy"}
//     ]}

export default function WeatherComponent(props) {
    const [records, setRecords] = useState([]);

    useEffect(() => {
        fetch(GET_WEATHER_URL)
        .then(function(response) {
            return response.json();
        })
        .then(function(response) {
            console.log(response);
            setRecords(response);
        })
    }, [])

    let weatherRecords = records.map((record, index) => {
        return (<WeatherRecord record={record} key={index}/>);
    })
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
