import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import { StatisticDBRecord, StatisticFileRecord } from "./statistic";

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

it("render statisticDBRecord", () => {
    act(() => {
        let testData = {
            countryName: "Ukraine",
            recordsCount: "215",
            lastCheckDate: "00:00 15 jan 2022",
            lastCityCheck: "Lviv"
        }
        render(<StatisticDBRecord record={testData}/>, container);
    });
    let testResult = "<tr><th>Ukraine</th><th>215</th><th>00:00 15 jan 2022</th><th>Lviv</th></tr>";
    expect(container.innerHTML).toBe(testResult);
});

it("render statisticFileRecord", () => {
    act(() => {
        let testData = {
            countryName: "Ukraine",
            firstCheckDate: "15 jan 2022",
            lastCheckDate: "16 jan 2022",
            countValue: "16"
        }
        render(<StatisticFileRecord record={testData}/>, container);
    });
    let testResult = "<tr><th>Ukraine</th><th>15 jan 2022</th><th>16 jan 2022</th><th>16</th></tr>";
    expect(container.innerHTML).toBe(testResult);
});
