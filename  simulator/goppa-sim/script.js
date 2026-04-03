function agLogic() {
    const P = 7; // Finite Field GF(7)
    
    const mod = (n) => ((n % P) + P) % P;

    return {
        points: [],
        message: [1, 2, 1],
        codeword: [],
        received: [],
        errorPos: null,

        init() {
            // Find points on y^2 = x^3 + 2 (mod 7)
            for (let x = 0; x < P; x++) {
                for (let y = 0; y < P; y++) {
                    if (mod(y * y) === mod(x * x * x + 2)) {
                        this.points.push({ x, y });
                    }
                }
            }
            this.calculate();
            this.renderStatic();
            this.renderMathFormulas();
        },

        updateMessage(i, val) {
            let temp = [...this.message];
            temp[i] = mod(parseInt(val) || 0);
            this.message = temp;
            this.calculate();
        },

        calculate() {
            this.codeword = this.points.map(pt => {
                let val = this.message[0] + (this.message[1] * pt.x) + (this.message[2] * pt.y);
                return mod(val);
            });
            this.received = [...this.codeword];
            this.decode();
        },

        toggleError(i) {
            let temp = [...this.received];
            temp[i] = mod(temp[i] + 1);
            this.received = temp;
            this.decode();
        },

        decode() {
            this.errorPos = null;
            for (let i = 0; i < this.received.length; i++) {
                if (this.received[i] !== this.codeword[i]) {
                    this.errorPos = i;
                    break; 
                }
            }
            this.renderDynamic();
        },

        renderStatic() {
            katex.render(`\\mathcal{X}: y^2 \\equiv x^3 + 2 \\pmod 7`, document.getElementById('curve-eq'));
        },

        renderDynamic() {
            const mathBox = document.getElementById('syndrome-math');
            if (!mathBox) return;

            if (this.errorPos === null) {
                katex.render(`\\Delta(P_i) = 0 \\quad \\forall i \\implies \\text{Valid Surface}`, mathBox);
            } else {
                const pt = this.points[this.errorPos];
                katex.render(`\\Delta(P_{${this.errorPos+1}}) \\neq 0 \\implies \\text{Error at } (${pt.x}, ${pt.y})`, mathBox);
            }
        },

        // NEW: Renders the detailed formal mathematics at the bottom of the page
        renderMathFormulas() {
            // Encoding formulas
            const enc1 = `f(x,y) = \\sum_{i=0}^{k-1} m_i \\phi_i(x,y) \\in L(G)`;
            const enc2 = `\\vec{c} = \\Big( f(P_1), f(P_2), \\dots, f(P_n) \\Big)`;
            
            katex.render(enc1, document.getElementById('formal-enc-1'));
            katex.render(enc2, document.getElementById('formal-enc-2'));

            // Decoding formulas
            const dec1 = `\\vec{s} = H \\vec{r}^T = H (\\vec{c} + \\vec{e})^T = H \\vec{e}^T`;
            const dec2 = `\\text{Find } \\sigma(x,y) \\in L(A) \\text{ s.t. } \\sigma(P_j) = 0 \\iff e_j \\neq 0`;

            katex.render(dec1, document.getElementById('formal-dec-1'));
            katex.render(dec2, document.getElementById('formal-dec-2'));
        }
    }
}
