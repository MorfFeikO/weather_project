import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import { StatisticComponent } from "./statistic";

let container = null;

beforeEach(() => {
    container = document.createElement("div");
    document.body.appendChild(container);
});

afterEach(() => {
    unmountComponentAtNode(container);
    container.remove();
    container = null;
})

it("render statisticComponent db with data an empty", () => {
    act(() => {
        let testData = []
        render(<StatisticComponent records={testData}
                                   label1="dbHeader1"
                                   label2="dbHeader2"
                                   label3="dbHeader3"
                                   label4="dbHeader4"
                                   db={true}/>, container);
    });
    expect(container.querySelectorAll("th#head1")[0].innerHTML).toBe("dbHeader1");
    expect(container.querySelectorAll("th#head2")[0].innerHTML).toBe("dbHeader2");
    expect(container.querySelectorAll("th#head3")[0].innerHTML).toBe("dbHeader3");
    expect(container.querySelectorAll("th#head4")[0].innerHTML).toBe("dbHeader4");
});

it("render statisticComponent files with data an empty", () => {
    act(() => {
        let testData = []
        render(<StatisticComponent records={testData}
                                   label1="fileHeader1"
                                   label2="fileHeader2"
                                   label3="fileHeader3"
                                   label4="fileHeader4"
                                   db="false"/>, container);
    });
    expect(container.querySelectorAll("th#head1")[0].innerHTML).toBe("fileHeader1");
    expect(container.querySelectorAll("th#head2")[0].innerHTML).toBe("fileHeader2");
    expect(container.querySelectorAll("th#head3")[0].innerHTML).toBe("fileHeader3");
    expect(container.querySelectorAll("th#head4")[0].innerHTML).toBe("fileHeader4");
});
