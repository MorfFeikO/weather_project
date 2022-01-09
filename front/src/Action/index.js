import * as types from "../Constants/index";

function startLoadingWeather() {
    return {
        type: types.START_LOADING_WEATHER
    }
}

function stopLoadingWeather() {
    return {
        type: types.STOP_LOADING_WEATHER
    }
}

function refreshDataWeather(value) {
    return {
        type: types.REFRESH_DATA_WEATHER,
        value
    }
}

export function loadAPIWeather() {
    return (dispatch) => {
        console.log('before fetch weather')
        dispatch(startLoadingWeather());
        fetch(types.GET_WEATHER_URL)
        .then(function(response) {
            return response.json();
        })
        .then(function(json) {
            dispatch(refreshDataWeather(json));
        })
        .then(function() {
            dispatch(stopLoadingWeather());
        })
        .catch(error => {
            throw(error);
        })
    }
}

function startLoadingStatistic() {
    return {
        type: types.START_LOADING_STATISTIC
    }
}

function stopLoadingStatistic() {
    return {
        type: types.STOP_LOADING_STATISTIC
    }
}

function refreshDataStatistic(value) {
    return {
        type: types.REFRESH_DATA_STATISTIC,
        value
    }
}

export function loadAPIStatistic() {
    return (dispatch) => {
        console.log('before fetch statss')
        dispatch(startLoadingStatistic());
        fetch(types.GET_STATISTIC_URL)
        .then(function(response) {
            return response.json();
        })
        .then(function(json) {
            dispatch(refreshDataStatistic(json));
        })
        .then(function() {
            dispatch(stopLoadingStatistic());
        })
        .catch(error => {
            throw(error);
        })
    }
}

// function startLoading() {
//     return {
//         type: types.START_LOADING
//     }
// }

// function stopLoading() {
//     return {
//         type: types.STOP_LOADING
//     }
// }

// export function updateAPIData() {
//     return (dispatch) => {
//         dispatch(startLoading());
//         fetch(types.GET_UPDATE_URL)
//         .then(function() {
//             console.log('i updated data')
//         })
//         .then(function() {;
//             dispatch(loadAPIWeather());
//             dispatch(loadAPIStatistic());
//         })
//         .then(function() {
//             console.log('i guess data have been changed and refreshed');
//         })
//         .then(function() {
//             dispatch(stopLoading());
//         })
//         .catch((error) => {
//             throw(error)
//         })
//     }
// }
