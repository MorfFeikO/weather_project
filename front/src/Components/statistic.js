import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { loadAPIStatistic } from "../Action";
import Table from "react-bootstrap/Table";
import "./componentTables.css";

export default function StatisticsComponents(props) {
    const records = useSelector(state => state.statistic.records);
    const dispatch = useDispatch();

    let loadData = () => dispatch(loadAPIStatistic());

    useEffect(() => {
        loadData();
    }, [])

    let dbRecords = records.db;
    let filesRecords = records.files;
    return (
    <div>
        <StatisticComponent records={dbRecords}
                            label1="Country"
                            label2="Weather records"
                            label3="Last weather check"
                            label4="Last city in a row"
                            db={true}/>
        <br/>
        <StatisticComponent records={filesRecords}
                            label1="Country"
                            label2="First weather check"
                            label3="Last weather check"
                            label4="Number of files"
                            db={false}/>
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
            <Table striped bordered hover className="Statistic-table">
                <thead className="Theader">
                    <tr>
                        <th id="head1">{label1}</th>
                        <th id="head2">{label2}</th>
                        <th id="head3">{label3}</th>
                        <th id="head4">{label4}</th>
                    </tr>
                </thead>
                <tbody className="Tbody">
                    {weatherRecords}
                </tbody>
            </Table>
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

export { StatisticDBRecord, StatisticFileRecord, StatisticComponent };
