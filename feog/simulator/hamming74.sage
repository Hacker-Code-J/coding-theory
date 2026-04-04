# ============================================================
# Hamming (7,4) Code Simulator (Terminal Menu Version) in SageMath
# With PNG/PDF plot export
# ============================================================

from random import random, randint

class Hamming74Simulator:
    def __init__(self):
        self.F = GF(2)
        self.n = ZZ(7)
        self.k = ZZ(4)
        self.t = ZZ(1)
        self.G = matrix(self.F, [
            [1,0,0,0,1,1,0],
            [0,1,0,0,1,0,1],
            [0,0,1,0,0,1,1],
            [0,0,0,1,1,1,1],
        ])
        self.H = matrix(self.F, [
            [1,1,0,1,1,0,0],
            [1,0,1,1,0,1,0],
            [0,1,1,1,0,0,1],
        ])
        self.columns = {tuple(self.H.column(i)): i for i in range(self.n)}

    def _check_probability(self, p):
        if p < 0 or p > 1:
            raise ValueError("Probability p must satisfy 0 <= p <= 1.")

    def _message_vector(self, m):
        if len(m) != 4:
            raise ValueError("Message must have length 4.")
        bits = [int(x) for x in m]
        for b in bits:
            if b not in [0,1]:
                raise ValueError("Message bits must be binary.")
        return vector(self.F, bits)

    def _codeword_vector(self, c):
        if len(c) != 7:
            raise ValueError("Codeword must have length 7.")
        bits = [int(x) for x in c]
        for b in bits:
            if b not in [0,1]:
                raise ValueError("Codeword bits must be binary.")
        return vector(self.F, bits)

    def encode(self, m):
        m = self._message_vector(m)
        return m * self.G

    def random_message(self):
        return vector(self.F, [randint(0,1) for _ in range(4)])

    def random_error_vector(self, p):
        self._check_probability(p)
        return vector(self.F, [1 if random() < p else 0 for _ in range(7)])

    def transmit(self, c, p):
        c = self._codeword_vector(c)
        e = self.random_error_vector(p)
        y = c + e
        return y, e

    def syndrome(self, y):
        y = self._codeword_vector(y)
        return self.H * y.column()

    def correct(self, y):
        y = self._codeword_vector(y)
        s = tuple(self.syndrome(y))
        corrected = vector(self.F, list(y))
        error_position = None
        if s != (self.F(0), self.F(0), self.F(0)):
            if s in self.columns:
                error_position = self.columns[s]
                corrected[error_position] += self.F(1)
        return corrected, error_position

    def decode_message(self, y):
        corrected, error_position = self.correct(y)
        return vector(self.F, list(corrected[:4])), corrected, error_position

    def hamming_weight(self, v):
        return sum(ZZ(int(a)) for a in v)

    def theoretical_block_error_probability(self, p):
        self._check_probability(p)
        return RR(1) - RR((1-p)**7 + 7*p*(1-p)**6)

    def demo_single_trial(self, message=None, p=0.1):
        self._check_probability(p)
        if message is None:
            m = self.random_message()
        else:
            m = self._message_vector(message)
        c = self.encode(m)
        y, e = self.transmit(c, p)
        m_hat, corrected, error_position = self.decode_message(y)
        success = (m_hat == m)

        print("========================================")
        print(" Hamming (7,4) Single Trial")
        print("========================================")
        print(f"Message:             {list(m)}")
        print(f"Codeword:            {list(c)}")
        print(f"Error vector:        {list(e)}")
        print(f"Received word:       {list(y)}")
        print(f"Syndrome:            {list(self.syndrome(y))}")
        print(f"Corrected word:      {list(corrected)}")
        print(f"Flipped position:    {error_position}")
        print(f"Decoded message:     {list(m_hat)}")
        print(f"Hamming weight(e):   {self.hamming_weight(e)}")
        print(f"Success:             {success}")
        print("========================================")

    def simulate(self, p=0.1, trials=1000, verbose=False):
        self._check_probability(p)
        if trials <= 0:
            raise ValueError("trials must be positive.")
        errors = 0
        total_flips = 0
        for _ in range(trials):
            m = self.random_message()
            c = self.encode(m)
            y, e = self.transmit(c, p)
            m_hat, corrected, error_position = self.decode_message(y)
            total_flips += self.hamming_weight(e)
            if m_hat != m:
                errors += 1
        empirical = RR(errors) / RR(trials)
        theory = self.theoretical_block_error_probability(p)
        result = {
            "empirical_block_error_rate": empirical,
            "theoretical_block_error_rate": theory,
            "absolute_error_gap": abs(empirical - theory),
            "average_channel_flips": RR(total_flips) / RR(trials),
        }
        if verbose:
            print("========================================")
            print(" Hamming (7,4) Monte Carlo Simulation")
            print("========================================")
            print(f"Channel crossover probability:   p = {RR(p)}")
            print(f"Trials:                          {ZZ(trials)}")
            print(f"Average channel flips/trial:     {result['average_channel_flips']}")
            print(f"Empirical block error rate:      {result['empirical_block_error_rate']}")
            print(f"Theoretical block error rate:    {result['theoretical_block_error_rate']}")
            print(f"Absolute gap:                    {result['absolute_error_gap']}")
            print("========================================")
        return result

    def compare_with_theory(self, p=0.1, trials=10000):
        result = self.simulate(p=p, trials=trials, verbose=False)
        print("========================================")
        print(" Hamming (7,4): Theory vs Simulation")
        print("========================================")
        print(f"p = {RR(p)}, trials = {ZZ(trials)}")
        print(f"Empirical block error:   {result['empirical_block_error_rate']}")
        print(f"Theoretical block error: {result['theoretical_block_error_rate']}")
        print(f"Absolute gap:            {result['absolute_error_gap']}")
        print("========================================")

    def syndrome_table(self):
        rows = [["syndrome", "bit position to flip"]]
        rows.append([list(vector(self.F,[0,0,0])), "no flip"])
        for i in range(self.n):
            rows.append([list(self.H.column(i)), i])
        return table(rows=rows[1:], header_row=rows[0])

    def plot_theory(self, p_values):
        pts = [(RR(p), self.theoretical_block_error_probability(p)) for p in p_values]
        line_graph = list_plot(
            pts, plotjoined=True, thickness=2,
            axes_labels=[r"$p$", r"$P_{\mathrm{block\ error}}$"],
            title="Hamming (7,4) theoretical block error probability"
        )
        point_graph = list_plot(pts, plotjoined=False, marker='o', size=25)
        return line_graph + point_graph

def save_plot_both(G, base_name):
    png_name = f"{base_name}.png"
    pdf_name = f"{base_name}.pdf"
    G.save(png_name)
    G.save(pdf_name)
    print(f"Saved {png_name}")
    print(f"Saved {pdf_name}")

def ask_save_plot(G, default_base="plot"):
    raw = input("Save plot as PNG and PDF? [y/N]: ").strip().lower()
    if raw == "y":
        base = input(f"Base filename without extension [default {default_base}]: ").strip()
        if base == "":
            base = default_base
        save_plot_both(G, base)

def read_probability(default=0.1):
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

def read_message(default="1,0,1,1"):
    raw = input(f"Enter a 4-bit comma-separated message [default {default}]: ").strip()
    if raw == "":
        raw = default
    bits = [ZZ(s.strip()) for s in raw.split(",") if s.strip() != ""]
    if len(bits) != 4:
        raise ValueError("Need exactly 4 message bits.")
    for b in bits:
        if b not in [0,1]:
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
    print(" Hamming (7,4) Simulator (Terminal Menu + Export)")
    print("="*58)
    print(" 1. Single-trial demo")
    print(" 2. Monte Carlo simulation")
    print(" 3. Theory vs simulation")
    print(" 4. Syndrome table")
    print(" 5. Theory plot")
    print(" 0. Exit")
    print("="*58)

def run_terminal_menu():
    sim = Hamming74Simulator()
    while True:
        try:
            print_menu()
            choice = input("Select an option: ").strip()
            if choice == "0":
                print("Exiting simulator.")
                break
            elif choice == "1":
                p = read_probability(0.1)
                m = read_message("1,0,1,1")
                sim.demo_single_trial(message=m, p=p)
                pause()
            elif choice == "2":
                p = read_probability(0.1)
                trials = read_trials(10000)
                sim.simulate(p=p, trials=trials, verbose=True)
                pause()
            elif choice == "3":
                p = read_probability(0.1)
                trials = read_trials(10000)
                sim.compare_with_theory(p=p, trials=trials)
                pause()
            elif choice == "4":
                show(sim.syndrome_table())
                pause()
            elif choice == "5":
                p_values = read_p_values(0.50, 0.02)
                G = sim.plot_theory(p_values)
                show(G)
                ask_save_plot(G, default_base="hamming74_theory")
                pause()
            else:
                print("Unknown choice.")
                pause()
        except Exception as e:
            print(f"\nError: {e}")
            pause()

if __name__ == "__main__":
    run_terminal_menu()
