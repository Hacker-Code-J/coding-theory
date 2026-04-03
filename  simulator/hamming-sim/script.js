function hammingLogic() {
    return {
        dataVec: [1, 0, 1, 1],
        codewordVec: [],
        receivedVec: [],
        syndromeVec: [0, 0, 0],
        
        // G = [I | P]
        G: [
            [1, 0, 0, 0, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1]
        ],
        
        // H = [P^T | I]
        H: [
            [1, 1, 0, 1, 1, 0, 0],
            [1, 0, 1, 1, 0, 1, 0],
            [0, 1, 1, 1, 0, 0, 1]
        ],

        init() {
            this.calculate();
            this.renderStatic();
        },

        toggleData(i) {
            this.dataVec[i] = this.dataVec[i] === 1 ? 0 : 1;
            this.calculate();
        },

        toggleError(i) {
            this.receivedVec[i] = this.receivedVec[i] === 1 ? 0 : 1;
            this.updateSyndrome();
        },

        calculate() {
            // Encode: c = d * G over GF(2)
            this.codewordVec = this.G[0].map((_, col) => 
                this.dataVec.reduce((acc, bit, row) => acc ^ (bit & this.G[row][col]), 0)
            );
            this.receivedVec = [...this.codewordVec];
            this.updateSyndrome();
        },

        updateSyndrome() {
            // Syndrome: s = H * r^T
            this.syndromeVec = this.H.map(row => 
                row.reduce((acc, hVal, i) => acc ^ (hVal & this.receivedVec[i]), 0)
            );
            this.renderDynamic();
        },

        get syndromeSum() { return this.syndromeVec.reduce((a, b) => a + b, 0); },

        get errorPos() {
            if (this.syndromeSum === 0) return 0;
            for (let col = 0; col < 7; col++) {
                if (this.H.every((row, rowIndex) => row[col] === this.syndromeVec[rowIndex])) {
                    return col + 1;
                }
            }
            return "Multi";
        },

        getLabel(i) { return [0, 1, 2, 3].includes(i) ? 'Data' : 'Parity'; },
        isError(i) { return this.receivedVec[i] !== this.codewordVec[i]; },

        renderStatic() {
            katex.render(`G = \\begin{pmatrix} ${this.G.map(r => r.join('&')).join('\\\\')} \\end{pmatrix}`, document.getElementById('g-matrix'));
            katex.render(`H = \\begin{pmatrix} ${this.H.map(r => r.join('&')).join('\\\\')} \\end{pmatrix}`, document.getElementById('h-matrix'));
        },

        renderDynamic() {
            const dStr = `\\vec{d}=[${this.dataVec.join(',')}]`;
            const cStr = `\\vec{c}=[${this.codewordVec.join(',')}]`;
            const sStr = `\\vec{s}=[${this.syndromeVec.join(',')}]^T`;
            
            katex.render(`${dStr} \\cdot G = ${cStr}`, document.getElementById('enc-formula'));
            katex.render(`H \\cdot \\vec{r}^T = ${sStr}`, document.getElementById('dec-formula'));
        }
    }
}
