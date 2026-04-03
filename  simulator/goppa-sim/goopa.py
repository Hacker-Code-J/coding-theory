from sage.all import *
import random
import time

# ANSI Color Codes
RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def create_goppa_code(q, m):
    k = GF(q, names=('a',))
    A = AffineSpace(k, 2, names=('x', 'y'))
    (x, y) = A._first_ngens(2)
    C = Curve(y**2 + y - x**m)
    F = C.function_field()
    pls = F.places()
    Q, = C.places_at_infinity()
    pls.remove(Q)
    G = (m-1) * Q
    return codes.EvaluationAGCode(pls, G)

def elem_to_hex(elem):
    try:
        return f"{elem.integer_representation():X}"
    except AttributeError:
        return "?"

def format_vec(vec, highlight_idx=-1, color=RED):
    return "[ " + " ".join(f"{color}{elem_to_hex(x)}{RESET}" if i == highlight_idx else elem_to_hex(x) for i, x in enumerate(vec)) + " ]"

def run_deep_linalg_visualizer():
    print(f"\n{CYAN}--- DEEP Linear Algebra Mechanics ---{RESET}")
    code = create_goppa_code(16, 3) 
    n, k = code.length(), code.dimension()
    F = code.base_field()
    H = code.parity_check_matrix()
    
    # Generate data
    message = vector(F, [F.random_element() for _ in range(k)])
    c = code.encode(message)
    
    # Inject error
    error_pos = random.randint(0, n-1)
    e = vector(F, n)
    e[error_pos] = F(1)
    r = c + e
    
    print(f"{YELLOW}Part 1: The Null Space Property (H * c = 0){RESET}")
    print("A valid codeword must exist entirely within the null space of H.")
    print(f"Codeword (c): {format_vec(c)}")
    print(f"Result of H*c : {format_vec(H * c, -1, GREEN)}  <- {GREEN}Perfectly Zero!{RESET}\n")
    time.sleep(2)

    print(f"{YELLOW}Part 2: The Error Projection (H * e = s){RESET}")
    print(f"Error Vec(e): {format_vec(e, error_pos, RED)}")
    print(f"Result of H*e : {format_vec(H * e, -1, RED)}  <- {RED}This is the Syndrome!{RESET}\n")
    time.sleep(2)

    print(f"{YELLOW}Part 3: The Distributive Property (Linearity){RESET}")
    print("Because matrix multiplication is linear, calculating the syndrome of")
    print("the received word (r = c + e) splits perfectly:")
    print("   H * r = H * (c + e)")
    print("   H * r = (H * c) + (H * e)")
    print(f"   H * r =   {GREEN}0{RESET}     +   {RED}s{RESET}")
    print(f"Result H*r    : {format_vec(H * r, -1, RED)}")
    print("Notice how the codeword 'c' was completely annihilated by H, leaving only 'e'!\n")
    time.sleep(3)

    print(f"{YELLOW}Part 4: Anatomy of a Dot Product (Row 0){RESET}")
    print(f"How is the very first element of the syndrome ({RED}{elem_to_hex((H*r)[0])}{RESET}) actually calculated?")
    print("It is the dot product of Row 0 of H and the received vector r:\n")
    
    row_0 = H.row(0)
    print(f"H Row 0 : {format_vec(row_0, error_pos, RED)}")
    print(f"Vec r   : {format_vec(r, error_pos, RED)}")
    
    # Calculate element-wise multiplication
    element_wise_products = [row_0[i] * r[i] for i in range(n)]
    print(f"Multiply: {format_vec(element_wise_products, error_pos, RED)}")
    
    # Calculate the sum (which in characteristic 2 is an XOR sum)
    final_sum = sum(element_wise_products)
    print(f"\nSumming (XORing) the 'Multiply' array yields the final scalar: {RED}{elem_to_hex(final_sum)}{RESET}")
    if final_sum == (H*r)[0]:
        print(f"{CYAN}Proof Complete: The dot product sum perfectly matches the first element of the Syndrome vector.{RESET}\n")

run_deep_linalg_visualizer()
