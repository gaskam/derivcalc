import { expect, test } from "bun:test";

const filename = "derivcalc.py";

// @ts-ignore
import texte from "./derivcalc.py" with { type: "text" };

import { beforeAll } from "bun:test";

beforeAll(() => {
    texte;
});

test("Parentheses", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("(127)")}`.text()
    ).toStartWith("['127']");
});

test("Addition", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("3+4+(5+6)")}`.text()
    ).toStartWith("['3', '4', '+', '5', '6', '+', '+']");
});

test("Subtraction", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("3-4-(5-6)")}`.text()
    ).toStartWith("['3', '-4', '+', '-1', '5', '-6', '+', '*', '+']");
});

test("Multiplication", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("3*4*(5*6)")}`.text()
    ).toStartWith("['3', '4', '*', '5', '6', '*', '*']");
});

test("Division", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("3/4/(5/6)")}`.text()
    ).toStartWith("['3', '4', '/', '5', '6', '/', '/']");
});

test("Wikipedia", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("(3+4)(5/6)")}`.text()
    ).toStartWith("['3', '4', '+', '5', '6', '/', '*']");
});

test("Exponentiation", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("3^4^(5^6)")}`.text()
    ).toStartWith("['3', '4', '5', '6', '^', '^', '^']");
});

test("Float", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("2.57+3.25^37.1")}`.text()
    ).toStartWith("['2.57', '3.25', '37.1', '^', '+']");
});

test("Negative", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("-3+4(-6+5)")}`.text()
    ).toStartWith("['-3', '4', '-6', '5', '+', '*', '+']");
});

test("Functions", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("(sin(3)+cos(4)*tan(5))/sqrt(6)")}`.text()
    ).toStartWith("['3', 'sin', '4', 'cos', '5', 'tan', '*', '+', '6', 'sqrt', '/']");
});

test("Constants", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("π+e")}`.text()
    ).toStartWith("['�', 'e', '+']");
});

test("Variables", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("a+b(c-d)")}`.text()
    ).toStartWith("['a', 'b', 'c', '-1', 'd', '*', '+', '*', '+']");
});

test("Negatve Variables", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("-a-b(-c+d)")}`.text()
    ).toStartWith("['-1', 'a', '*', '-1', 'b', '*', '-1', 'c', '*', 'd', '+', '*', '+']");
});

test("Complex", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("2π*sqrt(m/k)^(sqrt(1)/-2)")}`.text()
    ).toStartWith("['2', '�', '*', 'm', 'k', '/', 'sqrt', '1', 'sqrt', '-2', '/', '^', '*']");
});

test("Madness", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("(-(x+5))")}`.text()
    ).toStartWith("['-1', 'x', '5', '+', '*']");
});

test("Satan", async () => {
    expect(
        await Bun.$`python3 ${filename} < ${new Response("-16-sqrt(-sin(log((π+e^x)^2)/-5))")}`.text()
    ).toStartWith("['-16', '-1', '-1', '�', 'e', 'x', '^', '+', '2', '^', 'log', '-5', '/', 'sin', '*', 'sqrt', '*', '+']");
});