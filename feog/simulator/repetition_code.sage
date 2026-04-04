# ============================================================
# Repetition Code Simulator (Terminal Menu Version) in SageMath
# With PNG/PDF plot export
# ============================================================

from random import random, randint

class RepetitionCodeSimulator:
    def __init__(self, n):
        if n <= 0:
            raise ValueError("n must be a positive integer.")
        if n % 2 == 0:
            raise ValueError("For unique majority decoding, n must be odd.")
        self.n = ZZ(n)
        self.k = ZZ(1)
        self.F = GF(2)
        self.t = (self.n - 1) // 2

    def _check_bit(self, b):
        if int(b) not in [0, 1]:
            raise ValueError("Bit must be 0 or 1.")

    def _check_probability(self, p):
        if p < 0 or p > 1:
            raise ValueError("Probability p must satisfy 0 <= p <= 1.")

    def _to_vector(self, word):
        if len(word) != self.n:
            raise ValueError(f"Word must have length {self.n}.")
        cleaned = []
        for x in word:
            if int(x) not in [0, 1]:
                raise ValueError("All entries must be binary.")
            cleaned.append(int(x))
        return vector(self.F, cleaned)

    def encode_bit(self, b):
        self._check_bit(b)
        b = int(b)
        return vector(self.F, [b] * self.n)

    def random_error_vector(self, p):
        self._check_probability(p)
        return vector(self.F, [1 if random() < p else 0 for _ in range(self.n)])

    def transmit(self, codeword, p):
        c = self._to_vector(codeword)
        e = self.random_error_vector(p)
        y = c + e
        return y, e

    def decode_word(self, received_word):
        y = self._to_vector(received_word)
        ones = sum(ZZ(int(a)) for a in y)
        zeros = self.n - ones
        return 1 if ones > zeros else 0

    def hamming_weight(self, v):
        v = self._to_vector(v)
        return sum(ZZ(int(a)) for a in v)

    def theoretical_block_error_probability(self, p):
        self._check_probability(p)
        total = 0
        for i in range(self.t + 1, self.n + 1):
            total += binomial(self.n, i) * (p**i) * ((1 - p)**(self.n - i))
        return RR(total)

    def demo_single_trial(self, bit=None, p=0.1):
        self._check_probability(p)
        if bit is None:
            bit = randint(0, 1)
        self._check_bit(bit)
        c = self.encode_bit(bit)
        y, e = self.transmit(c, p)
        b_hat = self.decode_word(y)
        success = (b_hat == int(bit))
        print("========================================")
        print(" Repetition Code Single Trial")
        print("========================================")
        print(f"Code parameters: (n,k)=({self.n},{self.k})")
        print(f"Error-correcting capability: t = {self.t}")
        print(f"Sent bit:            {int(bit)}")
        print(f"Encoded codeword:    {list(c)}")
        print(f"Error vector:        {list(e)}")
        print(f"Received word:       {list(y)}")
        print(f"Decoded bit:         {b_hat}")
        print(f"Hamming weight(e):   {self.hamming_weight(e)}")
        print(f"Success:             {success}")
        print("========================================")

    def simulate(self, bit=None, p=0.1, trials=1000, verbose=False):
        self._check_probability(p)
        if trials <= 0:
            raise ValueError("trials must be a positive integer.")

        errors = 0
        total_channel_flips = 0

        for _ in range(trials):
            b = randint(0, 1) if bit is None else int(bit)
            c = self.encode_bit(b)
            y, e = self.transmit(c, p)
            b_hat = self.decode_word(y)
            total_channel_flips += self.hamming_weight(e)
            if b_hat != b:
                errors += 1

        empirical_block_error_rate = RR(errors) / RR(trials)
        theoretical_error = self.theoretical_block_error_probability(p)
        result = {
            "empirical_block_error_rate": empirical_block_error_rate,
            "theoretical_block_error_rate": theoretical_error,
            "absolute_error_gap": abs(empirical_block_error_rate - theoretical_error),
            "average_channel_flips": RR(total_channel_flips) / RR(trials),
        }

        if verbose:
            print("========================================")
            print(" Repetition Code Monte Carlo Simulation")
            print("========================================")
            print(f"Code parameters:                 (n,k)=({self.n},{self.k})")
            print(f"Correction radius:               t = {self.t}")
            print(f"Channel crossover probability:   p = {RR(p)}")
            print(f"Trials:                          {trials}")
            print(f"Average channel flips/trial:     {result['average_channel_flips']}")
            print(f"Empirical block error rate:      {result['empirical_block_error_rate']}")
            print(f"Theoretical block error rate:    {result['theoretical_block_error_rate']}")
            print(f"Absolute gap:                    {result['absolute_error_gap']}")
            print("========================================")
        return result

    def compare_with_theory(self, bit=None, p=0.1, trials=10000):
        result = self.simulate(bit=bit, p=p, trials=trials, verbose=False)
        print("========================================")
        print(" Theory vs Simulation")
        print("========================================")
        print(f"n = {self.n}, k = {self.k}, t = {self.t}")
        print(f"p = {RR(p)}, trials = {ZZ(trials)}")
        mode = "random bits" if bit is None else f"fixed bit = {int(bit)}"
        print(f"Mode:                  {mode}")
        print(f"Empirical BER(block):  {result['empirical_block_error_rate']}")
        print(f"Theoretical BER(block):{result['theoretical_block_error_rate']}")
        print(f"Absolute gap:          {result['absolute_error_gap']}")
        print("========================================")

    def transmit_message(self, bits, p=0.1, verbose=True):
        decoded = []
        records = []
        for b in bits:
            c = self.encode_bit(b)
            y, e = self.transmit(c, p)
            b_hat = self.decode_word(y)
            decoded.append(b_hat)
            records.append((int(b), list(c), list(e), list(y), b_hat))

        if verbose:
            print("========================================")
            print(" Message Transmission Demo")
            print("========================================")
            print(f"n = {self.n}, p = {RR(p)}, t = {self.t}")
            for i, rec in enumerate(records, start=1):
                b, c, e, y, bhat = rec
                print(f"{i:2d}. bit={b}, codeword={c}, error={e}, received={y}, decoded={bhat}")
            print("----------------------------------------")
            print(f"Original message: {list(map(int, bits))}")
            print(f"Decoded message:  {decoded}")
            print(f"Successful:       {decoded == list(map(int, bits))}")
            print("========================================")

    def plot_theory(self, p_values):
        pts = [(RR(p), self.theoretical_block_error_probability(p)) for p in p_values]
        line_graph = list_plot(
            pts, plotjoined=True, thickness=2,
            axes_labels=[r"$p$", r"$P_{\mathrm{block\ error}}$"],
            title=f"Theoretical block error probability for repetition code n={self.n}"
        )
        point_graph = list_plot(pts, plotjoined=False, marker='o', size=25)
        return line_graph + point_graph

    @staticmethod
    def plot_multiple_theory(n_values, p_values):
        G = Graphics()
        for n in n_values:
            sim = RepetitionCodeSimulator(int(n))
            pts = [(RR(p), sim.theoretical_block_error_probability(p)) for p in p_values]
            G += list_plot(pts, plotjoined=True, thickness=2, legend_label=f"n={n}")
        G.axes_labels([r"$p$", r"$P_{\mathrm{block\ error}}$"])
        G.set_legend_options(loc='upper left')
        return G

    @staticmethod
    def comparison_table(n_values, p=0.1, trials=5000):
        rows = []
        for n in n_values:
            sim = RepetitionCodeSimulator(int(n))
            result = sim.simulate(bit=None, p=p, trials=trials, verbose=False)
            rows.append([sim.n, sim.t, RR(p), result["empirical_block_error_rate"],
                         result["theoretical_block_error_rate"], result["absolute_error_gap"]])
        header = ["n", "t", "p", "empirical block error", "theoretical block error", "absolute gap"]
        return table(rows=rows, header_row=header)

def save_plot_both(G, base_name):
    png_name = f"{base_name}.png"
    pdf_name = f"{base_name}.pdf"
    G.save(png_name)
    G.save(pdf_name)
    print(f"Saved {png_name}")
    print(f"Saved {pdf_name}")

def ask_save_plot(G, default_base="plot"):
    raw = input(f"Save plot as PNG and PDF? [y/N]: ").strip().lower()
    if raw == "y":
        base = input(f"Base filename without extension [default {default_base}]: ").strip()
        if base == "":
            base = default_base
        save_plot_both(G, base)

def read_odd_n(default=5):
    raw = input(f"Enter odd repetition length n [default {default}]: ").strip()
    if raw == "":
        return ZZ(default)
    n = ZZ(raw)
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be a positive odd integer.")
    return n

def read_probability(default=0.2):
    raw = input(f"Enter channel crossover probability p in [0,1] [default {default}]: ").strip()
    if raw == "":
        return RR(default)
    p = RR(raw)
    if p < 0 or p > 1:
        raise ValueError("p must satisfy 0 <= p <= 1.")
    return p

def read_trials(default=10000):
    raw = input(f"Enter number of trials [default {default}]: ").strip()
    if raw == "":
        return ZZ(default)
    trials = ZZ(raw)
    if trials <= 0:
        raise ValueError("trials must be positive.")
    return trials

def read_bit_or_random():
    raw = input("Choose transmitted bit: 0, 1, or r for random [default r]: ").strip().lower()
    if raw == "":
        raw = "r"
    if raw == "r":
        return None
    if raw not in ["0", "1"]:
        raise ValueError("Enter 0, 1, or r.")
    return ZZ(raw)

def read_message(default="1,0,1,1,0"):
    raw = input(f"Enter comma-separated message bits [default {default}]: ").strip()
    if raw == "":
        raw = default
    bits = [ZZ(s.strip()) for s in raw.split(",") if s.strip() != ""]
    for b in bits:
        if b not in [0, 1]:
            raise ValueError("Message must contain only 0 and 1.")
    return bits

def read_p_values(default_max=0.50, default_step=0.02):
    p_max_raw = input(f"Enter maximum p value [default {default_max}]: ").strip()
    step_raw = input(f"Enter step size [default {default_step}]: ").strip()
    p_max = RR(default_max) if p_max_raw == "" else RR(p_max_raw)
    step = RR(default_step) if step_raw == "" else RR(step_raw)
    if p_max <= 0 or p_max > 1:
        raise ValueError("Maximum p must satisfy 0 < p <= 1.")
    if step <= 0:
        raise ValueError("Step size must be positive.")
    return srange(0, p_max + step/2, step)

def pause():
    input("\nPress Enter to continue...")

def print_menu():
    print("\n" + "="*58)
    print(" Repetition Code Simulator (Terminal Menu + Export)")
    print("="*58)
    print(" 1. Single-trial demo")
    print(" 2. Monte Carlo simulation")
    print(" 3. Theory vs simulation")
    print(" 4. Message transmission demo")
    print(" 5. Theory plot for one code length")
    print(" 6. Comparison table for n = 1,3,5,7,9")
    print(" 7. Multi-length theory plot")
    print(" 0. Exit")
    print("="*58)

def run_terminal_menu():
    while True:
        try:
            print_menu()
            choice = input("Select an option: ").strip()
            if choice == "0":
                print("Exiting simulator.")
                break
            elif choice == "1":
                n = read_odd_n(5); p = read_probability(0.2); bit = read_bit_or_random()
                RepetitionCodeSimulator(n).demo_single_trial(bit=bit, p=p)
                pause()
            elif choice == "2":
                n = read_odd_n(5); p = read_probability(0.2); trials = read_trials(10000); bit = read_bit_or_random()
                RepetitionCodeSimulator(n).simulate(bit=bit, p=p, trials=trials, verbose=True)
                pause()
            elif choice == "3":
                n = read_odd_n(5); p = read_probability(0.2); trials = read_trials(10000); bit = read_bit_or_random()
                RepetitionCodeSimulator(n).compare_with_theory(bit=bit, p=p, trials=trials)
                pause()
            elif choice == "4":
                n = read_odd_n(7); p = read_probability(0.08); bits = read_message("1,0,1,1,0")
                RepetitionCodeSimulator(n).transmit_message(bits, p=p, verbose=True)
                pause()
            elif choice == "5":
                n = read_odd_n(5); p_values = read_p_values(0.50, 0.02)
                G = RepetitionCodeSimulator(n).plot_theory(p_values)
                show(G)
                ask_save_plot(G, default_base=f"repetition_n{n}_theory")
                pause()
            elif choice == "6":
                p = read_probability(0.10); trials = read_trials(5000)
                show(RepetitionCodeSimulator.comparison_table([1,3,5,7,9], p=p, trials=trials))
                pause()
            elif choice == "7":
                p_values = read_p_values(0.50, 0.02)
                G = RepetitionCodeSimulator.plot_multiple_theory([1,3,5,7,9], p_values)
                show(G)
                ask_save_plot(G, default_base="repetition_compare_lengths")
                pause()
            else:
                print("Unknown choice.")
                pause()
        except Exception as e:
            print(f"\nError: {e}")
            pause()

if __name__ == "__main__":
    run_terminal_menu()
