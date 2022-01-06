import React, {useState, useEffect} from "react";


const GET_STATISTIC_URL = "http://localhost:8004/api/statistic"

// let defProp = {
//     db: [
//         {countryName: "Ukraine", recordsCount: "2", lastCheckDate: "00:00 22 nov 2021", lastCityCheck: "Lviv"},
//         {countryName: "England", recordsCount: "4", lastCheckDate: "00:00 23 nov 2021", lastCityCheck: "Odessa"}
//     ],
//     files: [
//         {countryName: "China", firstCheckDate: "21 nov 2021", lastCheckDate: "29 nov 2021", countValue: "11"},
//         {countryName: "India", firstCheckDate: "25 nov 2021", lastCheckDate: "30 nov 2021", countValue: "54"}
//     ]
// }


export default function StatiticsComponents(props) {
    const [dbRecords, setDBRecords] = useState([]);
    const [filesRecords, setFilesRecords] = useState([]);

    useEffect(() => {
        fetch(GET_STATISTIC_URL)
        .then(function(response) {
            return response.json();
        })
        .then(function(response) {
            console.log(response);
            setDBRecords(response.db);
            setFilesRecords(response.files)
        })
    }, [])

    // useEffect(() => {
    //     setDbRecords(defProp.db);
    //     setFilesRecords(defProp.files);
    // })

    return (
    <div>
        <StatisticComponent records={dbRecords} label1="Country"
                                                label2="Weather records"
                                                label3="Last weather check"
                                                label4="Last city in a row"
                                                db={true}/>
        <br/>
        <StatisticComponent records={filesRecords} label1="Country"
                                                   label2="First weather check"
                                                   label3="Last weather check"
                                                   label4="Number of files"
                                                   files={true}/>
    </div>);
}


function StatisticComponent(props) {
    let {records, db, label1, label2, label3, label4} = props
    let weatherRecords = records.map((record, index) => {
        if (db) {
            return (<StatisticDBRecord record={record} key={index}/>);
        } else {
            return (<StatisticFileRecord record={record} key={index}/>);
        }
    })
    return (<div>
            <table>
                <thead>
                    <tr>
                        <th>{label1}</th>
                        <th>{label2}</th>
                        <th>{label3}</th>
                        <th>{label4}</th>
                    </tr>
                </thead>
                <tbody>
                    {weatherRecords}
                </tbody>
            </table>
        </div>);
}


function StatisticDBRecord(props) {
    let {record} = props
    return (<tr>
                <th>{record.countryName}</th>
                <th>{record.recordsCount}</th>
                <th>{record.lastCheckDate}</th>
                <th>{record.lastCityCheck}</th>
            </tr>);
}


function StatisticFileRecord(props) {
    let {record} = props
    return (<tr>
                <th>{record.countryName}</th>
                <th>{record.firstCheckDate}</th>
                <th>{record.lastCheckDate}</th>
                <th>{record.countValue}</th>
            </tr>);
}

// defprop = fetch("GET_WEATHER_URL")
//             .then(function(response) {
//                 return response.json()
//             })
