import { combineReducers } from "redux";
import { START_LOADING_WEATHER, STOP_LOADING_WEATHER, REFRESH_DATA_WEATHER, START_LOADING_STATISTIC, STOP_LOADING_STATISTIC, REFRESH_DATA_STATISTIC } from "../Constants";

let weatherRecords = [
    {country: "Ukraine", city: "Odessa", temperature: "2", condition: "sunny"},
    {country: "Ukraine", city: "Lviv", temperature: "23", condition: "rainy"}
]


let statisticRecords = {
    db: [
        {countryName: "Ukraine", recordsCount: "2", lastCheckDate: "00:00 22 nov 2021", lastCityCheck: "Lviv"},
        {countryName: "England", recordsCount: "4", lastCheckDate: "00:00 23 nov 2021", lastCityCheck: "Odessa"}
    ],
    files: [
        {countryName: "China", firstCheckDate: "21 nov 2021", lastCheckDate: "29 nov 2021", countValue: "11"},
        {countryName: "India", firstCheckDate: "25 nov 2021", lastCheckDate: "30 nov 2021", countValue: "54"}
    ]
}

let weatherState = {
    records: [...weatherRecords],
    loading: false
}

let statisticState = {
    records: {...statisticRecords},
    loading: false
}

export function weather(state=weatherState, action) {
    switch (action.type) {
        case START_LOADING_WEATHER:
            return {...state, loading: true}
        case STOP_LOADING_WEATHER:
            return {...state, loading: false}
        case REFRESH_DATA_WEATHER:
            return {...state, records: [...action.value]}
        default:
            return state;
    }
}

export function statistic(state=statisticState, action) {
    switch (action.type) {
        case START_LOADING_STATISTIC:
            return {...state, loading: true}
        case STOP_LOADING_STATISTIC:
            return {...state, loading: false}
        case REFRESH_DATA_STATISTIC:
            return {...state, records: {...action.value}}
        default:
            return state;
    }
}

export const rootReducer = combineReducers({
    weather,
    statistic
})
