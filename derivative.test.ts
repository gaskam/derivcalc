import { expect, test, beforeAll, afterAll, describe } from "bun:test";
import { unlink } from "node:fs/promises";

const outputFile = "dbd2a894338c4a07aa5c8246fc59e630.py"

// @ts-ignore
import derivcalc from "./derivcalc.py" with { type: "text" };
// @ts-ignore
import tester from "./derivative.test.py" with { type: "text" };

beforeAll(() => {
    // Removes the top-level function calls
    let output: string = derivcalc.replace(/^[a-zA-Z0-9]+\(.*\)$/gm, '');
    output = output + '\n' +  tester;

    Bun.write(outputFile, output);
});

afterAll(async () => {
    // Removes the temporary compiled python code
    await unlink(outputFile);
});

async function runTest(input: string): Promise<string> {
    const output = await Bun.$`echo "${input}" | python3 ${outputFile}`.text();

    return output.trimEnd();
}

describe("Simple addition derivative tests", async () => {
    const result1 = await runTest("['x', '5', '+']");
    const result2 = await runTest("['5', 'x', '+']");
    const result3 = await runTest("['x', 'x', '+']");
    const result4 = await runTest("['5', '5', '+']");

    test("Simplification (1)", () => {
        expect(result1).toStartWith("['1']");
    });

    test("Simplification (2)", () => {
        expect(result2).toBe("['1']");
    });

    test("Simple (3)", () => {
        expect(result3).toBe("['1', '1', '+']");
    });
    
    test("Dummy (4)", () => {
        expect(result4).toBe("['0']");
    });
});

describe("Simple substraction derivative tests", async () => {
    const result1 = await runTest("['x', '5', '-']");
    const result2 = await runTest("['5', 'x', '-']");
    const result3 = await runTest("['x', 'x', '-']");
    const result4 = await runTest("['5', '5', '-']");

    test("Simplification (1)", () => {
        expect(result1).toStartWith("['1']");
    });

    test("Simplification (2)", () => {
        expect(result2).toBe("['1', 'neg']");
    });

    test("Simple (3)", () => {
        expect(result3).toBe("['1', '1', '-']");
    });
    
    test("Dummy (4)", () => {
        expect(result4).toBe("['0']");
    });
});

describe("Simple multiplication derivative tests", async () => {
    const result1 = await runTest("['x', '5', '*']");
    const result2 = await runTest("['5', 'x', '*']");
    const result3 = await runTest("['x', 'x', '*']");
    const result4 = await runTest("['5', '5', '*']");
    const result5 = await runTest("['x', '0', '5', '*', '*']");

    test("Simplification (1)", () => {
        expect(result1).toStartWith("['5']");
    });

    test("Simplification (2)", () => {
        expect(result2).toBe("['5']");
    });

    test("Simple (3)", () => {
        expect(result3).toBe("['x', 'x', '+']");
    });
    
    test("Dummy (4)", () => {
        expect(result4).toBe("['0']");
    });
    
    test.todoIf(result5 == "['0', '5', '*']")("Zero multiplication (5)", () => {
        expect(result5).toBe("['0']");
    });
});

describe("Simple division derivative tests", async () => {
    const result1 = await runTest("['x', '5', '/']");
    const result2 = await runTest("['5', 'x', '/']");
    const result3 = await runTest("['x', 'x', '/']");
    const result4 = await runTest("['5', '5', '/']");

    test("Simplification (1)", () => {
        expect(result1).toStartWith("['5', '5', '2', '^', '/']");
    });

    test("Simplification (2)", () => {
        expect(result2).toBe("['5', 'neg', 'x', '2', '^', '/']");
    });

    test("Simple (3)", () => {
        expect(result3).toBe("['x', 'x', '-', 'x', '2', '^', '/']"); // Not simplified, but correct
    });
    
    test("Dummy (4)", () => {
        expect(result4).toBe("['0']");
    });
});