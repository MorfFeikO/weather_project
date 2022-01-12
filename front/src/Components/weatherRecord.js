export default function WeatherRecord(props) {
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
