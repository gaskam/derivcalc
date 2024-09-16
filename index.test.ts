import { expect, test, beforeAll } from "bun:test";

const filename = "derivcalc.py";

// @ts-ignore
import texte from "./derivcalc.py" with { type: "text" };

beforeAll(() => {
    texte;
});

async function runTest(input: string): Promise<{ rpn: string, derivative: string }> {
    const output = await Bun.$`echo "${input}" | python3 ${filename}`.text();

    const rpnMatch = output.match(/RPN: (.+)/);
    const derivativeMatch = output.match(/Derivative: (.+)/);

    if (!rpnMatch || !derivativeMatch) {
        throw new Error("Couldn't find expected output");
    }

    return {
        rpn: rpnMatch[1].trim(),
        derivative: derivativeMatch[1].trim()
    };
}

test("Parentheses", async () => {
    const result = await runTest("(127)");
    expect(result.rpn).toBe("['127']");
    expect(result.derivative).toBe("0");
});

test("Addition", async () => {
    const result = await runTest("3+4+(5+6)");
    expect(result.rpn).toBe("['3', '4', '+', '5', '6', '+', '+']");
    expect(result.derivative).toBe("0");
});

test.todo("Subtraction", async () => {
    const result = await runTest("3-4-(5-6)");
    expect(result.rpn).toBe("['3', '-4', '+', '-1', '5', '-6', '+', '*', '+']");
    expect(result.derivative).toBe("0");
});

test.todo("Multiplication", async () => {
    const result = await runTest("3*4*(5*6)");
    expect(result.rpn).toBe("['3', '4', '*', '5', '6', '*', '*']");
    expect(result.derivative).toBe("0");
});

test.todo("Division", async () => {
    const result = await runTest("3/4/(5/6)");
    expect(result.rpn).toBe("['3', '4', '/', '5', '6', '/', '/']");
    expect(result.derivative).toBe("0");
});

test.todo("Wikipedia", async () => {
    const result = await runTest("(3+4)(5/6)");
    expect(result.rpn).toBe("['3', '4', '+', '5', '6', '/', '*']");
    expect(result.derivative).toBe("0");
});

test.todo("Exponentiation", async () => {
    const result = await runTest("3^4^(5^6)");
    expect(result.rpn).toBe("['3', '4', '5', '6', '^', '^', '^']");
    expect(result.derivative).toBe("0");
});

test.todo("Float", async () => {
    const result = await runTest("2.57+3.25^37.1");
    expect(result.rpn).toBe("['2.57', '3.25', '37.1', '^', '+']");
    expect(result.derivative).toBe("0");
});

test.todo("Negative", async () => {
    const result = await runTest("-3+4(-6+5)");
    expect(result.rpn).toBe("['-3', '4', '-6', '5', '+', '*', '+']");
    expect(result.derivative).toBe("0");
});

test.todo("Function", async () => {
    const result = await runTest("(sin(3)+cos(4)*tan(5))/sqrt(6)");
    expect(result.rpn).toBe("['3', 'sin', '4', 'cos', '5', 'tan', '*', '+', '6', 'sqrt', '/']");
    expect(result.derivative).toBe("0");
});

test("Constants", async () => {
    const result = await runTest("π+e");
    expect(result.rpn).toBe("['�', 'e', '+']");
    expect(result.derivative).toBe("0");
});

test.todo("Variables", async () => {
    const result = await runTest("a+b(c-d)");
    expect(result.rpn).toBe("['a', 'b', 'c', '-1', 'd', '*', '+', '*', '+']");
    expect(result.derivative).toBe("0");
});

test.todo("Negative Variables", async () => {
    const result = await runTest("-a-b(-c+d)");
    expect(result.rpn).toBe("['-1', 'a', '*', '-1', 'b', '*', '-1', 'c', '*', 'd', '+', '*', '+']");
    expect(result.derivative).toBe("0");
});

test.todo("Complex", async () => {
    const result = await runTest("2π*sqrt(m/k)^(sqrt(1)/-2)");
    expect(result.rpn).toBe("['2', '�', '*', 'm', 'k', '/', 'sqrt', '1', 'sqrt', '-2', '/', '^', '*']");
    expect(result.derivative).toBe("0");
});

test("Madness", async () => {
    const result = await runTest("(-(x+5))");
    expect(result.rpn).toBe("['-1', 'x', '5', '+', '*']");
    expect(result.derivative).toBe("-1");
});

test("Satan", async () => {
    const result = await runTest("-16-sqrt(-sin(log((π+e^x)^2)/-5))");
    expect(result.rpn).toBe("['-16', '-1', '-1', '�', 'e', 'x', '^', '+', '2', '^', 'log', '-5', '/', 'sin', '*', 'sqrt', '*', '+']");
    expect(result.derivative).toBe("-(e^x * cos((2 * ln(e^x + �)) / 5)) / (5 * (e^x + �) * sqrt(sin((2 * ln(e^x + �)) / 5)))");
});
