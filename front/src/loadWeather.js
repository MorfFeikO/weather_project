import React from "react";


export default function LoadWeather(props) {
    let handleOnClick = (e) => {
        props.handleOnClick(e);
        console.log('handledOnClick')
    }

    return (
        <div><button onClick={handleOnClick}>Update weather</button></div>
    );
}
