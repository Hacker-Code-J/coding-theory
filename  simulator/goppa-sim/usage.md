GOOPA ALGEBRAIC GEOMETRY LAB - USAGE

1. INSTALLATION:
   - Install Python 3.x
   - Run: pip install streamlit numpy sympy

2. LAUNCH:
   - In your terminal, run: streamlit run app.py
   - A browser window will open automatically.

3. THE AG WORKFLOW:
   - SELECT FIELD: Choose a prime p for GF(p).
   - DEFINE DIVISOR: The 'Goppa Polynomial' degree acts as the divisor degree.
     In AG codes, this determines the dimension of the Riemann-Roch space.
   - OBSERVE MATRIX: Notice the matrix is no longer an Identity matrix + Parity.
     It is a matrix of 'Evaluations'. Each row is a basis function evaluated 
     at the points L.
   - ENCODE: Enter a message. The simulator computes the linear combination 
     of the basis functions.
   - VISUALIZE: The line chart shows the codeword as a 'discrete function' 
     sampled across the curve.
