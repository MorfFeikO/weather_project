import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import WeatherComponent from "./weather";
import * as redux from "react-redux";

const useSelectorMock = jest.spyOn(redux, "useSelector");
const useDispatchMock = jest.spyOn(redux, "useDispatch");

let container = null;

beforeEach(() => {
    useSelectorMock.mockClear();
    useDispatchMock.mockClear();
    container = document.createElement("div");
    document.body.appendChild(container);
});

afterEach(() => {
    unmountComponentAtNode(container);
    container.remove();
    container = null;
})

it("render weatherComponent empty", () => {
    useSelectorMock.mockReturnValue([])
    const dummyDispatch = jest.fn();
    useDispatchMock.mockReturnValue(dummyDispatch);
    act(() => {
        render(<WeatherComponent/>, container);
    });
    expect(container.querySelector("th#countryHead").innerHTML).toBe("Country");
    expect(container.querySelector("th#cityHead").innerHTML).toBe("City");
    expect(container.querySelector("th#temperatureHead").innerHTML).toBe("Temperature, C");
    expect(container.querySelector("th#conditionHead").innerHTML).toBe("Condition");
});

it("render weatherComponent with data", () => {
    useSelectorMock.mockReturnValue([
        {country: "Ukraine", city: "Lviv", temperature: "23", condition: "rainy"}
    ])
    const dummyDispatch = jest.fn();
    useDispatchMock.mockReturnValue(dummyDispatch);
    act(() => {
        render(<WeatherComponent/>, container);
    });
    let elementTH = container.querySelectorAll("th");
    expect(elementTH[4].innerHTML).toBe("Ukraine");
    expect(elementTH[5].innerHTML).toBe("Lviv");
    expect(elementTH[6].innerHTML).toBe("23");
    expect(elementTH[7].innerHTML).toBe("rainy");
});
