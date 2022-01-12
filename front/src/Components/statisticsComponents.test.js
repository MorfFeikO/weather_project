import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import StatisticsComponents from "./statistic";
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

it("render statisticsComponent empty", () => {
    useSelectorMock.mockReturnValue({db: [], files: []})
    useDispatchMock.mockReturnValue(jest.fn());
    act(() => {
        render(<StatisticsComponents/>, container);
    });
    expect(container.querySelectorAll("th#head1")[0].innerHTML).toBe("Country");
    expect(container.querySelectorAll("th#head1")[1].innerHTML).toBe("Country");
    expect(container.querySelectorAll("th#head2")[0].innerHTML).toBe("Weather records");
    expect(container.querySelectorAll("th#head2")[1].innerHTML).toBe("First weather check");
    expect(container.querySelectorAll("th#head3")[0].innerHTML).toBe("Last weather check");
    expect(container.querySelectorAll("th#head3")[1].innerHTML).toBe("Last weather check");
    expect(container.querySelectorAll("th#head4")[0].innerHTML).toBe("Last city in a row");
    expect(container.querySelectorAll("th#head4")[1].innerHTML).toBe("Number of files");

});
