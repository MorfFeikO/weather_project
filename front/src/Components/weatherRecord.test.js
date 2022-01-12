import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";

import WeatherRecord from "./weatherRecord";

let container = null;

beforeEach(() => {
    container = document.createElement("tbody");
    document.body.appendChild(container);
});

afterEach(() => {
    unmountComponentAtNode(container);
    container.remove();
    container = null;
})

it("render weatherRecord", () => {
    act(() => {
        let testData = {
            country: "Ukraine",
            city: "Lviv",
            temperature: "23.0",
            condition: "sunny"
        }
        render(<WeatherRecord record={testData}/>, container);
    });
    let testResult = "<tr><th>Ukraine</th><th>Lviv</th><th>23.0</th><th>sunny</th></tr>";
    expect(container.innerHTML).toBe(testResult);
});
