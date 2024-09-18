import { expect, test, beforeAll, describe } from "bun:test";

const filename = "derivcalc.py";

// @ts-ignore
import text from "./derivcalc.py" with { type: "text" };

beforeAll(() => {
    text;
});

async function runTest(input: string): Promise<{ rpn: string, rpnDerivat: string, derivative: string }> {
    const output = await Bun.$`echo "${input}" | python3 ${filename}`.text();

    const rpnMatch = output.match(/RPN: (.+)/);
    const rpnDerivatMatch = output.match(/RPNderivat: (.+)/);
    const derivativeMatch = output.match(/Derivative: (.+)/);

    // if (!rpnMatch || !derivativeMatch) {
    //     throw new Error("Couldn't find expected output");
    // }

    return {
        rpn: rpnMatch ? rpnMatch[1].trim() : "",
        rpnDerivat: rpnDerivatMatch ? rpnDerivatMatch[1].trim() : "",
        derivative: derivativeMatch ? derivativeMatch[1].trim() : ""
    };
}

describe("Parentheses", async () => {
    const result = await runTest("(127)");
    test("RPN", async () => {
        expect(result.rpn).toBe("['127']");
    });
    test("RPNderivat", async () => {
        expect(result.rpnDerivat).toBe("['0']");
    });
    test("Derivative", async () => {
        expect(result.derivative).toBe("0");
    });
});

describe("Subtraction", async () => {
    const result = await runTest("3-4-(5-6)");
    test("RPN", async () => {
        expect(result.rpn).toBe("['3', '-4', '+', '-1', '5', '-6', '+', '*', '+']");
    });
    test("RPNderivat", async () => {
        expect(result.rpnDerivat).toBe("['0']");
    });
    test.todo("Derivative", async () => {
        expect(result.derivative).toBe("0");
    });
});

describe("Multiplication", async () => {
    const result = await runTest("3*4*(5*6)");
    test("RPN", async () => {
        expect(result.rpn).toBe("['3', '4', '*', '5', '6', '*', '*']");
    });
    test("RPNderivat", async () => {
        expect(result.rpnDerivat).toBe("['0']");
    });
    test.todo("Derivative", async () => {
        expect(result.derivative).toBe("0");
    });
});

describe("Division", async () => {
    const result = await runTest("3/4/(5/6)");
    test("RPN", async () => {
        expect(result.rpn).toBe("['3', '4', '/', '5', '6', '/', '/']");
    });
    test("RPNderivat", async () => {
        expect(result.rpnDerivat).toBe("['0']");
    });
    test.todo("Derivative", async () => {
        expect(result.derivative).toBe("0");
    });
});

describe("Wikipedia", async () => {
    const result = await runTest("(3+4)(5/6)");
    test("RPN", async () => {
        expect(result.rpn).toBe("['3', '4', '+', '5', '6', '/', '*']");
    });
    test("RPNderivat", async () => {
        expect(result.rpnDerivat).toBe("['0']");
    });
    test.todo("Derivative", async () => {
        expect(result.derivative).toBe("0");
    });
});

describe("Exponentiation", async () => {
    const result = await runTest("3^4^(5^6)");
    test("RPN", async () => {
        expect(result.rpn).toBe("['3', '4', '5', '6', '^', '^', '^']");
    });
    test("RPNderivat", async () => {
        expect(result.rpnDerivat).toBe("['0']");
    });
    test.todo("Derivative", async () => {
        expect(result.derivative).toBe("0");
    });
});

describe("Float", async () => {
    const result = await runTest("2.57+3.25^37.1");
    test("RPN", async () => {
        expect(result.rpn).toBe("['2.57', '3.25', '37.1', '^', '+']");
    });
    test("RPNderivat", async () => {
        expect(result.rpnDerivat).toBe("['0']");
    });
    test.todo("Derivative", async () => {
        expect(result.derivative).toBe("0");
    });
});

describe("Negative", async () => {
    const result = await runTest("-3+4(-6+5)");
    test("RPN", async () => {
        expect(result.rpn).toBe("['-3', '4', '-6', '5', '+', '*', '+']");
    });
    test("RPNderivat", async () => {
        expect(result.rpnDerivat).toBe("['0']");
    });
    test.todo("Derivative", async () => {
        expect(result.derivative).toBe("0");
    });
});

describe("Function", async () => {
    const result = await runTest("(sin(3)+cos(4)*tan(5))/sqrt(6)");
    test("RPN", async () => {
        expect(result.rpn).toBe("['3', 'sin', '4', 'cos', '5', 'tan', '*', '+', '6', 'sqrt', '/']");
    });
    test("RPNderivat", async () => {
        expect(result.rpnDerivat).toBe("['0']");
    });
    test.todo("Derivative", async () => {
        expect(result.derivative).toBe("0");
    });
});

describe("Constants", async () => {
    const result = await runTest("π+e");
    test("RPN", async () => {
        expect(result.rpn).toBe("['�', 'e', '+']");
    });
    test("RPNderivat", async () => {
        expect(result.rpnDerivat).toBe("['0']");
    });
    test("Derivative", async () => {
        expect(result.derivative).toBe("0");
    });
});

describe("Variables", async () => {
    const result = await runTest("a+b(c-d)");
    test("RPN", async () => {
        expect(result.rpn).toBe("['a', 'b', 'c', '-1', 'd', '*', '+', '*', '+']");
    });
    test("RPNderivat", async () => {
        expect(result.rpnDerivat).toBe("['0']");
    });
    test.todo("Derivative", async () => {
        expect(result.derivative).toBe("0");
    });
});

describe("Negative Variables", async () => {
    const result = await runTest("-a-b(-c+d)");
    test("RPN", async () => {
        expect(result.rpn).toBe("['-1', 'a', '*', '-1', 'b', '*', '-1', 'c', '*', 'd', '+', '*', '+']");
    });
    test("RPNderivat", async () => {
        expect(result.rpnDerivat).toBe("['0']");
    });
    test.todo("Derivative", async () => {
        expect(result.derivative).toBe("0");
    });
});

describe("Complex", async () => {
    const result = await runTest("2π*sqrt(m/k)^(sqrt(1)/-2)");
    test("RPN", async () => {
        expect(result.rpn).toBe("['2', '�', '*', 'm', 'k', '/', 'sqrt', '1', 'sqrt', '-2', '/', '^', '*']");
    });
    test("RPNderivat", async () => {
        expect(result.rpnDerivat).toBe("['0']");
    });
    test.todo("Derivative", async () => {
        expect(result.derivative).toBe("0");
    });
});

describe("Madness", async () => {
    const result = await runTest("(-(x+5))");
    test("RPN", async () => {
        expect(result.rpn).toBe("['-1', 'x', '5', '+', '*']");
    });
    test("RPNderivat", async () => {
        expect(result.rpnDerivat).toBe("['-1']");
    });
    test("Derivative", async () => {
        expect(result.derivative).toBe("-1");
    });
});

describe("Satan", async () => {
    const result = await runTest("-16-sqrt(-sin(log((π+e^x)^2)/-5))");
    test("RPN", async () => {
        expect(result.rpn).toBe("['-16', '-1', '-1', '�', 'e', 'x', '^', '+', '2', '^', 'log', '-5', '/', 'sin', '*', 'sqrt', '*', '+']");
    });
    test.todo("RPNderivat", async () => {
        expect(result.rpnDerivat).toBe("['']")
    });
    test.todo("Derivative", async () => {
        expect(result.derivative).toBe("-(e^x * cos((2 * ln(e^x + π)) / 5)) / (5 * (e^x + π) * sqrt(sin((2 * ln(e^x + π)) / 5)))");
    });
});